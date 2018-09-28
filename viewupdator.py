"""
1. 主页（三个页面，small, big, large）
2. 规则页面（1个页面）
3. 所有历史游戏界面（列表形式，每轮游戏一行，只包含具体页面的页头信息）（三个页面，small, big, large)
4. 每轮游戏具体页面（每轮游戏一个页面，small, big, large 显示在同一个页面
5. 当前游戏下注页面（未结算的）
"""

import db
import model

view_root = "./view/generated/"
view_ch_root = view_root + "ch/"
view_ch_small_bet_root = view_ch_root + "smallbet/"
view_ch_big_bet_root = view_ch_root + "bigbet/"
view_ch_large_bet_root = view_ch_root + "largebet/"

view_en_root = view_root + "en/"
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


def generate_index_page():
    f = open(template_index_file, "r", encoding="utf-8")
    html = f.read()
    f.close()

    param_dict = {
        "small_bet_number_0_total_bet": db.get_total_bet_count(1, 0),
        "small_bet_number_0_total_bet_amount": db.get_total_bet_amount(1, 0),
        "small_bet_number_0_win_count": db.get_bet_number_total_win_count(1, 0),
        "small_bet_number_0_address": model.get_small_bet_address_by_number(0),

        "small_bet_number_1_total_bet": db.get_total_bet_count(1, 1),
        "small_bet_number_1_total_bet_amount": db.get_total_bet_amount(1, 1),
        "small_bet_number_1_win_count": db.get_bet_number_total_win_count(1, 1),
        "small_bet_number_1_address": model.get_small_bet_address_by_number(1),

        "small_bet_number_2_total_bet": db.get_total_bet_count(1, 2),
        "small_bet_number_2_total_bet_amount": db.get_total_bet_amount(1, 2),
        "small_bet_number_2_win_count": db.get_bet_number_total_win_count(1, 2),
        "small_bet_number_2_address": model.get_small_bet_address_by_number(2),

        "small_bet_number_3_total_bet": db.get_total_bet_count(1, 3),
        "small_bet_number_3_total_bet_amount": db.get_total_bet_amount(1, 3),
        "small_bet_number_3_win_count": db.get_bet_number_total_win_count(1, 3),
        "small_bet_number_3_address": model.get_small_bet_address_by_number(3),

        "small_bet_number_4_total_bet": db.get_total_bet_count(1, 4),
        "small_bet_number_4_total_bet_amount": db.get_total_bet_amount(1, 4),
        "small_bet_number_4_win_count": db.get_bet_number_total_win_count(1, 4),
        "small_bet_number_4_address": model.get_small_bet_address_by_number(4),

        "small_bet_number_5_total_bet": db.get_total_bet_count(1, 5),
        "small_bet_number_5_total_bet_amount": db.get_total_bet_amount(1, 5),
        "small_bet_number_5_win_count": db.get_bet_number_total_win_count(1, 5),
        "small_bet_number_5_address": model.get_small_bet_address_by_number(5),

        "small_bet_number_6_total_bet": db.get_total_bet_count(1, 6),
        "small_bet_number_6_total_bet_amount": db.get_total_bet_amount(1, 6),
        "small_bet_number_6_win_count": db.get_bet_number_total_win_count(1, 6),
        "small_bet_number_6_address": model.get_small_bet_address_by_number(6),

        "small_bet_number_7_total_bet": db.get_total_bet_count(1, 7),
        "small_bet_number_7_total_bet_amount": db.get_total_bet_amount(1, 7),
        "small_bet_number_7_win_count": db.get_bet_number_total_win_count(1, 7),
        "small_bet_number_7_address": model.get_small_bet_address_by_number(7),

        "small_bet_number_8_total_bet": db.get_total_bet_count(1, 8),
        "small_bet_number_8_total_bet_amount": db.get_total_bet_amount(1, 8),
        "small_bet_number_8_win_count": db.get_bet_number_total_win_count(1, 8),
        "small_bet_number_8_address": model.get_small_bet_address_by_number(8),

        "small_bet_number_9_total_bet": db.get_total_bet_count(1, 9),
        "small_bet_number_9_total_bet_amount": db.get_total_bet_amount(1, 9),
        "small_bet_number_9_win_count": db.get_bet_number_total_win_count(1, 9),
        "small_bet_number_9_address": model.get_small_bet_address_by_number(9),

        "big_bet_number_0_total_bet": db.get_total_bet_count(2, 0),
        "big_bet_number_0_total_bet_amount": db.get_total_bet_amount(2, 0),
        "big_bet_number_0_win_count": db.get_bet_number_total_win_count(2, 0),
        "big_bet_number_0_address": model.get_big_bet_address_by_number(0),

        "big_bet_number_1_total_bet": db.get_total_bet_count(2, 1),
        "big_bet_number_1_total_bet_amount": db.get_total_bet_amount(2, 1),
        "big_bet_number_1_win_count": db.get_bet_number_total_win_count(2, 1),
        "big_bet_number_1_address": model.get_big_bet_address_by_number(1),

        "big_bet_number_2_total_bet": db.get_total_bet_count(2, 2),
        "big_bet_number_2_total_bet_amount": db.get_total_bet_amount(2, 2),
        "big_bet_number_2_win_count": db.get_bet_number_total_win_count(2, 2),
        "big_bet_number_2_address": model.get_big_bet_address_by_number(2),

        "big_bet_number_3_total_bet": db.get_total_bet_count(2, 3),
        "big_bet_number_3_total_bet_amount": db.get_total_bet_amount(2, 3),
        "big_bet_number_3_win_count": db.get_bet_number_total_win_count(2, 3),
        "big_bet_number_3_address": model.get_big_bet_address_by_number(3),

        "big_bet_number_4_total_bet": db.get_total_bet_count(2, 4),
        "big_bet_number_4_total_bet_amount": db.get_total_bet_amount(2, 4),
        "big_bet_number_4_win_count": db.get_bet_number_total_win_count(2, 4),
        "big_bet_number_4_address": model.get_big_bet_address_by_number(4),

        "big_bet_number_5_total_bet": db.get_total_bet_count(2, 5),
        "big_bet_number_5_total_bet_amount": db.get_total_bet_amount(2, 5),
        "big_bet_number_5_win_count": db.get_bet_number_total_win_count(2, 5),
        "big_bet_number_5_address": model.get_big_bet_address_by_number(5),

        "big_bet_number_6_total_bet": db.get_total_bet_count(2, 6),
        "big_bet_number_6_total_bet_amount": db.get_total_bet_amount(2, 6),
        "big_bet_number_6_win_count": db.get_bet_number_total_win_count(2, 6),
        "big_bet_number_6_address": model.get_big_bet_address_by_number(6),

        "big_bet_number_7_total_bet": db.get_total_bet_count(2, 7),
        "big_bet_number_7_total_bet_amount": db.get_total_bet_amount(2, 7),
        "big_bet_number_7_win_count": db.get_bet_number_total_win_count(2, 7),
        "big_bet_number_7_address": model.get_big_bet_address_by_number(7),

        "big_bet_number_8_total_bet": db.get_total_bet_count(2, 8),
        "big_bet_number_8_total_bet_amount": db.get_total_bet_amount(2, 8),
        "big_bet_number_8_win_count": db.get_bet_number_total_win_count(2, 8),
        "big_bet_number_8_address": model.get_big_bet_address_by_number(8),

        "big_bet_number_9_total_bet": db.get_total_bet_count(2, 9),
        "big_bet_number_9_total_bet_amount": db.get_total_bet_amount(2, 9),
        "big_bet_number_9_win_count": db.get_bet_number_total_win_count(2, 9),
        "big_bet_number_9_address": model.get_big_bet_address_by_number(9),

        "large_bet_number_0_total_bet": db.get_total_bet_count(3, 0),
        "large_bet_number_0_total_bet_amount": db.get_total_bet_amount(3, 0),
        "large_bet_number_0_win_count": db.get_bet_number_total_win_count(3, 0),
        "large_bet_number_0_address": model.get_large_bet_address_by_number(0),

        "large_bet_number_1_total_bet": db.get_total_bet_count(3, 1),
        "large_bet_number_1_total_bet_amount": db.get_total_bet_amount(3, 1),
        "large_bet_number_1_win_count": db.get_bet_number_total_win_count(3, 1),
        "large_bet_number_1_address": model.get_large_bet_address_by_number(1),

        "large_bet_number_2_total_bet": db.get_total_bet_count(3, 2),
        "large_bet_number_2_total_bet_amount": db.get_total_bet_amount(3, 2),
        "large_bet_number_2_win_count": db.get_bet_number_total_win_count(3, 2),
        "large_bet_number_2_address": model.get_large_bet_address_by_number(2),

        "large_bet_number_3_total_bet": db.get_total_bet_count(3, 3),
        "large_bet_number_3_total_bet_amount": db.get_total_bet_amount(3, 3),
        "large_bet_number_3_win_count": db.get_bet_number_total_win_count(3, 3),
        "large_bet_number_3_address": model.get_large_bet_address_by_number(3),

        "large_bet_number_4_total_bet": db.get_total_bet_count(3, 4),
        "large_bet_number_4_total_bet_amount": db.get_total_bet_amount(3, 4),
        "large_bet_number_4_win_count": db.get_bet_number_total_win_count(3, 4),
        "large_bet_number_4_address": model.get_large_bet_address_by_number(4),

        "large_bet_number_5_total_bet": db.get_total_bet_count(3, 5),
        "large_bet_number_5_total_bet_amount": db.get_total_bet_amount(3, 5),
        "large_bet_number_5_win_count": db.get_bet_number_total_win_count(3, 5),
        "large_bet_number_5_address": model.get_large_bet_address_by_number(5),

        "large_bet_number_6_total_bet": db.get_total_bet_count(3, 6),
        "large_bet_number_6_total_bet_amount": db.get_total_bet_amount(3, 6),
        "large_bet_number_6_win_count": db.get_bet_number_total_win_count(3, 6),
        "large_bet_number_6_address": model.get_large_bet_address_by_number(6),

        "large_bet_number_7_total_bet": db.get_total_bet_count(3, 7),
        "large_bet_number_7_total_bet_amount": db.get_total_bet_amount(3, 7),
        "large_bet_number_7_win_count": db.get_bet_number_total_win_count(3, 7),
        "large_bet_number_7_address": model.get_large_bet_address_by_number(7),

        "large_bet_number_8_total_bet": db.get_total_bet_count(3, 8),
        "large_bet_number_8_total_bet_amount": db.get_total_bet_amount(3, 8),
        "large_bet_number_8_win_count": db.get_bet_number_total_win_count(3, 8),
        "large_bet_number_8_address": model.get_large_bet_address_by_number(8),

        "large_bet_number_9_total_bet": db.get_total_bet_count(3, 9),
        "large_bet_number_9_total_bet_amount": db.get_total_bet_amount(3, 9),
        "large_bet_number_9_win_count": db.get_bet_number_total_win_count(3, 9),
        "large_bet_number_9_address": model.get_large_bet_address_by_number(9),
    }

    # Small -------------------------------------
    curr_game_round = db.get_curr_unsettle_game_round(1)
    param_dict["small_curr_game_round"] = curr_game_round
    param_dict["small_curr_bet_count"] = db.get_curr_unsettle_count(1)
    param_dict["small_curr_bet_amount"] = db.get_curr_unsettle_amount(1)
    prev_game_round = curr_game_round - 1

    bet_round_data = None
    if prev_game_round >= 1:
        bet_round_data = db.get_bet_round_data(1, prev_game_round)

    if bet_round_data is None:
        param_dict["small_prev_bet_count"] = 0
        param_dict["small_prev_bet_count"] = 0
        param_dict["small_prev_bet_amount"] = 0
        param_dict["small_prev_winner_count"] = 0
        param_dict["small_prev_loser_count"] = 0
        param_dict["small_prev_total_reward"] = 0
        param_dict["small_prev_reward_number"] = 0
    else:
        param_dict["small_prev_bet_count"] = bet_round_data.bet_count
        param_dict["small_prev_bet_amount"] = bet_round_data.total_bet_amount
        param_dict["small_prev_winner_count"] = bet_round_data.winner_count
        param_dict["small_prev_loser_count"] = bet_round_data.loser_count
        param_dict["small_prev_total_reward"] = bet_round_data.total_reward
        param_dict["small_prev_reward_number"] = bet_round_data.bet_number
    # Small ------------------------------------- End

    # Big ------------------------------------------
    curr_game_round = db.get_curr_unsettle_game_round(2)
    param_dict["big_curr_game_round"] = curr_game_round
    param_dict["big_curr_bet_count"] = db.get_curr_unsettle_count(2)
    param_dict["big_curr_bet_amount"] = db.get_curr_unsettle_amount(2)
    prev_game_round = curr_game_round - 1

    bet_round_data = None
    if prev_game_round >= 1:
        bet_round_data = db.get_bet_round_data(2, prev_game_round)

    if bet_round_data is None:
        param_dict["big_prev_bet_count"] = 0
        param_dict["big_prev_bet_count"] = 0
        param_dict["big_prev_bet_amount"] = 0
        param_dict["big_prev_winner_count"] = 0
        param_dict["big_prev_loser_count"] = 0
        param_dict["big_prev_total_reward"] = 0
        param_dict["big_prev_reward_number"] = 0
    else:
        param_dict["big_prev_bet_count"] = bet_round_data.bet_count
        param_dict["big_prev_bet_amount"] = bet_round_data.total_bet_amount
        param_dict["big_prev_winner_count"] = bet_round_data.winner_count
        param_dict["big_prev_loser_count"] = bet_round_data.loser_count
        param_dict["big_prev_total_reward"] = bet_round_data.total_reward
        param_dict["big_prev_reward_number"] = bet_round_data.bet_number
    # Big ------------------------------------- End

    # Large ------------------------------------------
    curr_game_round = db.get_curr_unsettle_game_round(3)
    param_dict["large_curr_game_round"] = curr_game_round
    param_dict["large_curr_bet_count"] = db.get_curr_unsettle_count(3)
    param_dict["large_curr_bet_amount"] = db.get_curr_unsettle_amount(3)
    prev_game_round = curr_game_round - 1

    bet_round_data = None
    if prev_game_round >= 1:
        bet_round_data = db.get_bet_round_data(2, prev_game_round)

    if bet_round_data is None:
        param_dict["large_prev_bet_count"] = 0
        param_dict["large_prev_bet_count"] = 0
        param_dict["large_prev_bet_amount"] = 0
        param_dict["large_prev_winner_count"] = 0
        param_dict["large_prev_loser_count"] = 0
        param_dict["large_prev_total_reward"] = 0
        param_dict["large_prev_reward_number"] = 0
    else:
        param_dict["large_prev_bet_count"] = bet_round_data.bet_count
        param_dict["large_prev_bet_amount"] = bet_round_data.total_bet_amount
        param_dict["large_prev_winner_count"] = bet_round_data.winner_count
        param_dict["large_prev_loser_count"] = bet_round_data.loser_count
        param_dict["large_prev_total_reward"] = bet_round_data.total_reward
        param_dict["large_prev_reward_number"] = bet_round_data.bet_number
    # Large ------------------------------------- End

    bet_template = """
    <div class="bet-item">
            <span>{{join_txid}}</span>
            <span>{{join_time}}</span>
            <span>{{bet_number}}</span>
            <span>{{bet_amount}}</span>
            <span>{{bet_level}}</span>
            <span>{{player_address}}</span>
    </div>
    """

    """
           <span>下注txid</span>
           <span>下注时间</span>
           <span>下注数字</span>
           <span>下注金额</span>
           <span>下注等级</span>
           <span>玩家地址</span>
    """

    settled_bet_template = """
        <div class="bet-item">
                <span>{{join_txid}}</span>
                <span>{{join_time}}</span>
                <span>{{bet_round}}</span>
                <span>{{bet_number}}</span>
                <span>{{bet_amount}}</span>
                <span>{{bet_level}}</span>
                {{bet_profit}}
                <span>{{player_address}}</span>
        </div>
        """

    # recently unsettle bet list
    recently_unsettle_bet_list = db.get_recently_unsettle_bet_list()
    unsettle_bet_content = ""
    for bet in recently_unsettle_bet_list:
        bet_str = bet_template
        bet_str = bet_str.replace("{{join_txid}}", bet.join_txid[0:10])
        bet_str = bet_str.replace("{{join_time}}", str(bet.created_at))
        bet_str = bet_str.replace("{{bet_number}}", str(bet.bet_number))
        bet_str = bet_str.replace("{{bet_amount}}", str(bet.bet_amount))
        if bet.bet_level == 1:
            bet_level_str = "小赌注"
        elif bet.bet_level == 2:
            bet_level_str = "中赌注"
        elif bet.bet_level == 3:
            bet_level_str = "大赌注"
        bet_str = bet_str.replace("{{bet_level}}", bet_level_str)
        bet_str = bet_str.replace("{{player_address}}", bet.payment_address)
        unsettle_bet_content += bet_str + "\n\n"
    html = html.replace("{{recently_bets_content}}", unsettle_bet_content)

    # recently settled bet list
    recently_settled_bet_list = db.get_recently_settled_bet_list(100)
    settled_bet_content = ""
    for bet in recently_settled_bet_list:
        bet_str = settled_bet_template
        bet_str = bet_str.replace("{{join_txid}}", bet.join_txid[0:10])
        bet_str = bet_str.replace("{{join_time}}", str(bet.created_at))
        bet_str = bet_str.replace("{{bet_round}}", str(bet.game_round))
        bet_str = bet_str.replace("{{bet_number}}", str(bet.bet_number))
        bet_str = bet_str.replace("{{bet_amount}}", str(bet.bet_amount))
        if bet.bet_level == 1:
            bet_level_str = "小赌注"
        elif bet.bet_level == 2:
            bet_level_str = "中赌注"
        elif bet.bet_level == 3:
            bet_level_str = "大赌注"
        bet_str = bet_str.replace("{{bet_level}}", bet_level_str)
        if bet.bet_state == 1:
            profit_str = '<span style="color=green"> ' + str(bet.reward_amount + bet.bet_amount) + ' </span>'
        else:
            profit_str = '<span style="color=red"> -' + str(bet.reward_amount + bet.bet_amount) + ' </span>'
        bet_str = bet_str.replace("{{bet_profit}}", profit_str)
        bet_str = bet_str.replace("{{player_address}}", bet.payment_address)
        settled_bet_content += bet_str + "\n\n"
    html = html.replace("{{recently_settled_content}}", unsettle_bet_content)

    html = html.replace("{{small_min_bet_amount}}", str(model.get_min_bet_amount(1)))
    html = html.replace("{{big_min_bet_amount}}", str(model.get_min_bet_amount(2)))
    html = html.replace("{{large_min_bet_amount}}", str(model.get_min_bet_amount(3)))

    for key in param_dict:
        # print(key, param_dict[key])
        html = html.replace("{{" + key + "}}", str(param_dict[key]))
    html_file = get_index_file_path(1)
    f = open(html_file, "w", encoding="utf-8")
    f.write(html)
    f.close()


def push_page():
    pass


def update_view(_small_settled_round_list, _big_settled_round_list, _large_settled_round_list):
    generate_index_page()

    generate_settled_bet_detail_page(_small_settled_round_list, 1)
    generate_settled_bet_detail_page(_big_settled_round_list, 2)
    generate_settled_bet_detail_page(_large_settled_round_list, 3)

    generate_settled_history_page(1)
    generate_settled_history_page(2)
    generate_settled_history_page(3)

    push_page()


def regenerate_all():
    generate_index_page()
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


db.init_db()
regenerate_all()
