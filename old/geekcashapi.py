import json
import os
from roulette import log
import util

command_prefix = 'gcli'


def do_command(command):
    command = command_prefix + ' ' + command
    result = os.popen(command).read().strip()

    if result.startswith('error code'):
        print('EXCEPTION: ', result)
        return -1
    else:
        return result


def get_account_name_by_address(_address):
    command = 'getaccount {0}'.format(_address)
    result = do_command(command)
    if result == -1:
        log('Get account name by address faild: {0}'.format(_address))
        return -1
    return result


def get_account_address(account_name):
    """
    Get geekcash address by account name, if the account no address, create new one.
    """
    command = 'getaddressesbyaccount {0}'.format(account_name)
    result = do_command(command)
    if result == -1:
        log('Fatal error: get addresses by account faild!')
        return -1

    json_obj = json.loads(result)
    address_count = len(json_obj)
    if address_count == 0:
        log('no account address: {0}, to create new one!'.format(account_name))
        command = 'getaccountaddress {0}'.format(account_name)
        result = do_command(command)
        if result == -1:
            log('Fatal error, create new address faild: {0}'.format(account_name))
            return -1
        else:
            return result
    else:
        return json_obj[0]


def get_curr_blockchain_height():
    command = 'getblockcount'
    return int(do_command(command))


def get_block_hash_by_height(block_height):
    command = 'getblockhash {0}'.format(block_height)
    return do_command(command)


def get_block_info_by_hash(block_hash):
    command = 'getblockheader "{0}"'.format(block_hash)
    return do_command(command)


def get_block_info_by_height(block_height):
    block_hash = get_block_hash_by_height(block_height)
    if block_hash != -1:
        return get_block_info_by_hash(block_hash)
    return -1


def get_block_height_by_hash(block_hash):
    block_info = get_block_info_by_hash(block_hash)
    if block_info != -1:
        json_obj = json.loads(block_info)
        return json_obj['height']
    return -1


def get_block_timestamp_by_hash(block_hash):
    block_info = get_block_info_by_hash(block_hash)
    if block_info != -1:
        json_obj = json.loads(block_info)
        return json_obj['time']
    return -1


def get_block_timestamp_by_height(block_height):
    block_hash = get_block_hash_by_height(block_height)
    if block_hash != -1:
        return get_block_timestamp_by_hash(block_hash)
    return -1


def get_block_nonce_by_hash(block_hash):
    block_info = get_block_info_by_hash(block_hash)
    if block_info != -1:
        json_obj = json.loads(block_info)
        return json_obj['nonce']
    return -1


def get_block_nonce_by_height(block_height):
    block_hash = get_block_hash_by_height(block_height)
    if block_hash != -1:
        return get_block_nonce_by_hash(block_hash)
    return -1


def get_block_timestamp_nonce_by_hash(block_hash):
    block_info = get_block_info_by_hash(block_hash)
    if block_info != -1:
        json_obj = json.loads(block_info)
        return json_obj['time'], json_obj['nonce']
    return -1,-1


def get_block_hash_timestamp_nonce_by_height(block_height):
    block_hash = get_block_hash_by_height(block_height)
    if block_hash != -1:
        timestamp, nonce = get_block_timestamp_nonce_by_hash(block_hash)
        if timestamp != -1 and nonce != -1:
            return block_hash, timestamp, nonce
    return -1, -1, -1


def get_block_hash_height_time_by_txid(_txid):
    command = 'getrawtransaction {0} 1'.format(_txid)
    result = do_command(command)
    if result == -1:
        log('get block hash and hgith and time faild: {0}', _txid)
        return -1,-1,-1
    json_obj = json.loads(result)
    block_hash = json_obj['blockhash']
    block_height = json_obj['height']
    block_time = json_obj['blocktime']
    return block_hash,block_height,block_time


def get_balance_by_address(_address):
    unspent_list = get_unspent_list_by_address(_address)
    if unspent_list == -1:
        log('get balance by address faild: {}'.format(_address))
        return -1
    balance = 0
    for unspent in unspent_list:
        amount = unspent['amount']
        balance += amount
    return balance


