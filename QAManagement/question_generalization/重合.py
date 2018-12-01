# -*- coding: utf-8 -*-
# @Time    : 2018/8/29 13:07
# @Author  : wb
# @File    : 重合.py

# 查看重复

ques_arc = {'id': 6, 'cont': '有', 'pos': 'v', 'ne': 'O', 'parent': -1, 'relate': 'HED', 'semparent': -1, 'semrelate': 'Root', 'arg': [{'id': 0, 'type': 'A0', 'beg': 1, 'end': 1}, {'id': 1, 'type': 'LOC', 'beg': 2, 'end': 5}, {'id': 2, 'type': 'A1', 'beg': 7, 'end': 8}], 'sem': [{'id': 0, 'parent': -1, 'relate': 'Root'}]}
model_arc = {'id': 6, 'cont': '有', 'pos': 'v', 'ne': 'O', 'parent': -1, 'relate': 'HED', 'semparent': -1, 'semrelate': 'Root', 'arg': [{'id': 0, 'type': 'A0', 'beg': 1, 'end': 1},  {'id': 1, 'type': 'A1', 'beg': 5, 'end': 7}], 'sem': [{'id': 0, 'parent': -1, 'relate': 'Root'}]}

# list_c = [a for a in ques_arc['arg'][i] for i in range(len(ques_arc['arg'])) if a in model_arc['arg'][j]  for j in range(len(model_arc['arg']))]
#
# print(list_c)

# 查看两个的数量即可
for ques in ques_arc

