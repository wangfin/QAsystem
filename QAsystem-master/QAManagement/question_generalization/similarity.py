# -*- coding: utf-8 -*-
# @Time    : 2018/8/15 9:35
# @Author  : wb
# @File    : similarity.py

# 使用gensim计算句子相似度


import numpy as np
from gensim.models import word2vec,KeyedVectors
from gensim import corpora, models, similarities
import math

class Similarity():

    w2v = KeyedVectors.load_word2vec_format('../data/chinese_model.txt',limit=500000)

    # 将输入的list转换成句向量
    def sent2vec(self,sen_list):
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


    # 计算余弦夹角
    def cos_dist(self,a, b):
        if len(a) != len(b):
            return None
        part_up = 0.0
        a_sq = 0.0
        b_sq = 0.0
        for a1, b1 in zip(a, b):
            part_up += a1 * b1
            a_sq += a1 ** 2
            b_sq += b1 ** 2
        part_down = math.sqrt(a_sq * b_sq)
        if part_down == 0.0:
            return None
        else:
            return part_up / part_down

    # 运行主函数，输入问句，模板问句list
    def main(self,question_list,model_list):

        # 输入需要泛化的问句
        # 输入在泛化数据库中的模板
        # 从数据库模板中找出与question最相近的10个句子
        # 使用这10个句子的模板进行泛化

        questionvec = self.sent2vec(question_list)

        result = []

        for model in model_list:
            # print(model)
            modelvec = self.sent2vec(model)
            # 显示分数的dict
            score = {}

            model_ques = ''

            for i in model:
                model_ques = model_ques + i + ' '

            # print(model_ques)

            score[model_ques] = self.cos_dist(questionvec,modelvec)
            result.append(score)

            # 输出形式 {model:score}

        return result