def get_input_address_and_mount(vin_txid, vin_vout):
    command = 'getrawtransaction {0} 1'.format(vin_txid)
    result = do_command(command)
    if result == -1:
        return -1,-1
    json_obj = json.loads(result)
    input_address_array = json_obj['vout'][vin_vout]['scriptPubKey']['addresses']
    input_amount = json_obj['vout'][vin_vout]['value']
    print('Input: ',input_address_array)
    print('Amount: ',input_amount)
    return input_address_array[0],input_amount


def get_input_vin_list_by_unspent_txid(unspent_txid):
    command = 'getrawtransaction {0} 1'.format(unspent_txid)
    result = do_command(command)
    if result == -1:
        return -1
    json_obj = json.loads(result)
    return json_obj['vin']


def get_unspent_list_by_address(_address):
    """
    return: a list that contains all unspent info of _address
    [{
        "txid": "5c729ac838168de171676388ee40c3d786b750624429d78e62edc8a75500fef0",
        "vout": 0,
        "address": "GSGe3BWjtdNQ5KA9TjnL6TD6jeZm57RweT",
        "account": "'main2'",
        "scriptPubKey": "76a9145c6dbbbc8d7c9391bdd509c05fec20688f05b41d88ac",
        "amount": 2.00000000,
        "confirmations": 1036,
        "ps_rounds": -2,
        "spendable": true,
        "solvable": true
    }]
    """
    command = 'listunspent 0 999999999 [\\"{0}\\"]'.format(_address)
    result = do_command(command)
    if result != -1:
        json_obj = json.loads(result)
        return json_obj
    return -1


def get_unspent_list():
    command = 'listunspent'
    result = do_command(command)
    if result != -1:
        json_obj = json.loads(result)
        return json_obj
    return -1


def get_payment_address(unspent_txid, unspent_address):
    command = 'getrawtransaction {0} 1'.format(unspent_txid)
    result = do_command(command)
    if result == -1:
        log('get payment address faild, get rawtrasaction by unspent_txid faild!')
        return -1

    json_obj = json.loads(result)
    vout_array = json_obj['vout']
    vout_count = len(vout_array)

    if vout_count == 1:     # 没有找零地址，从vin中获取输入地址
        receive_address = vout_array[0]['scriptPubKey']['addresses'][0]
        if receive_address != unspent_address:
            log('Fatal Error: receive address is not equal unspent address \njson:{0}'.format(result))
            return -1
        # detect input address from vin txid
        vin_array = json_obj['vin']
        vin_txid = vin_array[0]['txid']
        vin_vout = vin_array[0]['vout']
        command = 'getrawtransaction {0} 1'.format(vin_txid)
        result = do_command(command)
        if result == -1:
            log('get payment address faild, get rawtransaction by vin_txid faild! vin_txid: {0} vin_vout:{1}'.format(vin_txid, vin_vout))
            return -1
        json_obj = json.loads(result)
        vout = json_obj['vout'][vin_vout]
        payment_address = vout['scriptPubKey']['addresses'][0]
        return payment_address
    elif vout_count == 2:   # 有找零地址，直接使用找零地址
        for vout in vout_array:
            vout_address = vout['scriptPubKey']['addresses'][0]
            if vout_address != unspent_address:
                return vout_address
        log('Fatal error , unknow error!')
        return -1
    else:
        log("Fuck, i can't detect the payment address!")
        return -1


