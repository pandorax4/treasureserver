import util

url = "https://aiodex.com/exchange/fetch-data"


result = util.http_post_request(url, "")
print(result)