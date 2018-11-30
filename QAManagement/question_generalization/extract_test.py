# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 9:51
# @Author  : wb
# @File    : extract_test.py

# import os
# from pyltp import Segmentor
# from pyltp import Postagger
# # 抽取的测试文件
# # 导入LTP的文件
# LTP_DATA_DIR = '../data/ltp_data'  # ltp模型目录的路径
#
# # 分词
# cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
# segmentor = Segmentor()  # 初始化实例
# segmentor.load_with_lexicon(cws_model_path, '../data/new_dictionary.txt')  # 加载模型，第二个参数是您的增量模型路径
#
# # 词性标注
# pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
# postagger = Postagger()  # 初始化实例
# postagger.load(pos_model_path)  # 加载模型
#
# # 分类的疑问词
# # 多久 how-long
# how_long = ['多长时间', '多少时间', '多久']
# # 多少 how-much
# how_much = ['多少', '几']
# # 地点 where
# where = ['什么地方', '什么地点', '哪里', '何处', '哪个地方']
# # 方式 how_do
# how_do = ['怎样', '怎么', '怎么样', '如何', '哪些方法', '哪些方式', '哪些途径', '何种方法', '什么方法', '什么方式', '什么途径']
# # 人物 who
# who = ['什么人', '谁', '哪个人', '何人', '哪些人', '哪一个人']
# # 时间 when
# when = ['什么时间', '什么时候', '何时', '哪个时候']
# # 原因 why
# why = ['什么原因', '哪些原因', '什么因素', '哪些因素', '为什么', '为何']
# # 是否类 yes_no
# yes_no = ['能', '能够', '会可', '可能', '可以', '有', '是']
# # 定义类
# definition = ['是什么', '什么是']
# # 列表类 list_ques
# list_ques = ['哪些', '有什么', '有哪些', '有啥']
# # 哪个 which
# which = ['哪个', '哪']
# # 正常疑问句
# common_ques = ['什么']
# # 疑问语气词
# modal = ['吗', '呢', '吧', '么', '嘛']
#
# question = '这个游戏玩的人多么？'
# words = segmentor.segment(question)  # 分词
# words_list = list(words)
#
# postags = postagger.postag(words_list)  # 词性标注
# postags_list = list(postags)
#
# print(words_list)
# print(postags_list)
#
# segmentor.release()  # 释放模型
# postagger.release()  # 释放模型

from QAManagement.question_generalization.extract import Extract

extract = Extract()

question = 'cad为什么打开图形后文字都是问号？'
# type = 'why'
#
# result = extract.Pretreate(question,type)
# print(result)
#
# result1 = extract.compression(result[1])
# print(result1)

# extract.savedb(['1','2'],['a','b'],'how_long')
extract.main(question=question)
