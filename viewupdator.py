"""
1. 主页（三个页面，small, big, large）
2. 规则页面（1个页面）
3. 所有历史游戏界面（列表形式，每轮游戏一行，只包含具体页面的页头信息）（三个页面，small, big, large)
4. 每轮游戏具体页面（每轮游戏一个页面，small, big, large 显示在同一个页面
5. 当前游戏下注页面（未结算的）
"""

import db
import model

view_root = "../"
template_index_file = "./view/template/index.html"
template_bet_file = "./view/template/bet.html"
template_history_file = "./view/template/history.html"

generated_index_file = "./view/generated/index.html"


# 生成每一轮小赌注详情页（包含每一个下注）
def generate_small_settled_bet_detail_page(_round_list):
	# TODO: read html page template
	for game_round in _round_list:
		bet_list = db.get_bet_list_by_round(game_round)
		html_content = ""
		page_path = "{}{}.html".format(view_root, game_round)


# 生成每一轮中赌注详情页（包含每一个下注）
def generate_big_settled_bet_detail_page(_round_list):
	pass


# 生成每一轮大赌注详情页（包含每一个下注）
def generate_large_settled_bet_detail_page(_round_list):
	pass


# 生成小赌注历史汇总页
def generate_small_settled_header_page():
	pass


# 生成中赌注历史汇总页
def generate_big_settled_header_page():
	pass


# 生成大赌注历史汇总页
def generate_large_settled_header_page():
	pass


# 生成本轮游戏（未结算）详情页（包含每一个下注）
def generate_current_bet_round_detail_page():
	pass


def generate_index_page():
	f = open(template_index_file, "r", encoding="utf-8")
	html = f.read()
	f.close()
	print(html)

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

	for key in param_dict:
		# print(key, param_dict[key])
		html = html.replace("{{" + key + "}}", str(param_dict[key]))
	f = open(generated_index_file,"w")
	f.write(html)
	f.close()


def push_page():
	pass


def update_view(_small_settled_round_list, _big_settled_round_list, _large_settled_round_list):
	generate_small_settled_bet_detail_page(_small_settled_round_list)
	generate_big_settled_bet_detail_page(_big_settled_round_list)
	generate_large_settled_bet_detail_page(_large_settled_round_list)
	generate_small_settled_header_page()
	generate_big_settled_header_page()
	generate_large_settled_header_page()
	generate_current_bet_round_detail_page()
	generate_index_page()
	push_page()


db.init_db()
generate_index_page()
