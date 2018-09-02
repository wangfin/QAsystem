# -*- coding: utf-8 -*-
# @Time    : 2018/8/27 15:55
# @Author  : wb
# @File    : cluster.py
import json

from gensim.models import KeyedVectors
import numpy as np
import pandas as pd
from gensim.similarities import Similarity

from QAManagement.ques_new.kmeans import KMeansClassifier
import os
import matplotlib.pyplot as plt

# 文本聚类算法
# 导入文本段，对文本进行分类
# 几类具有特殊性质的文本
# 操作步骤 等

# 1.读入数据，将文本转换成词向量
class Cluster():

    # w2v = KeyedVectors.load_word2vec_format('../../data/chinese_model.txt', limit=500000)

    # 1.将输入的list转换成句向量
    def sent2vec(self, sen_list):
        words = sen_list
        M = []
        for w in words:
            try:
                M.append(Similarity.w2v.wv[w])
            except:
                continue
        M = np.array(M)
        v = M.sum(axis=0)

        return v / np.sqrt((v ** 2).sum())

    # 2.对词向量进行聚类
    # def run(self):
    #     # 首先读入数据进行训练分类
    #     path = "../data/notable"  # 文件夹目录
    #     files = os.listdir(path)  # 得到文件夹下的所有文件名称
    #     urls = []
    #     for file in files:  # 遍历文件夹
    #         if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
    #             urls.append(path + "/" + file)
    #
    #     # print(urls) # 打印结果
    #     # print(len(urls))
    #     # print(urls[101])
    #     # paths = [urls[101]]
    #
    #     if len(urls) > 0:
    #         for path in urls:
    #             # print(path)
    #             file = open(path)
    #             for line in file.readlines():
    #                 dic = json.loads(line)
    #
    #                 print(dic)
    #
    #                 if dic['titlecontent'] != '':

    # 加载数据集，DataFrame格式，最后将返回为一个matrix格式
    def loadDataset(self,infile):
        df = pd.read_csv(infile, sep='\t', header=0, dtype=str, na_filter=False)
        return np.array(df).astype(np.float)

    # 聚类
    def classifier(self):
        data_X = self.loadDataset("testSet")
        k = 3
        clf = KMeansClassifier(k)
        clf.fit(data_X)
        cents = clf._centroids
        labels = clf._labels
        sse = clf._sse
        colors = ['b', 'g', 'r', 'k', 'c', 'm', 'y', '#e24fff', '#524C90', '#845868']
        for i in range(k):
            index = np.nonzero(labels == i)[0]
            x0 = data_X[index, 0]
            x1 = data_X[index, 1]
            y_i = i
            for j in range(len(x0)):
                plt.text(x0[j], x1[j], str(y_i), color=colors[i], \
                         fontdict={'weight': 'bold', 'size': 6})
            plt.scatter(cents[i, 0], cents[i, 1], marker='x', color=colors[i], \
                        linewidths=7)

        plt.title("SSE={:.2f}".format(sse))
        plt.axis([-7, 7, -7, 7])
        outname = "k_clusters" + str(k) + ".png"
        plt.savefig(outname)


