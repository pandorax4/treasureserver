"""
1. 主页（三个页面，small, big, large）
2. 规则页面（1个页面）
3. 所有历史游戏界面（列表形式，每轮游戏一行，只包含具体页面的页头信息）（三个页面，small, big, large)
4. 每轮游戏具体页面（每轮游戏一个页面，small, big, large 显示在同一个页面
5. 当前游戏下注页面（未结算的）
"""

import db
import model
import json


index_ch = "index_ch.json"
index_en = "index_en.json"
rules_ch = "rules_ch.json"
rules_en = "rules_en.json"
bet_ch = "bet_ch.json"
bet_en = "bet_en.json"
history_ch = "history_ch.json"
history_en = "history_en.json"

index_data = "index_data.json"
bet_small_data = "bet_small_{}.json"
bet_big_data = "bet_big_{}.json"
bet_large_data = "bet_large_{}.json"
history_small_bet_data = "history_small_bet.json"
history_big_bet_data = "history_big_bet.json"
history_large_bet_data = "history_large_bet.json"






# view_root = "./view/generated/"
view_root = "D:/nginx-1.15.4/html/"
view_ch_root = view_root + ""
view_ch_small_bet_root = view_ch_root + "smallbet/"
view_ch_big_bet_root = view_ch_root + "bigbet/"
view_ch_large_bet_root = view_ch_root + "largebet/"

view_en_root = view_root + ""
view_en_small_bet_root = view_en_root + "smallbet/"
view_en_big_bet_root = view_en_root + "bigbet/"
view_en_large_bet_root = view_en_root + "largebet/"


def get_index_file_path(_lang=0):
    """
    :param _lang: 0 english, 1 chinese
    :return:
    """
    if _lang == 0:
        return view_en_root + "index.html"
    else:
        return view_ch_root + "index.html"


def get_history_file_path(_bet_level, _lang=0):
    html_name = "history.html"
    if _lang == 0:
        if _bet_level == 1:
            return view_en_small_bet_root + html_name
        if _bet_level == 2:
            return view_en_big_bet_root + html_name
        if _bet_level == 3:
            return view_en_large_bet_root + html_name
    if _lang == 1:
        if _bet_level == 1:
            return view_ch_small_bet_root + html_name
        if _bet_level == 2:
            return view_ch_big_bet_root + html_name
        if _bet_level == 3:
            return view_ch_large_bet_root + html_name


def get_bet_detail_file_path(_bet_level, _bet_round, _lang=0):
    html_name = "{}.html".format(_bet_round)
    if _lang == 0:
        if _bet_level == 1:
            return view_en_small_bet_root + html_name
        if _bet_level == 2:
            return view_en_big_bet_root + html_name
        if _bet_level == 3:
            return view_en_large_bet_root + html_name
    if _lang == 1:
        if _bet_level == 1:
            return view_ch_small_bet_root + html_name
        if _bet_level == 2:
            return view_ch_big_bet_root + html_name
        if _bet_level == 3:
            return view_ch_large_bet_root + html_name


template_index_file = "./view/template/ch/index.html"
template_bet_file = "./view/template/ch/bet.html"
template_history_file = "./view/template/ch/history.html"


"""
def get_generated_bet_file_path(_bet_level, _bet_round):
    if _bet_level == 1:
        return "{}{}/{}.html".format(generated_bet_detail_root, "small", _bet_round)
    elif _bet_level == 2:
        return "{}{}/{}.html".format(generated_bet_detail_root, "big", _bet_round)
    elif _bet_level == 3:
        return "{}{}/{}.html".format(generated_bet_detail_root, "large", _bet_round)
    return None


def get_generated_bet_history_file_path(_bet_level):
    page_name = "history"
    if _bet_level == 1:
        return "{}{}/{}.html".format(generated_bet_history_root, "small", page_name)
    elif _bet_level == 2:
        return "{}{}/{}.html".format(generated_bet_history_root, "big", page_name)
    elif _bet_level == 3:
        return "{}{}/{}.html".format(generated_bet_history_root, "large", page_name)
    return None
"""


