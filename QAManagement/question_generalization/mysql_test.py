# -*- coding: utf-8 -*-
# @Time    : 2018/8/15 22:12
# @Author  : wb
# @File    : mysql_test.py

# 测试数据库

from mysqldb_helper import SQLHelper

helper = SQLHelper(host=SQLHelper.host,user=SQLHelper.username,pwd=SQLHelper.password,db=SQLHelper.database)

sql = "SELECT * FROM common_ques WHERE question= '主卡 和 副卡 的 号码 有 什么 区别 ？'"
model_words_list = []
model_postags_list = []
model_arcs_list = []
result = helper.ExecQuery(sql)
for res in result:
    model_words_list.append(res[1].split())
    model_postags_list.append(res[2].split())
    model_arcs_list.append(res[3].split())
    # print(i[3])
print(model_words_list)
print(model_postags_list)
print(model_arcs_list)
model_list = model_words_list + model_postags_list + model_arcs_list
print(model_list[2])