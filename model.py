import geekcashapi as api
import os
import json
from util import log
import sys

game_start_block_height = 180000
block_count_of_round = 100
balance_collect_block_count = 10        # every 10 block to collect all bet balance to collect account

account_prefix = 'account_'

addresses2number = {}
number2addresses = {}
addresses = []

collect_balance_address = ""


class Bet(object):
    def __init__(self):
        self.join_txid = ''
        self.join_block_height = -1
        self.join_block_hash = ''
        self.join_block_timestamp = -1
        
        self.bet_block_height = -1
        self.bet_block_hash = ''        # get from result
        self.bet_block_timestamp = -1   # get from result
        self.bet_block_nonce = -1       # get from result

        self.bet_address = ''
        self.bet_amount = -1
        self.bet_nonce_last_digit = -1
        
        self.payment_address = ''
        self.bet_state = -1     # -1 no result, 0 lose, 1 win



def init_bet_addresses():
    global addresses, number2addresses,addresses2number, collect_balance_address

    account_name = 'collection'
    collect_balance_address = api.get_account_address(account_name)
    if collect_balance_address == -1:
        sys.exit()

    address_file = 'number2addresses.txt'
    if os.path.exists(address_file):
        f = open(address_file,'r')
        str_data = f.read()
        f.close()
        json_obj = json.loads(str_data)
        for num in json_obj:
            address = json_obj[num]
            addresses.append(address)
            number2addresses[num] = address
            addresses2number[address] = num
            #print(num,address)
    else:
        for num in range(0,10):
            account_name = '{0}{1}'.format(account_prefix, num)
            address = api.get_account_address(account_name)
            if address == -1:
                sys.exit()
            else:
                addresses.append(address)
                number2addresses[num] = address
                addresses2number[address] = num
        
        
        json_str = json.dumps(number2addresses, indent=4, separators=(',',':'))
        f = open(address_file,'w')
        f.write(json_str)
        f.close()

    print('Addresses loaded:')
    for num in number2addresses:
        print(num, number2addresses[num])
    


def get_bet_block_height_by_join_block_height(block_height):
    if block_height % block_count_of_round == 0:
        return block_height

    part = int(block_height / block_count_of_round)
    bet_block = (part + 1) * block_count_of_round
    return bet_block


def now_is_bet_block(curr_block_height):
    if curr_block_height % block_count_of_round == 0:
        return True
    else:
        return False


def now_is_collect_balance_block(prev_block_height, curr_block_height):
    if curr_block_height % balance_collect_block_count == 0:
        return True
    
    diff = curr_block_height - prev_block_height
    if diff > 1:
        for x in range(prev_block_height + 1, curr_block_height + 1):
            if x % balance_collect_block_count == 0:
                return True
    return False


def create_abet(_join_txid, _bet_address, _bet_amount):
    bet = Bet()

    join_txid = _join_txid
    join_block_hash, join_block_height, join_block_timestamp = api.get_block_hash_height_time_by_txid(join_txid)
    bet_block_height = get_bet_block_height_by_join_block_height(join_block_height)
    bet_address = _bet_address
    bet_amount = _bet_amount
    bet_nonce_last_digit = addresses2number[bet_address]
    payment_address = api.get_payment_address(join_txid, bet_address)

    if payment_address in addresses:
        log('Fatal error , payment address is bet address! {}'.format(payment_address))
        sys.exit()

    bet.join_txid = join_txid
    bet.join_block_height = int(join_block_height)
    bet.join_block_hash = join_block_hash
    bet.join_block_timestamp = int(join_block_timestamp)
    bet.bet_block_height = int(bet_block_height)
    bet.bet_address = bet_address
    bet.bet_amount = bet_amount
    bet.bet_nonce_last_digit = int(bet_nonce_last_digit)
    bet.payment_address = payment_address

    return bet


def collect_unspent_data():
    '''
    return: {address:unspent_list,...}
    '''
    unspent_data_dict = {}
    for address in addresses:
        unspent_list = api.get_unspent_list_by_address(address)
        unspent_data_dict[address] = unspent_list
    return unspent_data_dict


def construct_bets(unspent_data_dict):
    try:
        bet_list = []
        for address in unspent_data_dict:
            unspent_list = unspent_data_dict[address]
            bet_address = address
            for unspent in unspent_list:
                join_txid = unspent['txid']
                bet_amount = unspent['amount']
                abet = create_abet(join_txid,bet_address,bet_amount)
                bet_list.append(abet)
        return bet_list
    except Exception as _e:
        log('!!!!! Construct bets faild! ' + str(_e))
        sys.exit()


def collect_balance(curr_block_height):
    for address in addresses:
        api.send_all_balance_to_address(address,collect_balance_address,'collect at {}'.format(curr_block_height))