def send_to_many(from_address, address_list, amount_list, change_address, comment=''):
    """
    from_address:   which address to payout
    address_list:   which addresses you want to pay ['address1','address2','address3']
    amount_list:    the item length is match to address_list, the amount you want to pay for each address
    change_address: basically , the change_address is the address of from_account, make sure account has just one address, that's very clear
    comment:        comment is the comment of command, whatever
    Note:           receiver pay the fee!
    """
    address_count = len(address_list)
    amount_count = len(amount_list)
    if address_count != amount_count:
        print("Address Count and Amount count is not match!")
        return -1

    account_name = get_account_name_by_address(from_address)
    if account_name == -1:
        log('send to many get account name faild: {0}'.format(from_address))
        return -1

    account_balance = get_balance_by_address(from_address)
    if account_balance == -1:
        print("Get Balance Faild!, can't payout!")
        return -1

    total_payout = 0.0
    for x in range(0, amount_count):
        total_payout += amount_list[x]
    
    total_change = account_balance - total_payout
    total_change = round(total_change, 8)

    if total_change < 0:
        print("Balance not enough, can't payout! balance:{0},payout:{1}".format(account_balance, total_payout))
        return -1

    payout_str = ''
    address_str = ''
    # combine receivers
    for x in range(0, address_count):
        address = address_list[x]
        amount = amount_list[x]
        payout_str += '\\"{0}\\":{1},'.format(address, amount)
        address_str += '\\"{0}\\",'.format(address)
        print('Payout {0} {1}'.format(address, amount))

    print('Change {0} {1}'.format(change_address, total_change))

    # combine change
    if total_change > 0 and change_address is not None:
        payout_str += '\\"{0}\\":{1},'.format(change_address, total_change)
        address_str += '\\"{0}\\",'.format(change_address)

    payout_str = '"{' + payout_str[:-1] + '}"'
    address_str = '"[' + address_str[:-1] + ']"'

    command = 'sendmany "{0}" {1} 0 false "{2}" {3}'.format(account_name, payout_str, comment, address_str)
    
    return do_command(command)


def send_to_address(from_address, address, amount, change_address, comment=''):
    address_list = [address]
    amount_list = [amount]
    return send_to_many(from_address, address_list, amount_list, change_address, comment)


def send_all_balance_to_address(from_address, to_address, comment=''):
    account_balance = get_balance_by_address(from_address)
    if account_balance == -1:
        log('FAILD! Get Balance Faild!, cant payout!')
        return -1

    if account_balance == 0:
        # print('No Balance in address {0}'.format(from_address))
        return -1

    address_list = [to_address]
    amount_list = [account_balance]
    log('Send all balance from {} -> {}'.format(from_address, to_address))
    return send_to_many(from_address, address_list, amount_list, None, comment)


def create_raw_transaction(unspent_list, send_dict, change_address=None):
    input_amount = 0
    input_list = []
    for unspent in unspent_list:
        input_txid = unspent['txid']
        vout = unspent['vout']
        amount = unspent['amount']
        input_amount += amount
        a_input = {'"txid"': '"{}"'.format(input_txid), '"vout"': vout}
        input_list.append(a_input)

    fee = ((len(unspent_list) * 180 + (len(send_dict) + 1) * 34 + 10 + 40) / 1024) * 0.000015
    fee = util.get_precision(fee, 8)
    print("Raw Fee: ", fee)
    out_dict = {}

    total_send_amount = 0
    for address in send_dict:
        send_amount = send_dict[address]
        send_amount = util.get_precision(send_amount, 8)
        total_send_amount += send_amount
        key = '"{}"'.format(address)
        out_dict[key] = send_amount

    total_send_amount = util.get_precision(total_send_amount, 8)
    change_amount = input_amount - total_send_amount - fee
    change_amount = util.get_precision(change_amount, 8)

    print("Input Amount: ", input_amount, "Send Amount: ", total_send_amount, "Change Amount: ", change_amount, "fee: ",
          fee)

    if change_amount < 0:
        print("No enough money to send!")
        return -1

    if change_address is None:
        key = '"{}"'.format(change_address)
        out_dict[key] = change_amount

    txid_json_str = json.dumps(input_list)
    output_json_str = json.dumps(out_dict)

    command = 'createrawtransaction "{}" "{}"'.format(txid_json_str, output_json_str)
    return do_command(command)


def sign_raw_transaction(raw_transaction_hash):
    command = 'signrawtransaction "{}"'.format(raw_transaction_hash)
    result = do_command(command)
    if result == -1:
        return -1
    else:
        return json.loads(result)


