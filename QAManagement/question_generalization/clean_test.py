# -*- coding: utf-8 -*-
# @Time    : 2018/8/11 16:20
# @Author  : wb
# @File    : clean_test.py

# pyltp的分句检测
from pyltp import SentenceSplitter
sents = SentenceSplitter.split('蚂蚁借呗提前还款还要付利息吗?具体怎么算')  # 分句
print('\n'.join(sents))
print(len(sents))