# 生成每一轮赌注详情页（包含每一个下注）
def generate_settled_bet_detail_page(_round_list, _bet_level):
    f = open(template_bet_file, "r", encoding="utf-8")
    html = f.read()
    f.close()

    for bet_round in _round_list:
        round_html = html
        bet_round_data = db.get_bet_round_data(_bet_level, bet_round)
        if bet_round_data is None:
            continue
        settled_bet_list = db.get_settled_bet_list(_bet_level, bet_round)
        round_html = round_html.replace("{{game_round}}", str(bet_round_data.bet_round))
        round_html = round_html.replace("{{bet_level}}", str(bet_round_data.bet_level))
        round_html = round_html.replace("{{reward_number}}", str(bet_round_data.bet_number))
        round_html = round_html.replace("{{start_block}}", str(bet_round_data.start_block))
        round_html = round_html.replace("{{end_block}}", str(bet_round_data.settled_block - 1))
        round_html = round_html.replace("{{reward_block}}", str(bet_round_data.settled_block))
        round_html = round_html.replace("{{total_bet_count}}", str(bet_round_data.bet_count))
        round_html = round_html.replace("{{total_bet_amount}}", str(bet_round_data.total_bet_amount))
        round_html = round_html.replace("{{winner_count}}", str(bet_round_data.winner_count))
        round_html = round_html.replace("{{loser_count}}", str(bet_round_data.loser_count))
        round_html = round_html.replace("{{total_reward}}", str(bet_round_data.total_reward))

        bet_item_html = """
        <div class="bet-item">
            <span>{{join_txid}}</span>
            <span>{{join_time}}</span>
            <span>{{bet_number}}</span>
            <span>{{bet_amount}}</span>
            {{profit_amount}}
            <span>{{reward_txid}}</span>
        </div>  
        """
        bet_content = ""
        for bet in settled_bet_list:
            bet_str = bet_item_html
            bet_str = bet_str.replace("{{join_txid}}", bet.join_txid)
            bet_str = bet_str.replace("{{join_time}}", str(bet.created_at))
            bet_str = bet_str.replace("{{bet_number}}", str(bet.bet_number))
            bet_str = bet_str.replace("{{bet_amount}}", str(bet.bet_amount))
            if bet.bet_state == 0:
                new_str = '<span class="bet-lose">-' + str(bet.reward_amount) + '</span>'
                bet_str = bet_str.replace("{{profit_amount}}", new_str)
                bet_str = bet_str.replace("{{reward_txid}}", "-")
            else:
                new_str = '<span>' + str(bet.reward_amount) + '</span>'
                bet_str = bet_str.replace("{{profit_amount}}", new_str)
                bet_str = bet_str.replace("{{reward_txid}}", bet.reward_txid)
            bet_content += bet_str + "\n\n"

        round_html = round_html.replace("{{bets_content}}", bet_content)

        bet_html_file = get_bet_detail_file_path(_bet_level, bet_round, 1)
        f = open(bet_html_file, "w", encoding="utf-8")
        f.write(round_html)
        f.close()


def generate_settled_history_page(_bet_level):
    header_list = db.get_settled_header_list(_bet_level)
    if len(header_list) == 0:
        return

    f = open(template_history_file, "r", encoding="utf-8")
    html = f.read()
    f.close()

    item_html_template = """
    <div class="game-item">
        <span>{{bet_round}}</span>
        <span>{{bet_number}}</span>
        <span>{{bet_count}}</span>
        <span>{{bet_amount}}</span>
        <span>{{winner_count}}</span>
        <span>{{loser_count}}</span>
        <span>{{total_reward}}</span>
        <span>{{start_block}}</span>
        <span>{{end_block}}</span>
        <span>{{reward_block}}</span>
        <span>{{nonce}}</span>
    </div>
    
    """
    history_content = ""
    for header in header_list:
        item_html = item_html_template
        item_html = item_html.replace("{{bet_round}}", str(header.bet_round))
        item_html = item_html.replace("{{bet_number}}", str(header.bet_number))
        item_html = item_html.replace("{{bet_count}}", str(header.bet_count))
        item_html = item_html.replace("{{bet_amount}}", str(header.total_bet_amount))
        item_html = item_html.replace("{{winner_count}}", str(header.winner_count))
        item_html = item_html.replace("{{loser_count}}", str(header.loser_count))
        item_html = item_html.replace("{{total_reward}}", str(header.total_reward))
        item_html = item_html.replace("{{start_block}}", str(header.start_block))
        item_html = item_html.replace("{{end_block}}", str(header.settled_block - 1))
        item_html = item_html.replace("{{reward_block}}", str(header.settled_block))
        item_html = item_html.replace("{{nonce}}", str(header.block_nonce))
        history_content += item_html + "\n\n"

    html = html.replace("{{history_bet_content}}", history_content)

    html_file = get_history_file_path(_bet_level, 1)
    f = open(html_file, "w", encoding="utf-8")
    f.write(html)
    f.close()


def push_page():
    pass