def send_raw_transaction(signed_raw_transaction_hex):
    command = 'sendrawtransaction "{}"'.format(signed_raw_transaction_hex)
    return do_command(command)


def send_unspent_to_address(unspent, to_address):
    input_txid = unspent['txid']
    vout = unspent['vout']
    amount = unspent['amount']
    amount_minus_fee = amount - 0.00001100
    txid_array = [{'"txid"': '"{}"'.format(input_txid), '"vout"': vout}]
    output_dict = {'"{}"'.format(to_address): amount_minus_fee}

    txid_json_str = json.dumps(txid_array)
    output_json_str = json.dumps(output_dict)

    command = 'createrawtransaction "{}" "{}"'.format(txid_json_str, output_json_str)

    # create raw transaction
    result = do_command(command)
    if result == -1:
        return -1

    # sign raw transaction
    command = 'signrawtransaction "{}"'.format(result)
    result = do_command(command)
    if result == -1:
        return -1

    result = json.loads(result)

    # send raw transaction
    command = 'sendrawtransaction "{}"'.format(result['hex'])
    result = do_command(command)

    if result != -1:
        print(result, amount_minus_fee, '->', to_address)

    return result


def send_unspent_list_to_address(unspent_list, to_address):
    send_amount = 0
    input_list = []
    for unspent in unspent_list:
        input_txid = unspent['txid']
        vout = unspent['vout']
        amount = unspent['amount']
        send_amount += amount
        a_input = {'"txid"': '"{}"'.format(input_txid), '"vout"': vout}
        input_list.append(a_input)

    fee = ((len(unspent_list) * 180 + 1 * 34 + 10 + 40) / 1024) * 0.000015
    fee = util.get_precision(fee, 8)
    send_amount -= fee
    send_amount = util.get_precision(send_amount, 8)

    output_dict = {'"{}"'.format(to_address): send_amount}

    txid_json_str = json.dumps(input_list)
    output_json_str = json.dumps(output_dict)

    command = 'createrawtransaction "{}" "{}"'.format(txid_json_str, output_json_str)

    # create raw transaction
    result = do_command(command)
    if result == -1:
        print("Send unspent list to address faild at Create Raw Transaction Command!")
        return -1

    # sign raw transaction
    command = 'signrawtransaction "{}"'.format(result)
    result = do_command(command)
    if result == -1:
        print("Send unspent list to address faild at Sign Raw Transaction Command!")
        return -1

    result = json.loads(result)

    # send raw transaction
    command = 'sendrawtransaction "{}"'.format(result['hex'])
    result = do_command(command)

    if result != -1:
        print("Input count: {}".format(len(unspent_list)))
        print(result, send_amount, '->', to_address, "fee: {}".format(fee))

    return result


def from_unspent_list_send_to_many(unspent_list, send_dict, change_address):
    raw_transaction_hash = create_raw_transaction(unspent_list, send_dict, change_address)
    if raw_transaction_hash != -1:
        signed_raw_transaction = sign_raw_transaction(raw_transaction_hash)
        print("Sign result: \n", signed_raw_transaction)
        if signed_raw_transaction != -1:
            signed_raw_transaction_hex = signed_raw_transaction['hex']
            send_txid = send_raw_transaction(signed_raw_transaction_hex)
            print("result txid:\n", send_txid)
        else:
            print("Signed raw transaction faild!")
    else:
        print("Create raw transaction faild")


def list_all_address_balance():
    unspent_list = get_unspent_list()
    total_balance = 0.0
    for unspent in unspent_list:
        input_txid = unspent['txid']
        address = unspent['address']
        balance = unspent['amount']
        total_balance += balance
        print(input_txid, address, balance)

    print("\n")
    print("Unspent Count: ", len(unspent_list))
    print("All balance: ", total_balance)




# TODO: 待测试
# 1. 使用代码瞬间转入多笔


