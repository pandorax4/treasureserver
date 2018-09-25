"""
1. 主页（三个页面，small, big, large）
2. 规则页面（1个页面）
3. 所有历史游戏界面（列表形式，每轮游戏一行，只包含具体页面的页头信息）（三个页面，small, big, large)
4. 每轮游戏具体页面（每轮游戏一个页面，small, big, large 显示在同一个页面
5. 当前游戏下注页面（未结算的）
"""

import db

view_root = "../"


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


# 生成小赌注主页（附带当前轮未结算信息）
def generate_small_bet_index_page():
    pass


# 生成中赌注主页（附带当前轮未结算信息）
def generate_big_bet_index_page():
    pass


# 生成大赌注主页（附带当前轮未结算信息）
def generate_large_bet_index_page():
    pass


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
    generate_small_bet_index_page()
    generate_big_bet_index_page()
    generate_large_bet_index_page()
    push_page()



