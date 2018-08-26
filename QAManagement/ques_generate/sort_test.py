# 取最大最小值测试

data = [{'date': '2018-08-16', 'weekday': '周四', 'num': 0}, {'date': '2018-08-17', 'weekday': '周五', 'num': 0}, {'date': '2018-08-18', 'weekday': '周六', 'num': 1}, {'date': '2018-08-19', 'weekday': '周日', 'num': 1}, {'date': '2018-08-20', 'weekday': '周一', 'num': 3}, {'date': '2018-08-21', 'weekday': '周二', 'num': 0}, {'date': '2018-08-22', 'weekday': '周三', 'num': 0}, {'date': '2018-08-23', 'weekday': '周四', 'num': 0}]

data.sort(key=lambda k:list(k.values())[2],reverse=True)
print(data)
data.sort(key=lambda k:list(k.values())[0],reverse=False)
print(data)
# print(max(data))
