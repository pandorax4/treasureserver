import sys
import time
from old import datacenter

update_block_list = []


def commit_to_github():
    pass


def generate_json(bet_block_height, dbbet_list):
    pass


def update_json_to_view(block_height):
    print('Update: ', block_height)


def update_view():
    if len(sys.argv) > 1:
        datacenter.init_db()
        block_list_str = sys.argv[1]
        for str_block in block_list_str.split(','):
            block_height = int(str_block)
            update_block_list.append(block_height)

        for block in update_block_list:
            dbbet_block_list = datacenter.get_bet_block_list(block)
            generate_json(block, dbbet_block_list)

        datacenter.close_db()

        for block in update_block_list:
            update_json_to_view(block)

        commit_to_github()


if __name__ == '__main__':
    time.sleep(2)
    update_view()
