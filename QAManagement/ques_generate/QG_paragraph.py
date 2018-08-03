# -*- coding: utf-8 -*-
# @Time    : 2018/7/25 21:12
# @Author  : wb
# @File    : QG_paragraph.py

# 本文件是用来生成标题的问题的
# 首先分为两大类：标题就是问题的；标题是正常短语的

import os
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
import json
import re
from .LTML import LTML
import requests


class Paragraph(object):

    """
        第一类：标题就是问句的
        这里面也分几种情况
        句子以问号结尾的（中文问号？，英文问号?）都算
        另一种是问句，但没有以问号结尾
        这一种可以通过检查句子中是否有疑问词来判断
    """
    # # 初始化的时候调用LTP的模型
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
    # # 依存句法分析
    # par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
    # parser = Parser()  # 初始化实例
    # parser.load(par_model_path)  # 加载模型

    # 先进行自定义的分词
    LTP_DATA_DIR = '../data/ltp_data'  # ltp模型目录的路径
    cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
    segmentor = Segmentor()  # 初始化实例
    segmentor.load_with_lexicon(cws_model_path, '../data/new_dictionary.txt')  # 加载模型，第二个参数是您的增量模型路径

    # 读取疑问词
    ques_word_file = open('../data/question_word.txt')
    ques_words_list = []
    for line in ques_word_file:
        ques_words_list.append(line.strip('\n'))

    # 设置最后总输出的QA对
    QA_all = []

    # 特殊情况标注如下

    # 这些可以通过tf-idf来区分开

    # 可以表示内容的小标题 xxx是什么
    # '接口功能','功能介绍','功能描述','功能说明'
    content_subtitles = ['简介','概述','功能']

    # 可以表示动作的小标题 xxx如何
    action_subtitles = ['步骤']

    # 可以表示列表的小标题 xxx有哪些
    # '前置条件','注意事项'
    list_subtitles = ['条件','事项','场景','示例']

    # 表示无意义的title
    # 如果标题尤其中的某一类的话
    # 如果没有titlecontent，也没有subtitle，不生成QA
    # 如果下面的内容在上方的某一个中，那就是与上方的相同
    # 如果有titlecontent，那么就是xxx是什么，答案为titlecontent
    # 如果没有titlecontent，但是有subtitle，就与其他的subtitle的相同

    # 开发者工具中心没有subject的，所以直接使用subtitle
    meaningless_title = ['概述','开发者工具中心','附录','修订记录','简介']

    # 主函数，生成QA对的
    def main(self,paths):
        # 清空
        Paragraph.QA_all = []
        # 读取文件
        if len(paths) > 0:
            for path in paths:
                # print(path)
                # 本页面生成的QA
                page_qa = []
                file = open(path)
                for line in file.readlines():
                    dic = json.loads(line)

                    #Paragraph.json_all.append(dic)  # 全部的json存入一个数组

                    # 抽出文件的标题
                    title = dic['title'].strip().strip("\n")  # 对title的格式进行处理，去掉空格和换行
                    if title == '':  # 文章的标题可能因为一些关系没有抽取出来
                        if len(dic['subject']) > 0: # 那么就抽取subject的最后一个
                            title = dic['subject'][-1].strip().strip("\n")

                if self.Is_ask_type(title):  # 如果是疑问句
                    ques_qa = self.Ques_type_title(dic,title)
                    page_qa.extend(ques_qa)
                else:  # 如果不是疑问句
                    # 调用标题为正常的函数
                    phrase_qa = self.Phrase_type_title(dic,title)
                    subtitle_qa = self.Phrase_type_subtitle(dic,title)
                    page_qa.extend(phrase_qa)
                    page_qa.extend(subtitle_qa)

                # print(page_qa)
                Paragraph.QA_all.extend(page_qa)

            return Paragraph.QA_all
        else:
            return Paragraph.QA_all

    '''
        函数名：Ques_type_title
        作用：第一类的标题生成的QA对
        输入：dic,title
        输出：QA_dict
    '''
    def Ques_type_title(self,dic,title):

        ques_qa = []

        answer = ''
        QA_flag = None

        question = title
        content = dic['titlecontent'].strip()
        # 标题内容不为空
        if content != '':
            answer = content
            QA_flag = True
        # 标题内容为空
        else:
            if 'subject' in dic.keys() and (len(dic['subject']) > 0):
                # 取出该页面的所有的小标题
                subtitles = self.get_subtitle(dic)

                # 有小标题
                if len(subtitles) > 0:

                    for subtitle in subtitles:
                        answer = answer + subtitle[list(subtitle.keys())[0]] + ' '
                        QA_flag = True
                # 没有小标题
                else:
                    QA_flag = False
            # 没有subject
            else:
                QA_flag = False

        # 如果能够生成QA
        if QA_flag:
            # QA对的保存形式
            QA_dict = self.saveqa(question,answer,dic)

            ques_qa.append(QA_dict)

        return ques_qa

    '''
        函数名：Phrase_type_title
        作用：第二类的标题生成的QA对
        输入：dic,title
        输出：QA_dict
    '''
    def Phrase_type_title(self,dic,title):

        # 该类标题生成的所有的QA对
        phrase_qa = []

        # 1.首先还是先对标题分词
        words = Paragraph.segmentor.segment(title)  # 分词
        title_list = list(words)

        '''
            本来是需要这样考虑的，在全部的标题中，词性都可以划分成v+n
            但是这两种表达的语义不一样，一个是动词作定语修饰名词的 如 订阅操作，返回码，根据论文，发现这样的词在v和n之间加入的是没有关系的
            另一个是普通的动词+名词，现在需要把这两个分开来
            就只能假设里面有VOB的那就是普通的V+N，如果没有那就是第一种
        '''
        # 这个标记是用来标志VOB的
        VOB_flag = None

        # 这个是用来标记是否可以生成QA对的
        QA_flag = None

        question = ''
        answer = ''

        # 标题在那些无意义的词中
        if title in Paragraph.meaningless_title:
            if 'subject' in dic.keys() and (len(dic['subject']) > 0):

                question = dic['subject'][1] + '的' + dic['subject'][-3] + '是什么？'
                # QA_flag = True

                # 查看大标题下的内容是否为空
                if dic['titlecontent'].strip() == '':
                    # 那么就开始查看小标题
                    # 取出该页面的所有的小标题
                    subtitles = self.get_subtitle(dic)
                    # print(subtitles)
                    # 本页面有小标题
                    if len(subtitles) > 0:
                        for subtitle in subtitles:
                            # 判断subcontent是不是为空：
                            if dic[list(subtitle.keys())[0].replace('title', 'content')].strip() != '':
                                # 小标题先分词
                                subtitle_words = list(Paragraph.segmentor.segment(subtitle[list(subtitle.keys())[0]]))
                                # print(list(subtitle.keys())[0])
                                # 这个分类是VOB的，就是问如何操作的
                                # 所以如果有小标题能够表示操作的，那么这个小标题的下的内容就是答案
                                if len([i for i in subtitle_words if i in Paragraph.action_subtitles]) > 0:
                                    answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                    # 直接保存QA
                                    QA_dict = self.saveqa(question, answer, dic)
                                    phrase_qa.append(QA_dict)
                                    # QA_flag = True

                                # 如果是在表示内容的list中，那么问句也需要改变，改变成sub[1]+'的'+title是什么
                                elif len([i for i in subtitle_words if i in Paragraph.content_subtitles]) > 0:
                                    question = dic['subject'][1] + '中' + title + '是什么？'
                                    answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                    # 直接保存QA
                                    QA_dict = self.saveqa(question, answer, dic)
                                    phrase_qa.append(QA_dict)
                                    # QA_flag = True
                            # 没有小标题内容
                            else:
                                QA_flag = False

                    # 这种的是既没有标题内容，又没有小标题，这种的就算了，不生成QA对
                    else:
                        QA_flag = False
                else:
                    answer = dic['titlecontent'].strip()

                    # 直接保存QA
                    QA_dict = self.saveqa(question, answer, dic)
                    phrase_qa.append(QA_dict)

            # '开发者工具中心'
            else:
                # 不生成QA吧，烦人的
                QA_flag = False


        # 是正常的标题
        else:
            # 2.判断title中是否包含主题
            # 判断是否有subject
            if 'subject' in dic.keys() and (len(dic['subject']) > 0):

                # 首先判断sub的长度，如果小于7，那么使用常规操作
                # 算了，没什么意义，不用了
                #if len(dic['subject'] <= 7):


                # 对subject的第二级和倒数第二级也需要分词
                subject_firsttwo = list(Paragraph.segmentor.segment(dic['subject'][1]))
                #subject_lasttwo = list(Paragraph.segmentor.segment(dic['subject'][-2]))
                '''
                    这里本来还需要考虑一件事情，就是subject[1],subject[-2],标题（或者subject[-1]）进行三者融合
                    看怎样拼接能完全的表达语义，但我不知道怎么进行语义融合
                    所以只是制定了一个简单的规律
                    [-2]有可能是附录，这个没用
                    # 当subject的长度大于7的时候，那么最后的标题的语义有些很差（如概述），我们的拼接内容为[1],[-2],[-3]
                    当标题与[1]分词集合中有重复的时候，只用标题
                    当[-2]与标题有重复的时候，用[1]+标题
                    其实当标题与[-2]没有重复的时候，也有可能只使用[1]+标题就好了
                    主要是需要三个一起上的时候，我不知道怎么判断，就是[1]+[-2]+标题 
                '''

                result = self.ltp_request(title_list)

                for arc in result:
                    if arc['relate'] == 'VOB':  # 词里面有动宾关系，可以提问如何xxx
                        VOB_flag = True
                        # 只要有直接退出
                        break
                    else:
                        VOB_flag = False

                # 如果title中包含主题，那么在使用标题构建问句时
                # 不需要考虑再拼接主题了
                # 下面这个是求标题的list与sub[1]的list有没有交集，如果有，那就是只用标题表示就行
                if len([i for i in subject_firsttwo if i in title_list]) > 0:
                    # 不需要拼接主题

                    # 这里有VOB，是普通的v+n 如恢复密码
                    if VOB_flag:
                        # 如果不需要拼接主题的话，就直接使用这个标题就行
                        question = '如何'+title + '？'
                        # QA_flag = True

                        # 查看大标题下的内容是否为空
                        if dic['titlecontent'].strip() == '':
                            # 那么就开始查看小标题
                            # 取出该页面的所有的小标题
                            subtitles = self.get_subtitle(dic)
                            # 本页面有小标题
                            if len(subtitles) > 0:
                                for subtitle in subtitles:
                                    # 判断subcontent是不是为空：
                                    if dic[list(subtitle.keys())[0].replace('title', 'content')].strip() != '':
                                        # 小标题先分词
                                        subtitle_words = list(Paragraph.segmentor.segment(subtitle[list(subtitle.keys())[0]]))
                                        # print(subtitle_words)
                                        # 这个分类是VOB的，就是问如何操作的
                                        # 所以如果有小标题能够表示操作的，那么这个小标题的下的内容就是答案
                                        if len([i for i in subtitle_words if i in Paragraph.action_subtitles]) > 0:
                                            answer = dic[list(subtitle.keys())[0].replace('title','content')]

                                            # 直接保存QA
                                            QA_dict = self.saveqa(question, answer, dic)
                                            phrase_qa.append(QA_dict)
                                            # QA_flag = True
                                        # 如果是在表示内容的list中，那么问句也需要改变，改变成sub[1]+'的'+title是什么
                                        elif len([i for i in subtitle_words if i in Paragraph.content_subtitles]) > 0:
                                            question = title + '是什么？'
                                            answer = dic[list(subtitle.keys())[0].replace('title','content')]
                                            # print('运行一次')
                                            # 直接保存QA
                                            QA_dict = self.saveqa(question, answer, dic)
                                            phrase_qa.append(QA_dict)
                                            # QA_flag = True
                                    # 小标题没有内容
                                    else:
                                        QA_flag = False
                            # 这种的是既没有标题内容，又没有小标题，这种的就算了，不生成QA对
                            else:
                                QA_flag = False
                        else:
                            answer = dic['titlecontent'].strip()

                            # 直接保存QA
                            QA_dict = self.saveqa(question, answer, dic)
                            phrase_qa.append(QA_dict)

                    # 是名词 问句是 xxx是什么
                    else:
                        question = title + '是什么？'
                        # QA_flag = True
                        # 查看大标题下的内容是否为空
                        if dic['titlecontent'].strip() == '':
                            # 那么就开始查看小标题
                            # 取出该页面的所有的小标题
                            subtitles = self.get_subtitle(dic)
                            # 本页面有小标题
                            if len(subtitles) > 0:
                                for subtitle in subtitles:
                                    # 判断subcontent是不是为空：
                                    if dic[list(subtitle.keys())[0].replace('title', 'content')].strip() != '':
                                        # 小标题先分词
                                        subtitle_words = list(Paragraph.segmentor.segment(subtitle[list(subtitle.keys())[0]]))
                                        # 这个分类是名词的，所以问他表示名词的词

                                        # print(subtitle_words)

                                        if len([i for i in subtitle_words if i in Paragraph.content_subtitles]) > 0:
                                            answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                            # print(answer)

                                            # 直接保存QA
                                            QA_dict = self.saveqa(question, answer, dic)
                                            phrase_qa.append(QA_dict)
                                            # QA_flag = True

                                        # 所以如果有小标题能够表示操作的，那么这个小标题的下的内容就是答案
                                        # 如果是在表示动作的list中，那么问句也需要改变，改变成'如何'+title是什么
                                        elif len([i for i in subtitle_words if i in Paragraph.action_subtitles]) > 0:
                                            question = '如何' + title + '？'
                                            answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                            # 直接保存QA
                                            QA_dict = self.saveqa(question, answer, dic)
                                            phrase_qa.append(QA_dict)
                                            # QA_flag = True
                                    # 没有小标题内容
                                    else:
                                        QA_flag = False
                            # 这种的是既没有标题内容，又没有小标题，这种的就算了，不生成QA对
                            else:
                                QA_flag = False
                        else:
                            answer = dic['titlecontent'].strip()

                            # 直接保存QA
                            QA_dict = self.saveqa(question, answer, dic)
                            phrase_qa.append(QA_dict)


                # 如果没有交集，就是sub[1]+title
                else:
                    # 需要拼接主题

                    # 这里有VOB，是普通的v+n 如恢复密码
                    if VOB_flag:
                        # 如果不需要拼接主题的话，就直接使用这个标题就行
                        question = dic['subject'][1] + '中' + '如何' + title + '？'
                        # QA_flag = True

                        # 查看大标题下的内容是否为空
                        if dic['titlecontent'].strip() == '':
                            # 那么就开始查看小标题
                            # 取出该页面的所有的小标题
                            subtitles = self.get_subtitle(dic)
                            # 本页面有小标题
                            if len(subtitles) > 0:
                                for subtitle in subtitles:
                                    # 判断subcontent是不是为空：
                                    if dic[list(subtitle.keys())[0].replace('title', 'content')].strip() != '':
                                        # 小标题先分词
                                        subtitle_words = list(Paragraph.segmentor.segment(subtitle[list(subtitle.keys())[0]]))
                                        # 这个分类是VOB的，就是问如何操作的
                                        # 所以如果有小标题能够表示操作的，那么这个小标题的下的内容就是答案
                                        if len([i for i in subtitle_words if i in Paragraph.action_subtitles]) > 0:
                                            answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                            # 直接保存QA
                                            QA_dict = self.saveqa(question, answer, dic)
                                            phrase_qa.append(QA_dict)
                                            # QA_flag = True
                                        # 如果是在表示内容的list中，那么问句也需要改变，改变成sub[1]+'的'+title是什么
                                        elif len([i for i in subtitle_words if i in Paragraph.content_subtitles]) > 0:
                                            question = dic['subject'][1] + '的' + title + '是什么？'
                                            answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                            # 直接保存QA
                                            QA_dict = self.saveqa(question, answer, dic)
                                            phrase_qa.append(QA_dict)
                                            # QA_flag = True
                                    else:
                                        QA_flag = False
                            # 这种的是既没有标题内容，又没有小标题，这种的就算了，不生成QA对
                            else:
                                QA_flag = False
                        else:
                            answer = dic['titlecontent'].strip()

                            # 直接保存QA
                            QA_dict = self.saveqa(question, answer, dic)
                            phrase_qa.append(QA_dict)

                    # 是名词 问句是 xxx是什么
                    else:
                        question = dic['subject'][1] + '的' + title + '是什么？'
                        # QA_flag = True
                        # 查看大标题下的内容是否为空
                        if dic['titlecontent'].strip() == '':
                            # 那么就开始查看小标题
                            # 取出该页面的所有的小标题
                            subtitles = self.get_subtitle(dic)
                            # 本页面有小标题
                            if len(subtitles) > 0:
                                for subtitle in subtitles:
                                    # 判断subcontent是不是为空：
                                    if dic[list(subtitle.keys())[0].replace('title', 'content')].strip() != '':
                                        # 小标题先分词
                                        subtitle_words = list(Paragraph.segmentor.segment(subtitle[list(subtitle.keys())[0]]))
                                        # 这个分类是名词的，所以问他表示名词的词

                                        if len([i for i in subtitle_words if i in Paragraph.content_subtitles]) > 0:
                                            answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                            # 直接保存QA
                                            QA_dict = self.saveqa(question, answer, dic)
                                            phrase_qa.append(QA_dict)
                                            # QA_flag = True

                                        # 所以如果有小标题能够表示操作的，那么这个小标题的下的内容就是答案
                                        # 如果是在表示动作的list中，那么问句也需要改变，改变成'如何'+title是什么
                                        elif len([i for i in subtitle_words if i in Paragraph.action_subtitles]) > 0:
                                            question = dic['subject'][1] + '中' + '如何' + title + '？'
                                            answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                            # 直接保存QA
                                            QA_dict = self.saveqa(question, answer, dic)
                                            phrase_qa.append(QA_dict)
                                            # QA_flag = True
                                    # 没有小标题内容
                                    else:
                                        QA_flag = False
                            # 这种的是既没有标题内容，又没有小标题，这种的就算了，不生成QA对
                            else:
                                QA_flag = False
                        else:
                            answer = dic['titlecontent'].strip()

                            # 直接保存QA
                            QA_dict = self.saveqa(question, answer, dic)
                            phrase_qa.append(QA_dict)


            else:  # 没有subject，（或者有subject但是subject为空）不生成QA对
                QA_flag = False


        return phrase_qa


    '''
        函数名：Phrase_type_title
        作用：小标题生成的QA对
        输入：dic,title
        输出：QA_dict
    '''
    def Phrase_type_subtitle(self,dic,title):

        subtitle_qa = []

        QA_flag = None
        VOB_flag = None
        question = ''
        answer = ''

        title_list = list(Paragraph.segmentor.segment(title))

        # 大标题无意义
        if title in Paragraph.meaningless_title:
            if 'subject' in dic.keys() and (len(dic['subject']) > 0):
                # 取出该页面的所有的小标题
                subtitles = self.get_subtitle(dic)

                # 有小标题
                if len(subtitles) > 0:

                    for subtitle in subtitles:
                        # 判断subcontent是不是为空：
                        if dic[list(subtitle.keys())[0].replace('title', 'content')].strip() != '':

                            # 对小标题判断下是不是问句，这种情况极其罕见，但是遇见了，还是判断下吧
                            if self.Is_ask_type(subtitle[list(subtitle.keys())[0]]):
                                question = subtitle[list(subtitle.keys())[0]]
                                answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                # 直接保存QA
                                QA_dict = self.saveqa(question, answer, dic)
                                subtitle_qa.append(QA_dict)
                                # QA_flag = True

                            # 正常的小标题，都是单个词语
                            else:
                                # 小标题先分词
                                subtitle_words = list(Paragraph.segmentor.segment(subtitle[list(subtitle.keys())[0]]))
                                # 分词后看句法关系
                                result = self.ltp_request(subtitle_words)

                                for arc in result:
                                    if arc['relate'] == 'VOB':  # 词里面有动宾关系，可以提问如何xxx
                                        VOB_flag = True
                                        # 只要有直接退出
                                        break
                                    else:
                                        VOB_flag = False
                                # 表示句子中有VOB
                                if VOB_flag:

                                    # 小标题与标题有重复，可以覆盖
                                    if len([i for i in subtitle_words if i in title_list]) > 0:
                                        question = dic['subject'][1] + '中' + '如何' + subtitle[list(subtitle.keys())[0]] + '？'
                                        answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        # 这个是表示列表的词语
                                        if len([i for i in subtitle_words if i in Paragraph.list_subtitles]) > 0:
                                            question = dic['subject'][1] + '中' + '有哪些' + subtitle[list(subtitle.keys())[0]] + '？'
                                            answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        # 直接保存QA
                                        QA_dict = self.saveqa(question, answer, dic)
                                        subtitle_qa.append(QA_dict)
                                    # 没有重复
                                    # 因为此时的大标题是mingingless的，无意义，所以使用倒数第二个
                                    else:
                                        question = dic['subject'][1] + '中' + dic['subject'][-2] + '如何' + subtitle[list(subtitle.keys())[0]] + '？'
                                        answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        # 这个是表示列表的词语
                                        if len([i for i in subtitle_words if i in Paragraph.list_subtitles]) > 0:
                                            question = dic['subject'][1] + '中' + dic['subject'][-2] + '有哪些' + subtitle[list(subtitle.keys())[0]] + '？'
                                            answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        # 直接保存QA
                                        QA_dict = self.saveqa(question, answer, dic)
                                        subtitle_qa.append(QA_dict)
                                # 名词
                                else:
                                    # 小标题与标题有重复，可以覆盖
                                    if len([i for i in subtitle_words if i in title_list]) > 0:
                                        question = dic['subject'][1] + '中' + subtitle[list(subtitle.keys())[0]] + '是什么？'
                                        answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        # 直接保存QA
                                        QA_dict = self.saveqa(question, answer, dic)
                                        subtitle_qa.append(QA_dict)
                                        # QA_flag = True
                                        # 这个是表示列表的词语
                                        if len([i for i in subtitle_words if i in Paragraph.list_subtitles]) > 0:
                                            question = dic['subject'][1] + '中' + '有哪些' + subtitle[list(subtitle.keys())[0]] + '？'
                                            answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                            # 直接保存QA
                                            QA_dict = self.saveqa(question, answer, dic)
                                            subtitle_qa.append(QA_dict)
                                            # QA_flag = True
                                    # 没有重复
                                    else:
                                        question = dic['subject'][1] + '中' + dic['subject'][-2] + '的' + subtitle[list(subtitle.keys())[0]] + '是什么？'
                                        answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        # 直接保存QA
                                        QA_dict = self.saveqa(question, answer, dic)
                                        subtitle_qa.append(QA_dict)
                                        # QA_flag = True
                                        # 这个是表示列表的词语
                                        if len([i for i in subtitle_words if i in Paragraph.list_subtitles]) > 0:
                                            question = dic['subject'][1] + '中' + dic['subject'][-2] + '有哪些' + subtitle[list(subtitle.keys())[0]] + '？'
                                            answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                            # 直接保存QA
                                            QA_dict = self.saveqa(question, answer, dic)
                                            subtitle_qa.append(QA_dict)
                                            # QA_flag = True
                        # 没有小标题下的正文，那就是不生成了呗
                        else:
                            QA_flag = False
                # 没有小标题，不生成
                else:
                    QA_flag = False


            # '开发者工具中心'
            # 标题在mingingless中，且没有subject或者有subject，但subject为空
            # 这种的就是典型的华为云开发者工具中心
            else:
                # 不生成QA吧，烦人的
                # emmmm，还是生成一下吧，这个就和普通的小标题生成问题一样，只不过把subject去掉
                # 取出该页面的所有的小标题
                subtitles = self.get_subtitle(dic)
                # 有小标题
                if len(subtitles) > 0:
                    for subtitle in subtitles:
                        # 判断subcontent是不是为空：
                        if dic[list(subtitle.keys())[0].replace('title', 'content')].strip() != '':
                            # 小标题是问句
                            if self.Is_ask_type(subtitle[list(subtitle.keys())[0]]):
                                question = subtitle[list(subtitle.keys())[0]]
                                answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                # 直接保存QA
                                QA_dict = self.saveqa(question, answer, dic)
                                subtitle_qa.append(QA_dict)
                                # QA_flag = True

                            # 正常的小标题，都是单个词语
                            else:
                                # 小标题先分词
                                subtitle_words = list(Paragraph.segmentor.segment(subtitle[list(subtitle.keys())[0]]))
                                # 分词后看句法关系
                                result = self.ltp_request(subtitle_words)

                                for arc in result:
                                    if arc['relate'] == 'VOB':  # 词里面有动宾关系，可以提问如何xxx
                                        VOB_flag = True
                                        # 只要有直接退出
                                        break
                                    else:
                                        VOB_flag = False
                                # 表示句子中有VOB
                                if VOB_flag:
                                    # 小标题与标题有重复，可以覆盖
                                    if len([i for i in subtitle_words if i in title_list]) > 0:
                                        question = '如何' + subtitle[list(subtitle.keys())[0]] + '？'
                                        answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        if len([i for i in subtitle_words if i in Paragraph.list_subtitles]) > 0:
                                            question = '有哪些' + subtitle[list(subtitle.keys())[0]] + '？'
                                            answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        # 直接保存QA
                                        QA_dict = self.saveqa(question, answer, dic)
                                        subtitle_qa.append(QA_dict)
                                        # QA_flag = True
                                    # 小标题没有重复
                                    else:

                                        question = title + '中' + '如何' + subtitle[list(subtitle.keys())[0]] + '？'
                                        answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        if len([i for i in subtitle_words if
                                                i in Paragraph.list_subtitles]) > 0:
                                            question = title + '中' + '有哪些' + subtitle[list(subtitle.keys())[0]] + '？'
                                            answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        # 直接保存QA
                                        QA_dict = self.saveqa(question, answer, dic)
                                        subtitle_qa.append(QA_dict)
                                        # QA_flag = True
                                # 没有VOB，就是名词
                                else:
                                    # 小标题覆盖
                                    if len([i for i in subtitle_words if i in title_list]) > 0:
                                        question = subtitle[list(subtitle.keys())[0]] + '是什么？'
                                        # print(subtitle)
                                        answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        # 这个是表示列表的词语
                                        if len([i for i in subtitle_words if i in Paragraph.list_subtitles]) > 0:
                                            question = '有哪些' + subtitle[
                                                list(subtitle.keys())[0]] + '？'
                                            answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        # 直接保存QA
                                        QA_dict = self.saveqa(question, answer, dic)
                                        subtitle_qa.append(QA_dict)
                                        # QA_flag = True

                                    # 小标题不覆盖
                                    else:
                                        question = title + '的' + subtitle[list(subtitle.keys())[0]] + '是什么？'
                                        answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        # 这个是表示列表的词语
                                        if len([i for i in subtitle_words if i in Paragraph.list_subtitles]) > 0:
                                            question = title + '有哪些' + subtitle[list(subtitle.keys())[0]] + '？'
                                            answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        # 直接保存QA
                                        QA_dict = self.saveqa(question, answer, dic)
                                        subtitle_qa.append(QA_dict)
                                        # QA_flag = True
                        # 小标题下的内容为空
                        else:
                            QA_flag = False

                # 没有小标题，不生成QA对
                else:
                    QA_flag = False


        # 是正常的大标题
        else:
            # 判断是否有subject
            if 'subject' in dic.keys() and (len(dic['subject']) > 0):

                # 取出该页面的所有的小标题
                subtitles = self.get_subtitle(dic)
                # 有小标题
                if len(subtitles) > 0:
                    for subtitle in subtitles:
                        # 判断subcontent是不是为空：
                        if dic[list(subtitle.keys())[0].replace('title', 'content')].strip() != '':
                            # 小标题是问句
                            if self.Is_ask_type(subtitle[list(subtitle.keys())[0]]):
                                question = subtitle[list(subtitle.keys())[0]]
                                answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                # 直接保存QA
                                QA_dict = self.saveqa(question, answer, dic)
                                subtitle_qa.append(QA_dict)
                                # QA_flag = True

                            # 正常的小标题，都是单个词语
                            else:
                                # 小标题先分词
                                subtitle_words = list(Paragraph.segmentor.segment(subtitle[list(subtitle.keys())[0]]))
                                # 分词后看句法关系
                                result = self.ltp_request(subtitle_words)

                                for arc in result:
                                    if arc['relate'] == 'VOB':  # 词里面有动宾关系，可以提问如何xxx
                                        VOB_flag = True
                                        # 只要有直接退出
                                        break
                                    else:
                                        VOB_flag = False
                                # 表示句子中有VOB
                                if VOB_flag:
                                    # 小标题与标题有重复，可以覆盖
                                    if len([i for i in subtitle_words if i in title_list]) > 0:
                                        question = dic['subject'][1] + '中' + '如何' + subtitle[
                                            list(subtitle.keys())[0]] + '？'
                                        answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        if len([i for i in subtitle_words if i in Paragraph.list_subtitles]) > 0:
                                            question = dic['subject'][1] + '中' + '有哪些' + subtitle[
                                                list(subtitle.keys())[0]] + '？'
                                            answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        # 直接保存QA
                                        QA_dict = self.saveqa(question, answer, dic)
                                        subtitle_qa.append(QA_dict)
                                        # QA_flag = True
                                    # 小标题没有重复
                                    else:

                                        question = dic['subject'][1] + '的' + title + '中' + '如何' + subtitle[
                                            list(subtitle.keys())[0]] + '？'
                                        answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        if len([i for i in subtitle_words if
                                                i in Paragraph.list_subtitles]) > 0:
                                            question = dic['subject'][1] + '的' + title + '中' + '有哪些' + subtitle[
                                                list(subtitle.keys())[0]] + '？'
                                            answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        # 直接保存QA
                                        QA_dict = self.saveqa(question, answer, dic)
                                        subtitle_qa.append(QA_dict)
                                        # QA_flag = True
                                # 没有VOB，就是名词
                                else:
                                    # 小标题覆盖
                                    if len([i for i in subtitle_words if i in title_list]) > 0:
                                        question = dic['subject'][1] + '中' + subtitle[list(subtitle.keys())[0]] + '是什么？'
                                        # print(subtitle)
                                        answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        # 这个是表示列表的词语
                                        if len([i for i in subtitle_words if i in Paragraph.list_subtitles]) > 0:
                                            question = dic['subject'][1] + '中' + '有哪些' + subtitle[
                                                list(subtitle.keys())[0]] + '？'
                                            answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        # 直接保存QA
                                        QA_dict = self.saveqa(question, answer, dic)
                                        subtitle_qa.append(QA_dict)
                                        # QA_flag = True

                                    # 小标题不覆盖
                                    else:
                                        question = dic['subject'][1] + '中' + title + '的' + subtitle[
                                            list(subtitle.keys())[0]] + '是什么？'
                                        answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        # 这个是表示列表的词语
                                        if len([i for i in subtitle_words if i in Paragraph.list_subtitles]) > 0:
                                            question = dic['subject'][1] + '中' + title + '有哪些' + subtitle[
                                                list(subtitle.keys())[0]] + '？'
                                            answer = dic[list(subtitle.keys())[0].replace('title', 'content')]

                                        # 直接保存QA
                                        QA_dict = self.saveqa(question, answer, dic)
                                        subtitle_qa.append(QA_dict)
                                        # QA_flag = True
                        # 小标题下的内容为空
                        else:
                            QA_flag = False

                # 没有小标题，不生成QA对
                else:
                    QA_flag = False




            else:  # 在正常的大标题下，但是没有subject，不生成QA对
                QA_flag = False


        return subtitle_qa



    # 判断输入的句子是否为问句 返回ture false
    def Is_ask_type(self,sentence):
        # 输出变量
        result = True
        words = Paragraph.segmentor.segment(sentence)  # 分词
        words_list = list(words)

        for i in words_list:
            # 根据句子末尾是否有问号，句子中是否有疑问词
            if i in Paragraph.ques_words_list or i == '？' or i == '?':
                result = True
                break
            else:
                result = False

        return result

    # 发送LTP请求的函数
    def ltp_request(self,sentence_list):
        # line = '虚拟化驱动不正常时网络、存储性能降低。'
        # words = Paragraph.segmentor.segment(sentence)  # 分词
        # words_list = list(words)
        # print(words_list)

        # LTML用于构建自定义分词的xml，用于向LTP云传入args
        ltml = LTML()
        ltml.build_from_words(sentence_list)
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

        content = r.json()

        # for i in content[0][0]:
        #     print(i)

        return content[0][0]

    # 写两个函数，函数使用来加标点符号的
    # 问句加标点
    def ques_punctuation(self,ques_sen):  # 问句的标点符号
        ques_sen = ques_sen.strip()
        # 判断问句的最后一位的标点
        if ques_sen[-1] in ['，', '。', '；']:  # 说明句子的最后一位是有标点的，但不是问号
            ques_sen = ques_sen[:-1] + '？'
        elif ques_sen[-1] not in ['，', '。', '？', '；', '！']:  # 句子最后没有标点结尾的
            ques_sen = ques_sen + '?'
        return ques_sen
    # 陈述句加标点
    def ans_punctuation(self,ans_sen):
        ans_sen = ans_sen.strip()
        # 判断问句的最后一位的标点
        if ans_sen[-1] in ['，', '？', '；']:  # 说明句子的最后一位是有标点的，但不是句号
            ans_sen = ans_sen[:-1] + '。'
        elif ans_sen[-1] not in ['，', '。', '？', '；', '！']:  # 句子最后没有标点结尾的
            ans_sen = ans_sen + '。'
        return ans_sen

    # 获取该页面下的小标题
    def get_subtitle(self,dic):
        num_subtilte = 0  # subtilte的个数
        pattern = re.compile(r'subtitle')

        # 获取该文档中的subtitle的个数
        for keys in dic.keys():
            if len(pattern.findall(keys)) != 0:
                num_subtilte += 1
        # print(url+":"+str(num_subtilte))

        subtitles = []
        if num_subtilte > 0:
            for num in range(num_subtilte):
                # subtitle = common_json[i]['subtitle' + str(num + 1)]
                key = 'subtitle' + str(num + 1)
                subtitle = re.sub(r'<.*?>', '', dic['subtitle' + str(num + 1)].strip())
                # pair = {}
                # pair[key] = subtitle
                subtitles.append({key:subtitle})

        # print(subtitles)

        return subtitles


    # 保存QA对
    def saveqa(self,question,answer,dic):

        # QA对的保存形式
        QA_dict = {}

        # 辣么这些title可以直接存入QA对中
        QA_dict['question'] = self.ques_punctuation(question)
        QA_dict['answer'] = self.ans_punctuation(answer)
        if 'link' in dic.keys() and dic['link'] != '':
            QA_dict['answer_link'] = dic['link']
        else:
            QA_dict['answer_link'] = ''
        if 'subject' in dic.keys() and (len(dic['subject']) > 0):
            QA_dict['subject'] = dic['subject'][1]
        else:
            QA_dict['subject'] = ''

        return QA_dict
