# -*- coding: utf-8 -*-
# @Time    : 2018/7/26 21:37
# @Author  : wb
# @File    : word2vec.py

# 使用词向量
# 用gensim打开glove词向量需要在向量的开头增加一行：所有的单词数 词向量的维度
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from gensim.test.utils import datapath
import os
import shutil
import hashlib
from sys import platform


# 计算行数，就是单词数
# def getFileLineNums(filename):
#     f = open(filename, 'r')
#     count = 0
#     for line in f:
#         count += 1
#     return count
#
#
# # Linux或者Windows下打开词向量文件，在开始增加一行
# def prepend_line(infile, outfile, line):
#     with open(infile, 'r') as old:
#         with open(outfile, 'w') as new:
#             new.write(str(line) + "\n")
#             shutil.copyfileobj(old, new)
#
#
# def prepend_slow(infile, outfile, line):
#     with open(infile, 'r') as fin:
#         with open(outfile, 'w') as fout:
#             fout.write(line + "\n")
#             for line in fin:
#                 fout.write(line)
#
#
# def load(filename):
#     num_lines = getFileLineNums(filename)
#     gensim_file = 'glove_model.txt'
#     gensim_first_line = "{} {}".format(num_lines, 300)
#     # Prepends the line.
#     if platform == "linux" or platform == "linux2":
#         prepend_line(filename, gensim_file, gensim_first_line)
#     else:
#         prepend_slow(filename, gensim_file, gensim_first_line)
#
#     model = gensim.models.KeyedVectors.load_word2vec_format(gensim_file)

# 导入已经生成好的词向量
#text_model = Word2Vec.load("../data/sgns.merge.bigram.txt")
wv_from_text = KeyedVectors.load_word2vec_format(datapath('/home/wang/data/sgns.merge.bigram.txt'), binary=False)  # C text format

print(wv_from_text.wv.most_similar(positive=['爱情']))
