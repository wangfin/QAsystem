# -*- coding: utf-8 -*-
# @Time    : 2018/8/17 10:27
# @Author  : wb
# @File    : 依存句法分析.py

# 使用依存句法分析句子结构

import os
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser

LTP_DATA_DIR = '../data/ltp_data'  # ltp模型目录的路径

# 分词
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
segmentor = Segmentor()  # 初始化实例
segmentor.load_with_lexicon(cws_model_path, '../data/new_dictionary.txt') # 加载模型，第二个参数是您的增量模型路径

# 词性标注
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
postagger = Postagger() # 初始化实例
postagger.load(pos_model_path)  # 加载模型

# 依存句法分析
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
parser = Parser() # 初始化实例
parser.load(par_model_path)  # 加载模型

line = '淘宝自动确认时间是多久？'

words = segmentor.segment(line)# 分词
print(' '.join(words))
words_list = list(words)

postags = postagger.postag(words_list)  # 词性标注
postags_list = list(postags)
print('\t'.join(postags))

arcs = parser.parse(words_list, postags_list)  # 句法分析
print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
arcs_list = list(arcs)