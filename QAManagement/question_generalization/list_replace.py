# -*- coding: utf-8 -*-
# @Time    : 2018/8/29 22:39
# @Author  : wb
# @File    : list_replace.py

# list切片替换

listA = ['你','好','真的','么','么？']
listB = ['1','2','3','4','5','6','7']

listA[2:4] = listB[1:3]
print(listA)