class BetAddress(object):
    def __init__(self, _bet_level, _number):
        self.number = _number
        self.address = model.get_bet_address(_bet_level, self.number)
        self.total_bet_count = db.get_total_bet_count(_bet_level, self.number)
        self.total_bet_amount = db.get_total_bet_amount(_bet_level, self.number)
        self.total_win_count = db.get_bet_number_total_win_count(_bet_level, self.number)

    def get_json_obj(self):
        return {
            "number": self.number,
            "address": self.address,
            "total_bet_count": self.total_bet_count,
            "total_bet_amount": self.total_bet_amount,
            "total_win_count": self.total_win_count,
        }


class CurrBetInfo(object):
    def __init__(self, _bet_level):
        self.round = db.get_curr_unsettle_game_round(_bet_level)
        self.bet_count = db.get_curr_unsettle_count(_bet_level)
        self.bet_amount = db.get_curr_unsettle_amount(_bet_level)

    def get_json_obj(self):
        return {
            "round": self.round,
            "bet_count": self.bet_count,
            "bet_amount": self.bet_amount,
        }


class SettledBetInfo(object):
    def __init__(self, _bet_level):
        self.round = db.get_last_game_round_number(_bet_level)
        self.bet_count = 0
        self.bet_amount = 0
        self.winner_count = 0
        self.loser_count = 0
        self.total_reward = 0
        self.bet_number = -1

        if self.round > 0:
            bet_round_data = db.get_bet_round_data(_bet_level, self.round)
            if bet_round_data is not None:
                self.bet_count = bet_round_data.bet_count
                self.bet_amount = bet_round_data.total_bet_amount
                self.winner_count = bet_round_data.winner_count
                self.loser_count = bet_round_data.loser_count
                self.total_reward = bet_round_data.total_reward
                self.bet_number = bet_round_data.bet_number

    def get_json_obj(self):
        return {
            "round": self.round,
            "bet_count": self.bet_count,
            "bet_amount": self.bet_amount,
            "winner_count": self.winner_count,
            "loser_count": self.loser_count,
            "total_reward": self.total_reward,
            "bet_number": self.bet_number,
        }


class UnSettleBet(object):
    def __init__(self,
                 _join_txid,
                 _join_block,
                 _bet_round,
                 _bet_level,
                 _bet_number,
                 _bet_amount,
                 _player_address,
                 _join_time):
        self.short_txid = _join_txid[:10] + "..."
        self.join_block = _join_block
        self.short_txid_link_to = ""
        self.bet_round = _bet_round
        self.bet_level = _bet_level
        self.bet_number = _bet_number
        self.bet_amount = _bet_amount
        self.player_address = _player_address
        self.join_time = _join_time

    def get_json_obj(self):
        return {
            "short_txid": self.short_txid,
            "join_block": self.join_block,
            "short_txid_link_to": self.short_txid_link_to,
            "bet_round": self.bet_round,
            "bet_level": self.bet_level,
            "bet_number": self.bet_number,
            "bet_amount": self.bet_amount,
            "player_address": self.player_address,
            "join_time": self.join_time,
        }


class SettledBet(object):
    def __init__(self,
                 _join_txid,
                 _join_block,
                 _settled_block,
                 _bet_round,
                 _bet_level,
                 _bet_number,
                 _bet_amount,
                 _bet_reward,
                 _bet_state,
                 _player_address,
                 _join_time):
        self.short_txid = _join_txid[:10] + "..."
        self.join_block = _join_block
        self.settled_block = _settled_block
        self.short_txid_link_to = ""
        self.bet_round = _bet_round
        self.bet_level = _bet_level
        self.bet_number = _bet_number
        self.bet_amount = _bet_amount
        self.bet_reward = _bet_reward
        self.bet_state = _bet_state
        self.player_address = _player_address
        self.join_time = _join_time

        if self.bet_state == 1:
            self.bet_reward += self.bet_amount
        else:
            self.bet_reward = -self.bet_amount

    def get_json_obj(self):
        return {
            "short_txid": self.short_txid,
            "join_block": self.join_block,
            "settled_block": self.settled_block,
            "short_txid_link_to": self.short_txid_link_to,
            "bet_round": self.bet_round,
            "bet_level": self.bet_level,
            "bet_number": self.bet_number,
            "bet_amount": self.bet_amount,
            "bet_reward": self.bet_reward,
            "player_address": self.player_address,
            "join_time": self.join_time,
        }


