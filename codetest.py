import rpcapi as api

txid = api.send_all_unspent_list_to_address("Gf5PDtLUq44sjRpFipFeq8Pzw3H2XK91By")
print(txid)