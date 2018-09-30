small_bet_account_name_prefix = "small_bet_"
big_bet_account_name_prefix = "big_bet_"
large_bet_account_name_prefix = "large_bet_"
small_bet_address_dict = {}
small_address_number_dict = {}
small_number_address_dict = {}
big_bet_address_dict = {}
big_address_number_dict = {}
big_number_address_dict = {}
large_bet_address_dict = {}
large_address_number_dict = {}
large_number_address_dict = {}

bet_level_min_amount_dict = {
    1: 20,
    2: 10000,
    3: 100000,
}


def get_small_bet_address_by_number(_number):
    account_name = "{}{}".format(small_bet_account_name_prefix, _number)
    return small_bet_address_dict.get(account_name, None)


def get_big_bet_address_by_number(_number):
    account_name = "{}{}".format(big_bet_account_name_prefix, _number)
    return big_bet_address_dict.get(account_name, None)


def get_large_bet_address_by_number(_number):
    account_name = "{}{}".format(large_bet_account_name_prefix, _number)
    return large_bet_address_dict.get(account_name, None)


def get_min_bet_amount(_bet_level):
    return bet_level_min_amount_dict.get(_bet_level, 1000)


def get_bet_address(_bet_level, _bet_number):
    if _bet_level == 1:
        return get_small_bet_address_by_number(_bet_number)
    elif _bet_level == 2:
        return get_big_bet_address_by_number(_bet_number)
    elif _bet_level == 3:
        return get_large_bet_address_by_number(_bet_number)
    return None