class BetLevel(object):
    def __init__(self, _bet_level):
        self.addresses = []
        self.min_bet_amount = model.get_min_bet_amount(_bet_level)
        self.curr_bet_info = CurrBetInfo(_bet_level)
        self.prev_bet_info = SettledBetInfo(_bet_level)
        self.recently_winners = []
        self.init_addresses(_bet_level)
        self.init_recently_winners(_bet_level)

    def get_json_obj(self):
        return {
            "addresses": self.addresses,
            "min_bet_amount": self.min_bet_amount,
            "curr_bet_info": self.curr_bet_info.get_json_obj(),
            "prev_bet_info": self.prev_bet_info.get_json_obj(),
            "recently_winners": self.recently_winners,
        }

    def init_addresses(self, _bet_level):
        for x in range(10):
            self.addresses.append(BetAddress(_bet_level, x).get_json_obj())

    def init_recently_winners(self, _bet_level):
        bet_list = db.get_recently_winner_list(_bet_level, 7)
        for bet in bet_list:
            settledbet = SettledBet(
                bet.join_txid,
                bet.join_block_height,
                bet.settlement_block_height,
                bet.game_round,
                bet.bet_level,
                bet.bet_number,
                bet.bet_amount,
                bet.reward_amount,
                bet.bet_state,
                bet.payment_address,
                bet.created_at.strftime("%Y-%m-%d %H:%M:%S")
            )
            self.recently_winners.append(settledbet.get_json_obj())


class PageIndex(object):
    def __init__(self):
        self.small_bets = BetLevel(1).get_json_obj()
        self.big_bets = BetLevel(2).get_json_obj()
        self.large_bets = BetLevel(3).get_json_obj()
        self.recently_unsettle_bets = []
        self.recently_settled_bets = []
        self.init_recently_settled_bets()
        self.init_recently_unsettle_bets()

    def get_json_obj(self):
        return {
            "small_bets": self.small_bets,
            "big_bets": self.big_bets,
            "large_bets": self.large_bets,
            "recently_unsettle_bets": self.recently_unsettle_bets,
            "recently_settled_bets": self.recently_settled_bets,
        }

    def init_recently_unsettle_bets(self):
        bet_list = db.get_recently_unsettle_bet_list()
        for bet in bet_list:
            unsettlebet = UnSettleBet(
                bet.join_txid,
                bet.join_block_height,
                bet.game_round,
                bet.bet_level,
                bet.bet_number,
                bet.bet_amount,
                bet.payment_address,
                bet.created_at.strftime("%Y-%m-%d %H:%M:%S")
            )
            self.recently_unsettle_bets.append(unsettlebet.get_json_obj())

    def init_recently_settled_bets(self):
        bet_list = db.get_recently_settled_bet_list(100)
        for bet in bet_list:
            settledbet = SettledBet(
                bet.join_txid,
                bet.join_block_height,
                bet.settlement_block_height,
                bet.game_round,
                bet.bet_level,
                bet.bet_number,
                bet.bet_amount,
                bet.reward_amount,
                bet.bet_state,
                bet.payment_address,
                bet.created_at.strftime("%Y-%m-%d %H:%M:%S")
            )
            self.recently_settled_bets.append(settledbet.get_json_obj())


def generate_index_data_json():
    page_index = PageIndex().get_json_obj()
    json_str = json.dumps(page_index)
    with open("index.json", "w", encoding="utf-8") as f:
        f.write(json_str)


def update_view(_small_settled_round_list, _big_settled_round_list, _large_settled_round_list):

    generate_settled_bet_detail_page(_small_settled_round_list, 1)
    generate_settled_bet_detail_page(_big_settled_round_list, 2)
    generate_settled_bet_detail_page(_large_settled_round_list, 3)

    generate_settled_history_page(1)
    generate_settled_history_page(2)
    generate_settled_history_page(3)

    push_page()


def regenerate_all():
    small_last_game_round = db.get_last_game_round_number(1)
    big_last_game_round = db.get_last_game_round_number(2)
    large_last_game_round = db.get_last_game_round_number(3)

    if small_last_game_round > 0:
        game_round_list = []
        for x in range(1, small_last_game_round + 1):
            game_round_list.append(x)
        generate_settled_bet_detail_page(game_round_list, 1)

    if big_last_game_round > 0:
        game_round_list = []
        for x in range(1, big_last_game_round + 1):
            game_round_list.append(x)
        generate_settled_bet_detail_page(game_round_list, 2)

    if large_last_game_round > 0:
        game_round_list = []
        for x in range(1, large_last_game_round + 1):
            game_round_list.append(x)
        generate_settled_bet_detail_page(game_round_list, 3)

    generate_settled_history_page(1)
    generate_settled_history_page(2)
    generate_settled_history_page(3)


#db.init_db()
#regenerate_all()
#generate_index_page()
