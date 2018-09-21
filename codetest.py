import rpcapi as api
import util

usnpent_txid_list = [
    "3cbf1974629c1320fba2cf94d44779334addd70a5e7b767109b2f696b7a19038",
    "1dcfebc4f6a8c5b8468ff5d97d39fc3f9b24abea34660f853eba46c97bca7c54",

]


"""
1. 获取同一个区块的输入，按txid做一下排序
2. 把每一个区块排好序的输入加入到匹配系统
3. 
"""


""" 
# 获取所有区块的 Nonce 值，写到 nonces.txt文件中
curr_block_height = api.get_current_block_height()

nonce_list = []

for h in range(curr_block_height):
    height, nonce, timestamp = api.get_block_height_nonce_timestamp_by_height(h)
    # print(height, nonce, timestamp)
    nonce_list.append(nonce)


with open("nonces.txt", "w") as f:
    for nonce in nonce_list:
        f.write("{}\n".format(nonce))

print("BlockHeight: ", curr_block_height)
print("Nonce Count: ", len(nonce_list))
"""

"""
游戏玩法：
1. 猜大小
"""


nonce_list = []
last_digit_dict = {}

for x in range(10):
    last_digit_dict[x] = 0

with open("nonces.txt", "r") as f:
    for snonce in f:
        snonce = snonce.strip()
        nonce_list.append(snonce)

for nonce in nonce_list:
    last_digit = int(nonce[-1])
    last_digit_dict[last_digit] += 1

nonce_count = len(nonce_list)

for ld in last_digit_dict:
    count = last_digit_dict[ld]
    percentage = util.get_precision((count / nonce_count) * 100, 2)
    print(ld, count, percentage)

