import requests
import json
import time
import threading
from win10toast import ToastNotifier

mn_account = {
    "mn01": "GaZVcUBuuMPbdqhf6uoR85vkVXYPfcpiLK",
    "mn02": "GXLshmx6SRxm42D6Yj7Q39hsKLECnbJa8j",
    "mn04": "GLBcgHz9d92NiTxbppxCjC9cVrbTSRwdn5",
    "bwgmn-01": "GZ8rAhufMuzpPSKJhbSdsw1oB4nijxf2xY",
    "bwgmn-02": "GVjty31houVCijpAa8dA7s9iTeh1GLe8m2",
    "bwgmn-03": "GcBQbMMiAJLQREJTb5dxiaoE9xb9zC7aGk",
    "bwgmn-04": "GMxarpujzzmuX6zPMPdqGk9T2HYES9sr6M",
    "bwgmn-05": "GPfqqgfdrZN3NbSfCV8AvBgPQsDuB96g5K",
    "bwgmn-06": "GJYCnCktRm2LeWjR279CKBWp6ZQihja9LU",
    "bwgmn-07": "GS87Ggfm6FE7zA5KyG6APDR1awbYXCNw1W",
    "bwgmn-08": "GbtAhr5kBRYze9UqxYd7kidihWtLD5FnHF",
    "bwgmn-09": "GaE4E3M99SDGhXQrvvc25w5fQWEybcRnS9",
    "bwgmn-10": "GcP2uas9ySoyEqXsKSryaNy6twcvHwPCVA",
    "bwgmn-11": "GZGhVvY7JMjAh7HnK7g5ijGmXBpUpiomjp",
    "bwgmn-12": "Gf83jCX6dTWxmZSAHULuqmurzourt934FK",
    "bwgmn-13": "GMeNfi3qappP9BPpTd83PHhccVDoqdrPye",
    "bwgmn-14": "GNBrYAKRRUKnJQastFogH9kabDKAicPTfk",
    "bwgmn-15": "GK1H6wW2m6EB6s4NKEQNb38YZ5wvzF82nF",
    "bwgmn-16": "GejYT48Vh7z9u1BEKLy3ZMXnGWEY38JrkM",
    "bwgmn-17": "GcJT8tNZ2w5p5JqPEV19THDvssmiNLMWAt",
    "bwgmn-18": "Gfoeg98W9dvDSj5hgCwDY6P8v1QKBiGPa8",
    "bwgmn-19": "GU6NFm51bBZw1YD3YdrzrdjzNuLbmwqWcb",
    "bwgmn-20": "GLKZNvtzPpcwoxtZJzSC2Aqdbk9bztT6TV",
    "bwgmn-21": "GbhZZhnCy9MxAk5HTFVHoHYaTrXyqdfb1G",
    "bwgmn-22": "GZarexPeeTcmRmdbHnUieyB45fJd1qEFzt",
    "bwgmn-23": "GZZw8rJ6saQUy7Ab4uqK3ZySXcByAaQCLF",
    "bwgmn-24": "GJ6ffV1JeXZjuFpjv5gf9jDCgyAQeUYtKH",
    "bwgmn-25": "GN3TMjq7dUL85DjSZ9qDtFBpKgWurscZE8",
    "bwgmn-26": "GLq1fgUhJbPozzEGuqUh9T2ZjzE5aCCQ4M",
    "bwgmn-27": "GPHugSV1Un7LisT6NpGni7NfiRBd7ahbVv",
    "bwgmn-28": "GRY83V1iBJiJzAyk8CGK4uAv9tZJbS6Dzc",
    "bwgmn-29": "GPwM1EAvr26uZCbPSP4U3sbLxS9ztnHi1E",
    "bwgmn-30": "Gbze4n1MunTKgY2U9FrJY5FRmE1bcwrPVP",
    "bwgmn-31": "GLR28TiPBHHQavVD4pAzApcs2saSr9Aawj",
    "bwgmn-32": "GLTvYMm9EpVcZzRSAMjJAaV4shsWZz4jqH",
    "bwgmn-33": "GPzFtQH22TxxSKSFnbQxhmnWupz8GEAtxE",
    "bwgmn-34": "GP7GgJUCDLCGcM67K511n7u6tJHPNDAZz7",
    "bwgmn-35": "GbX9PvaCwLGuEsTiHoXcQyGWmHgKnBVVTG",
    "bwgmn-36": "GRUGqsBJudhcuP4B5XAWrVFZx8vRhCr2JT",
    "bwgmn-37": "GJZpnZ6YNcX1jDVueaambzNKjyYufXgbjJ",
}


def http_post_request(url, params, add_to_headers=None):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json;charset=UTF-8',
        "origin": "https://explorer.geekcash.org",
        "referer": "https://explorer.geekcash.org/address/GaZVcUBuuMPbdqhf6uoR85vkVXYPfcpiLK",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    if add_to_headers:
        headers.update(add_to_headers)

    postdata = json.dumps(params)

    response = requests.post(url, postdata, headers=headers, timeout=10)
    json_obj = json.loads(response.text)
    return json_obj['bl']


def get_balance(mn_name, address):
    balance = http_post_request("https://api.geekcash.org/address/info", params={'id': address})
    on_got_balance(mn_name, address, balance)


def on_got_balance(mn_name, address, balance):
    print(mn_name, address, balance, "reward: ", int(balance - 10000))
    global balance_dict
    balance_dict[mn_name] = int(balance - 10000)


def show_message(msg):
    toaster = ToastNotifier()
    toaster.show_toast("GeekCash Masternode", msg, duration=5)


balance_dict = {}
last_total_reward = -1

while True:
    try:
        threads = []
        for name in mn_account:
            address = mn_account[name]
            t = threading.Thread(target=get_balance, args=(name, address,))
            threads.append(t)

        for t in threads:
            t.setDaemon(True)
            t.start()

        for t in threads:
            t.join()

        reward = 0
        for key in balance_dict:
            reward += balance_dict[key]

        print("Total Reward: ", reward)
        if reward != last_total_reward:
            msg = ""
            if last_total_reward > 0:
                new_income = reward - last_total_reward
            else:
                new_income = 0
            last_total_reward = reward

            if new_income > 0:
                msg += "Total new income: {}\n".format(new_income)

            msg += "Total Reward: {}".format(reward)

            show_message(msg)
    except:
        pass
    time.sleep(2.0)