'''
1. 单输入
    - 有找零 支付到零钱地址
    - 无找零 使用vin中第1个输入中的txid取得rawtransaction2，使用vin中第1个输入中的vout作为索引，去rawtrasaction2中vout数组中拿到输入地址
2. 多输入
    - 有找零 支付到零钱地址
    - 无找零 使用vin中第1个输入中的txid取得rawtransaction2，使用vin中第1个输入中的vout作为索引，去rawtrasaction2中vout数组中拿到输入地址
'''

'''
bet_txid = "5c729ac838168de171676388ee40c3d786b750624429d78e62edc8a75500fef0"
bet_address = "GSGe3BWjtdNQ5KA9TjnL6TD6jeZm57RweT"

result = get_payment_address(bet_txid, bet_address)
print(result)
'''


#main_address = get_account_address("main")
#to_address = "GKQxy9ZfaqCbqhvn6Jxt5LuLY48SRfYMHo"
bank_address = "GaVMbZ755ie3b39Au3pi9LkFd2pGG4mU9a"






#result = send_to_address(from_address, to_address, 2.0, from_address, "Comment")
#print("Result: ",result)

'''
address_list = []
amount_list = []

for x in range(500):
    account_name = "sub_{}".format(x)
    address = get_account_address(account_name)
    # print(account_name, address)
    balance = get_balance_by_address(address)
    # address_list.append(address)
    # amount_list.append(2.0)
    if balance > 0.0:
        print(account_name, address, balance)
    #print("Collect from {}, collect balance {}".format(address, balance))
    #result = send_all_balance_to_address(address, bank_address, "Collect From {}".format(account_name))
    #print(result)
'''
# print("Ready TO Send: ")

# result = send_to_many(bank_address, address_list, amount_list, bank_address, "Test send to 500 address")
# print("Result: ", result)

'''
address = "GgZgnTdyqBtxAzxi25Tyeuy3c3ueYex2fs"

unspent_list = get_unspent_list_by_address(address)

for unspent in unspent_list:
    result = send_unspent_to_address(unspent, bank_address)
    print(result)
'''

'''
for x in range(500):
    account_name = "sub_{}".format(x)
    address = get_account_address(account_name)
    unspent_list = get_unspent_list_by_address(address)
    for unspent in unspent_list:
        print("Account: ", account_name, address)
        send_unspent_to_address(unspent, bank_address)
'''


'''
unspent_list = get_unspent_list()
unspent_count = 0
for unspent in unspent_list:
    print(unspent['txid'], unspent['address'], unspent['amount'])
    unspent_count += 1

print("Unspent Count: ", unspent_count)
print("\n")

result = send_unspent_list_to_address(unspent_list, bank_address)

print("Result: \n", result)
'''

'''
unspent_list = get_unspent_list_by_address("GQAuXY5SyZMNqqRcCCSJkQG22BTcYQzaP4")
send_dict = {"GeJajKMpAirXdYEeWEHQDJtSfDv6F9p8a6":2.0, "GYatfDCWQDPFJHMWsCLy2rcvN1RoZ5xNg8": 3.0}

'''



'''

# generate many address
send_dict = {}
for x in range(1001):
    account_name = "sub_{}".format(x)
    address = get_account_address(account_name)
    send_dict[address] = 3.0
    #print(account_name, address)

print("Construct send dict OK!")

unspent_list = get_unspent_list()

print("Construct unspent list OK!")

from_unspent_list_send_to_many(unspent_list, send_dict, bank_address)
'''

#list_all_address_balance()

input_unspent_list = []
for x in range(1001):
    account_name = "sub_{}".format(x)
    address = get_account_address(account_name)
    unspent_list = get_unspent_list_by_address(address)
    input_unspent_list += unspent_list

to_address = "GaVMbZ755ie3b39Au3pi9LkFd2pGG4mU9a"

send_unspent_list_to_address(input_unspent_list, to_address)


# 2018.09.14 00:22
# 测试失败，因为一次发送的输入为1000个，太多了，接下来要测试一下使用 RPC 是否可以，如果 RPC 也不可以，那就减少
# 一次发送的交易量