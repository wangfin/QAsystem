# -*- coding: utf-8 -*-
# @Time    : 2018/8/15 22:40
# @Author  : wb
# @File    : generate_test.py

# 生成测试

from QAManagement.question_generalization.generate import Generate

generate = Generate()

result = generate.main('小米6在使用过程中有什么问题吗？')

print(result)
#
# input = [{'aaaa':9},{'bbbb':2},{'cccc':10},{'dddd':4},{'eeee':5},{'ffff':6},{'gggg':7}]
#
# result = generate.topnum(input,3)
#
# print(result)

# for i in input:
#     print(list(i.values())[0])

# print(list(input[2].values())[0]) list(subtitle.keys())[0]

# input.sort(key=lambda k: list(k.values())[0], reverse=True)
#
# print(input)

# line = 'a b c d e f g h i j k l'
# line2 = 'n m l o p '
# sen = []
# sen2 = []
# x1 = sen.append(line.split())
# x2 = sen2.append(line2.split())
# print(sen)
# print(sen2)
# print(sen + sen2)

# x1 = 'sadasdad'
# x2 = 'a b c d e f g h i j k l'.split()
# sen = [x1,x2]
# print(sen[0])