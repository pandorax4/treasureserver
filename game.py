
import geekcashapi as api
import time
from util import log
import util
import model
import datacenter

fee = 0.05
rawdata_path = '../rawdata/{0}.json'
commit_file_curr_bets = '../pandorax4.github.io/curr_bets.json'
last_update_view_record_file = '_last_view_block'
bet_view_path = '../betview/{0}.json'
is_updating_view = False
last_collect_balance_block_height = -1


def get_account_address_by_number(number):
    s_number = str(number)
    return model.account_addresses['account_' + s_number]


def get_sum_address():
    return model.account_addresses['sum']
    

def make_sure_network_updated():
    same_count = 0
    last_height = api.get_curr_blockchain_height()
    time.sleep(1)
    while True:
        curr_height = api.get_curr_blockchain_height()
        if curr_height == last_height and curr_height != 0:
            same_count += 1
        else:
            last_height = curr_height
            same_count = 0

        if same_count >= 10:
            log('Blockchain update OK!')
            break

        log('Sync Block {}'.format(curr_height))
        time.sleep(1)


# ------------------------------- About Game Logic -------------------------------

def save_raw_unspent_data_to_json(unspent_data_dict, curr_block_height):
    # save raw unspent data
    start_time = time.time()
    raw_unspent_json_str = util.get_format_json(unspent_data_dict)
    raw_unspent_save_file = rawdata_path.format(curr_block_height)
    datacenter.write_data_to_file(raw_unspent_save_file,raw_unspent_json_str)
    end_time = time.time()
    print('Save raw unspent data used: {0}'.format(end_time - start_time))


def save_unspent_data_to_database(bet_list):
    start_time = time.time()
    datacenter.save_bet_data(bet_list)
    end_time = time.time()
    print('Construct bet list used: {0}'.format(end_time - start_time))


def try_collect_all_balance(bet_list, curr_block_height):
    """
    1. 若 unspent_list 超过 30 则进行一次资金汇集
    2. 若 unspent_list 中有的块结果已出，则进行一次资金汇集
    """
    to_collect = False
    if len(bet_list) >= 30:
        to_collect = True
    else:
        for bet in bet_list:
            if curr_block_height >= bet.bet_block_height:
                to_collect = True
                break
    
    if to_collect:
        model.collect_balance(curr_block_height)


def try_closing_bets(curr_block_height):
    start_time = time.time()
    print('Star Closing Process ...')
    unclosing_dbbet_dict = datacenter.get_unclosing_dbbet_dict()
    for bet_block_height in unclosing_dbbet_dict:
        if curr_block_height > bet_block_height:
            unclosing_dbbet_list = unclosing_dbbet_dict[bet_block_height]

            win_player_count = 0
            lose_player_count = 0
            total_bet_amount = 0.0
            total_win_bet_amount = 0.0
            total_lose_bet_amount = 0.0

            bet_block_hash, bet_block_timestamp, nonce = api.get_block_hash_timestamp_nonce_by_height(bet_block_height)
            last_nonce_digit = int(str(nonce)[-1])
            
            # update bet block info
            for dbbet in unclosing_dbbet_list:
                dbbet.bet_block_hash = bet_block_hash
                dbbet.bet_block_timestamp = bet_block_timestamp
                dbbet.bet_block_nonce = nonce

                total_bet_amount += dbbet.bet_amount

                if dbbet.bet_nonce_last_digit == last_nonce_digit:
                    # win
                    dbbet.bet_state = 1
                    win_player_count += 1
                    total_win_bet_amount += dbbet.bet_amount
                else:
                    dbbet.bet_state = 0
                    lose_player_count += 1
                    total_lose_bet_amount += dbbet.bet_amount

            bonus = total_lose_bet_amount * (1.0 - fee)
            # calculate payment
            for dbbet in unclosing_dbbet_list:
                if dbbet.bet_state == 1:
                    bet_amount = dbbet.bet_amount
                    bet_percentage = bet_amount / total_win_bet_amount
                    reward_amount = bonus * bet_percentage
                    dbbet.reward_amount = reward_amount
                    dbbet.payment_state = 0
            datacenter.update_dbbet_list(unclosing_dbbet_list)
    end_time = time.time()
    print('Closing Process End! used: ', (end_time - start_time))


def try_pay_winers(curr_block_height):
    """
    检查资金库，若资金足够支付所有需要支付的资金，则进行支付，否则等下一轮
    :param curr_block_height:
    :return:
    """
    bet_list = datacenter.get_need_pay_dbbet_list()
    address_list = []
    amount_list = []
    for bet in bet_list:
        address_list.append(bet.payment_address)
        amount_list.append(bet.reward_amount + bet.bet_amount)

    pay_reward_txid = model.pay_reward(address_list,amount_list)

    if pay_reward_txid != -1:
        for bet in bet_list:
            bet.payment_txid = pay_reward_txid
            bet.payment_state = 1
        datacenter.update_dbbet_list(bet_list)
    else:
        print('No enough money to pay at block {0}, wait next block!'.format(curr_block_height))


def on_block_height_changed(prev_block_height, curr_block_height):
    log('On block height changed: {0} -> {1}'.format(prev_block_height, curr_block_height))
    
    # !!!! NOTE: 确保这个过程不会中断，否则有可能会漏掉玩家转入的币
    
    unspent_data_dict = model.collect_unspent_data()
    bet_list = model.construct_bets(unspent_data_dict)

    # 1. 将当前块未花费的数据保存起来
    save_raw_unspent_data_to_json(unspent_data_dict, curr_block_height)

    # 2. 将每一个地址的 unspent 数据存入数据库
    save_unspent_data_to_database(bet_list)

    # 3. 尝试资金汇集
    try_collect_all_balance(bet_list, curr_block_height)
    
    # 4. 尝试结算下注
    try_closing_bets(curr_block_height)

    # 5. 尝试支付赢家奖金
    try_pay_winers(curr_block_height)


def main_game_loop():
    print(' Game Start '.center(50, '='))
    last_block_height = api.get_curr_blockchain_height()
    print('Now Block {0}'.format(last_block_height))
    while True:
        if last_block_height == -1:
            last_block_height = api.get_curr_blockchain_height()
        else:
            curr_block_height = api.get_curr_blockchain_height()
            if curr_block_height == -1:
                log('Get current blockchain height faild!')
            else:
                if curr_block_height != last_block_height:
                    prev_block_height = last_block_height
                    last_block_height = curr_block_height
                    on_block_height_changed(prev_block_height, curr_block_height)

        time.sleep(1)


if __name__ == '__main__':
    datacenter.init_db()
    make_sure_network_updated()
    model.init_bet_addresses()
    main_game_loop()

