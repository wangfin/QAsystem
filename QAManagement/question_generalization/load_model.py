# -*- coding: utf-8 -*-
# @Time    : 2018/8/15 9:41
# @Author  : wb
# @File    : load_model.py

# 读取事先下载的词向量

# 用gensim打开glove词向量需要在向量的开头增加一行：所有的单词数 词向量的维度
import gensim
import os
import shutil
from sys import platform

class Load():

    # 计算行数，就是单词数
    def getFileLineNums(self,filename):
        f = open(filename, 'r')
        count = 0
        for line in f:
            count += 1
        return count


    # Linux或者Windows下打开词向量文件，在开始增加一行
    def prepend_line(self,infile, outfile, line):
        with open(infile, 'r') as old:
            with open(outfile, 'w') as new:
                new.write(str(line) + "\n")
                shutil.copyfileobj(old, new)


    def prepend_slow(self,infile, outfile, line):
        with open(infile, 'r') as fin:
            with open(outfile, 'w') as fout:
                fout.write(line + "\n")
                for line in fin:
                    fout.write(line)


    def load(self,filename):
        num_lines = self.getFileLineNums(filename)
        gensim_file = '/home/wang/data/chinese_model.txt'
        gensim_first_line = "{} {}".format(num_lines, 300)
        # Prepends the line.
        if platform == "linux" or platform == "linux2":
            self.prepend_line(filename, gensim_file, gensim_first_line)
        else:
            self.prepend_slow(filename, gensim_file, gensim_first_line)

        model = gensim.models.KeyedVectors.load_word2vec_format(gensim_file)


if __name__ == "__main__":
    load = Load()
    load.load('/home/wang/data/sgns.merge1.bigram.txt')


