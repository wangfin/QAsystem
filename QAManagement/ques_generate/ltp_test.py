# -*- coding: utf-8 -*-
# @Time    : 2018/7/27 15:44
# @Author  : wb
# @File    : ltp_test.py

# 测试LTP云的

import os
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
import json
import re
from LTML import LTML
import requests

# 初始化的时候调用LTP的模型
LTP_DATA_DIR = '../data/ltp_data'  # ltp模型目录的路径

# 分词
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
segmentor = Segmentor()  # 初始化实例
segmentor.load_with_lexicon(cws_model_path, '../data/new_dictionary.txt')  # 加载模型，第二个参数是您的增量模型路径

line = '购买数据调度服务'
words = segmentor.segment(line)  # 分词
words_list = list(words)
print(words_list)

# LTML用于构建自定义分词的xml，用于向LTP云传入args
ltml = LTML()
ltml.build_from_words(words_list)
xml = ltml.tostring()
# print(xml)

url_get_base = "https://api.ltp-cloud.com/analysis/"

# 这个是加入自定义词典的参数
args = {
    'api_key': 'a1R923E7s37daeNz7dsMeXiTexWGoookJX2HONwC',
    'pattern': 'all',
    'format': 'json',
    'xml_input': 'true',
    'text': xml
}

r = requests.post(url_get_base, data=args)

print("r的值："+ r.text)

content = r.json()

print(content)

for i in content[0][0]:
    print(i)




