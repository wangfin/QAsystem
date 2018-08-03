# -*- coding: utf-8 -*-
# @Time    : 2018/7/26 10:49
# @Author  : wb
# @File    : test_title.py

import os
from pyltp import SementicRoleLabeller
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
import json
import re

# 初始化的时候调用LTP的模型
LTP_DATA_DIR = '../data/ltp_data'  # ltp模型目录的路径

# 分词
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
segmentor = Segmentor()  # 初始化实例
segmentor.load_with_lexicon(cws_model_path, '../data/new_dictionary.txt')  # 加载模型，第二个参数是您的增量模型路径

# 词性标注
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
postagger = Postagger()  # 初始化实例
postagger.load(pos_model_path)  # 加载模型

# 依存句法分析
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
parser = Parser()  # 初始化实例
parser.load(par_model_path)  # 加载模型

# 读取疑问词
ques_word_file = open('../data/question_word.txt')
ques_words_list = []
for line in ques_word_file:
    ques_words_list.append(line.strip('\n'))

# 读取抽取好的json文件
# 遍历上传的文件夹中所有的文件
# 还需要判断上传的是文件夹目录还是文件
path = "../data/notable" #文件夹目录
files= os.listdir(path) #得到文件夹下的所有文件名称
urls = []
for file in files: #遍历文件夹
     if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
          urls.append(path+"/"+file)
#print(urls) #打印结果
print(len(urls))

is_question_title = False

for url in urls:
    QA_dict = {}
    file = open(url)
    for line in file.readlines():
        dic = json.loads(line)

        # json_all.append(dic)  # 全部的json存入一个数组

        # 抽出文件的标题
        title = dic['title'].strip().strip("\n")  # 对title的格式进行处理，去掉空格和换行
        if title == '':  # 文章的标题可能因为一些关系没有抽取出来
            if len(dic['subject']) > 0:
                title = dic['subject'][-1].strip().strip("\n")

        # 1.对标题的判断，判断他是疑问句还是普通的名词
        # 2.将疑问句和他的标题内容直接存入QA对中
        # 3.对还是名词的词进行更加高级的处理

        # 对title进行分类，有些title是名词，有些是疑问句
        words = segmentor.segment(title)  # 分词
        words_list = list(words)
        # 根据疑问词判断这句话是不是疑问句，但是有些疑问句中没有用到疑问词，于是就使用最末尾的 ？做判断
        for i in words_list:
            if i in ques_words_list or i == '？' or i == '?':
                is_question_title = True
                break  # 一旦有一个判断出了True直接跳出循环
            else:
                is_question_title = False

        if not is_question_title:  # 如果是陈述句
            print(url)
            words = segmentor.segment(title)  # 分词
            print(' '.join(words))
            words_list = list(words)

            postags = postagger.postag(words_list)  # 词性标注
            postags_list = list(postags)
            print('\t'.join(postags))

            arcs = parser.parse(words_list, postags_list)  # 句法分析
            print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

            if 'subject' in dic.keys() and len(dic['subject']) > 0:
                print(dic['subject'])
            #common_json.append(dic)

            num_subtilte = 0  # subtilte的个数
            pattern = re.compile(r'subtitle')

            # 获取该文档中的subtitle的个数
            for keys in dic.keys():
                if len(pattern.findall(keys)) != 0:
                    num_subtilte += 1
            #print(url+":"+str(num_subtilte))

            # subtitles = []
            if num_subtilte > 0:
                for num in range(num_subtilte):
                    # subtitle = common_json[i]['subtitle' + str(num + 1)]
                    subtitle = re.sub(r'<.*?>', '', dic['subtitle' + str(num + 1)].strip())
                    print(subtitle)
                    # subtitles.append(subtitle)




            print("*********************************************************")




