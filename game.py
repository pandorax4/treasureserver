
import geekcashapi as api
import util
import commit
import json
import os
import time
from util import log
import util
import model
import datacenter
import threading

fee = 0.05

rawdata_path = '../rawdata/{0}.json'

commit_file_curr_bets = '../geekcashlucky.github.io/curr_bets.json'

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
def write_last_update_view_block(block_height):
    f = open(last_update_view_record_file,'w')
    f.write(str(block_height))
    f.close()


def generate_bet_block_info(bet_block_height):
    log('Try Update bet block info: {}'.format(bet_block_height))
    bet_list = datacenter.get_bet_block_list(bet_block_height)
    if len(bet_list) > 0:
        log('Generate bet block info json , bet count: {}'.format(len(bet_list)))
        json_str = datacenter.get_bet_list_view_json(bet_list)
        file_path = bet_view_path.format(bet_block_height)
        f = open(file_path,'w')
        f.write(json_str)
        f.close()


def workthread_update_view():
    global is_updating_view
    #try:
    curr_block_height = api.get_curr_blockchain_height()
    last_update_block_height = curr_block_height
    # read last update block
    if os.path.exists(last_update_view_record_file):
        f = open(last_update_view_record_file,'r')
        text = f.read()
        f.close()
        last_update_block_height = int(text)

    if last_update_block_height > curr_block_height:
        log('Something wrong, last update block height is > curr block_height: {} > {}'.format(last_update_block_height,curr_block_height))
    elif last_update_block_height < curr_block_height:
        start = last_update_block_height + 1
        end = curr_block_height + 1
        last_bet_block = model.get_bet_block_height_by_join_block_height(last_update_block_height)
        # force update last bet block, because i'm not sure last bet block info is update successfuly.
        generate_bet_block_info(last_bet_block)
        for block_height in range(start,end):
            curr_bet_block = model.get_bet_block_height_by_join_block_height(block_height)
            if curr_bet_block != last_bet_block:
                generate_bet_block_info(curr_bet_block)
                last_bet_block = curr_bet_block
            last_update_block_height = block_height
            write_last_update_view_block(last_update_block_height)
    else:
        bet_block = model.get_bet_block_height_by_join_block_height(curr_block_height)
        generate_bet_block_info(bet_block)
        write_last_update_view_block(curr_block_height)

        # Commit to page

    is_updating_view = False
    #except Exception as _e:
    #    is_updating_view = False
     #   log('Update view exception: ' + str(_e))

    
def update_view():
    global is_updating_view
    if is_updating_view == True:
        return
    is_updating_view = True
    #try:
    t = threading.Thread(target=workthread_update_view)
    t.setDaemon(True)
    t.start()
    #except:
    #    is_updating_view = False




def check_and_payout():
    pass



# --------------------------------------------------------------------------------


# collect data
# balance collect
# payment
# generate static page
# update static page to github pages
def on_block_height_changed(prev_block_height, curr_block_height):
    global last_collect_balance_block_height
    log('On block height changed: {0} -> {1}'.format(prev_block_height, curr_block_height))
    
    # ================================================================
    '''
    NOTE: 确保这个过程不会中断，否则有可能会漏掉玩家转入的币
    '''
    unspent_data_dict = model.collect_unspent_data()

    # save raw unspent data
    start_time = time.time()
    raw_unspent_json_str = util.get_format_json(unspent_data_dict)
    raw_unspent_save_file = rawdata_path.format(curr_block_height)
    datacenter.write_data_to_file(raw_unspent_save_file,raw_unspent_json_str)
    end_time = time.time()
    print('Save raw unspent data used: {0}'.format(end_time - start_time))

    # save bet data
    start_time = time.time()
    bet_list = model.construct_bets(unspent_data_dict)
    datacenter.save_bet_data(bet_list)
    end_time = time.time()
    print('Construct bet list used: {0}'.format(end_time - start_time))

    # !!!!!!!!!! send all balance to one address !!!!!!!!!!
    if model.now_is_collect_balance_block(prev_block_height,curr_block_height):
        last_collect_balance_block_height = curr_block_height
        model.collect_balance(curr_block_height)
        return
    # ================================================================

    # closing bet
    start_time = time.time()
    print('Star Closing Process ...')
    unclosing_dbbet_dict = datacenter.get_unclosing_dbbet_dict()
    for bet_block_height in unclosing_dbbet_dict:
        if curr_block_height > bet_block_height:
            unclosing_dbbet_list = unclosing_dbbet_dict[bet_block_height]

            player_count = len(unclosing_dbbet_list)
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
                    payment_amount = bonus * bet_percentage
                    dbbet.payment_amount = payment_amount
                    dbbet.payment_state = 0
            datacenter.update_dbbet_list(unclosing_dbbet_list)
    end_time = time.time()
    print('Closing Process End! used: ', (end_time - start_time))

    # Check And payout
    if last_collect_balance_block_height > 0 and (curr_block_height - last_collect_balance_block_height > 1):
        check_and_payout()

    update_view()


def main_game_loop():
    print(' Game Start '.center(50,'='))
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
    #curr_height = api.get_curr_blockchain_height()
    #prev_height = curr_height - 1
    #on_block_height_changed(prev_height,curr_height)
    #result = api.send_to_many('main',address_list,amount_list, change,'test_send_many')
    #print(result)

