import time
import json

def get_current_strtime():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def log(log_str):
    sys_time = get_current_strtime()
    slog = '[{0}] {1}'.format(sys_time, log_str)
    print(slog)


def get_format_json(data):
    try:
        json_str = json.dumps(data, indent=4,separators=(',',':'))
        return json_str
    except:
        log('get fromat json error: {}'.format(data))
        return ''


def timestamp2localtime(timestamp):
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime   # 2013-10-10 23:40:00


def timestamp2utctime(timestamp):
    dateArray = datetime.datetime.utcfromtimestamp(timestamp)
    otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
    return otherStyleTime   # 2013-10-10 15:40:00