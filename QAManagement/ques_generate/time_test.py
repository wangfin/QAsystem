# 时间测试函数
import datetime
import time

def get_weeks_before_tody(n=0):
    '''''
    date format = "YYYY-MM-DD HH:MM:SS"
    '''
    now = datetime.datetime.now()
    if(n<0):
        return datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
    else:
        n_days_before = now - datetime.timedelta(days=n * 7)
        return datetime.datetime(n_days_before.year, n_days_before.month, n_days_before.day, n_days_before.hour, n_days_before.minute, n_days_before.second)

result = get_weeks_before_tody(1)
print(result)
