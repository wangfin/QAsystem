# -*- coding: utf-8 -*-
# @Time    : 2018/8/18 17:10
# @Author  : wb
# @File    : tree_test.py

# 构建树的测试类
from templatetree import Templatetree

templatetree = Templatetree()



import os
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser

# LTP_DATA_DIR = '../data/ltp_data'  # ltp模型目录的路径
#
# # 分词
# cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
# segmentor = Segmentor()  # 初始化实例
# segmentor.load_with_lexicon(cws_model_path, '../data/new_dictionary.txt') # 加载模型，第二个参数是您的增量模型路径
#
# # 词性标注
# pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
# postagger = Postagger() # 初始化实例
# postagger.load(pos_model_path)  # 加载模型
#
# # 依存句法分析
# par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
# parser = Parser() # 初始化实例
# parser.load(par_model_path)  # 加载模型
#
# line = '小米6在使用过程中有什么问题吗？'
#
# words = segmentor.segment(line)# 分词
# print(' '.join(words))
# words_list = list(words)
#
# postags = postagger.postag(words_list)  # 词性标注
# postags_list = list(postags)
# print('\t'.join(postags))
#
# arcs = parser.parse(words_list, postags_list)  # 句法分析
# print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
# arcs_list = []
#
# for arc in arcs:
#     arcs_list.append(str(arc.head) + ':' + str(arc.relation))
# print(arcs_list)

ques_words_list = '数据 存储 在 DIS 和 OBS 有什么 区别 ？'.split()
ques_postags_list = 'n v p ws c ws list_ques n wp'.split()
ques_arcs_list = '2:SBV 0:HED 2:CMP 7:ATT 6:LAD 4:COO 3:POB 2:VOB 2:WP'.split()


model_words_list = 'redis 和 memcache 有 哪些 区别 ？'.split()
model_postags_list = 'ws c ws modal list_ques n wp'.split()
model_arcs_list = '4:SBV 3:LAD 1:COO 0:HED 6:ATT 4:VOB 4:WP'.split()


ques_tree = templatetree.create(words_list=ques_words_list,postags_list=ques_postags_list,arcs_list=ques_arcs_list)
model_tree = templatetree.create(words_list=model_words_list,postags_list=model_postags_list,arcs_list=model_arcs_list)

print(ques_tree)
print(model_tree)

print(templatetree.depth_first(ques_tree))
print(templatetree.depth_first(model_tree))
# ques_str = templatetree.depth_first(ques_tree)
# model_str = templatetree.depth_first(model_tree)

templatetree.matchandgenerate(question_tree=ques_tree,model_tree=model_tree)