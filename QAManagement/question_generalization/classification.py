# -*- coding: utf-8 -*-
# @Time    : 2018/8/11 9:00
# @Author  : wb
# @File    : classification.py

import os
from pyltp import Segmentor
from pyltp import Postagger
# 用于问句分类

class Classification():
    # 导入ltp
    LTP_DATA_DIR = '../data/ltp_data'  # ltp模型目录的路径

    # 分词
    cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
    segmentor = Segmentor()  # 初始化实例
    segmentor.load_with_lexicon(cws_model_path, '../data/new_dictionary.txt')  # 加载模型，第二个参数是您的增量模型路径

    # 分类的疑问词
    # 多久 how-long
    how_long = ['多长时间','多少时间','多久']
    # 多少 how-much
    how_much = ['多少','几']
    # 地点 where
    where = ['什么地方','什么地点','哪里','何处','哪个地方']
    # 方式 how_do
    how_do = ['怎样','怎么','怎么样','如何','哪些方法','哪些方式','哪些途径','何种方法','什么方法','什么方式','什么途径']
    # 人物 who
    who = ['什么人','谁','哪个人','何人','哪些人','哪一个人']
    # 时间 when
    when = ['什么时间','什么时候','何时','哪个时候']
    # 原因 why
    why = ['什么原因','哪些原因','什么因素','哪些因素','为什么','为何']
    # 是否类 yes_no
    yes_no = ['能','能够','会可','可能','可以','有','是']
    # 定义类
    definition = ['是什么','什么是']
    # 列表类 list_ques
    list_ques = ['哪些','有什么','有哪些','有啥']
    # 哪个 which
    which = ['哪个','哪']
    # 正常疑问句
    common_ques = ['什么']
    # 疑问语气词
    modal = ['吗','呢','吧','么','嘛']

    # 设置各个类别的问句
    how_long_questions = []
    how_much_questions = []
    where_questions = []
    how_do_questions = []
    who_questions = []
    when_questions = []
    why_questions = []
    list_ques_questions = []
    yes_no_questions = []
    definition_questions = []
    common_ques_questions = []
    which_questions = []
    other_questions = []


    '''
        有些关键疑问词会经常出现
        如：什么，哪
    
    '''

    # 疑问词对比函数
    # 输入疑问句字符串分词列表，疑问词列表
    def check_question_type(self,question,question_words_list):
        # 疑问词之间有重复
        # 同时是否类的疑问词，是助动词与语气词的拼接
        # 对疑问词列表的中的疑问词进行分词
        result = None

        # 直接判断疑问句中是否有此字符串
        for question_word in question_words_list:
            if question_word in question:
                result = True
                break
            else:
                result = False

        return result

    # 检查语气词
    def check_modal(self,question):
        # 语气词的检查，需要判断语气词是否在句子末尾

        # 根据观察，在句子的末尾可能会有什么，结尾也是么，所以对于语气词的检查我们使用分词
        words = Classification.segmentor.segment(question)  # 分词
        words_list = list(words)

        result = None

        for mod in Classification.modal:
            if words_list[-2] == mod:
                result = True
                break
            else:
                result = False

        return result



    # 分类函数
    def classif(self,question_list):
        # 感觉不需要分词，直接进行字符串比配即可
        for question in question_list:
            # words = segmentor.segment(question_list)# 分词
            # words_list = list(words)
            # print(' '.join(words))
            if self.check_question_type(question, Classification.how_long):
                # how_long
                Classification.how_long_questions.append(question)
            elif self.check_question_type(question, Classification.where):
                # where
                Classification.where_questions.append(question)
            elif self.check_question_type(question, Classification.how_do):
                # how_do
                Classification.how_do_questions.append(question)
            elif self.check_question_type(question, Classification.who):
                # who
                Classification.who_questions.append(question)
            elif self.check_question_type(question, Classification.when):
                # when
                Classification.when_questions.append(question)
            elif self.check_question_type(question, Classification.why):
                # why
                Classification.why_questions.append(question)
            elif self.check_question_type(question, Classification.definition):
                # definition
                Classification.definition_questions.append(question)
            elif self.check_question_type(question, Classification.list_ques):
                # list_ques
                Classification.list_ques_questions.append(question)
            elif self.check_question_type(question, Classification.how_much):
                # how_much
                Classification.how_much_questions.append(question)
            elif self.check_question_type(question, Classification.yes_no) and self.check_modal(question):
                # yes_no
                Classification.yes_no_questions.append(question)
            elif self.check_modal(question):
                # yes_no
                Classification.yes_no_questions.append(question)
            elif self.check_question_type(question, Classification.common_ques):
                # common_ques
                Classification.common_ques_questions.append(question)
            elif self.check_question_type(question, Classification.which):
                # which
                Classification.which_questions.append(question)
            else:
                # others
                Classification.other_questions.append(question)


    def main(self,question_list):
        self.classif(question_list)




if __name__ == "__main__":
    # 输入问句
    question_file = open('../data/zhidao_train_clean_questions')
    question_list = []
    for line in question_file:
        question_list.append(line.strip('\n'))

    classif = Classification()

    classif.main(question_list)

    print(len(Classification.how_long_questions))
    print(len(Classification.how_do_questions))
    print(len(Classification.how_much_questions))
    print(len(Classification.where_questions))
    print(len(Classification.who_questions))
    print(len(Classification.when_questions))
    print(len(Classification.why_questions))
    print(len(Classification.which_questions))
    print(len(Classification.definition_questions))
    print(len(Classification.list_ques_questions))
    print(len(Classification.yes_no_questions))
    print(len(Classification.common_ques_questions))
    print(len(Classification.other_questions))

    category = ['how_long_questions','where_questions','how_do_questions','who_questions','when_questions',
                'why_questions','definition_questions','list_ques_questions','how_much_questions',
                'yes_no_questions','common_ques_questions','which_questions']

    # 将问句写入文件

    file = open('../data/classification/how_long_questions', 'w')
    for i in Classification.how_long_questions:
        file.write(i + '\n')

    file = open('../data/classification/how_do_questions', 'w')
    for i in Classification.how_do_questions:
        file.write(i + '\n')

    file = open('../data/classification/how_much_questions', 'w')
    for i in Classification.how_much_questions:
        file.write(i + '\n')

    file = open('../data/classification/where_questions', 'w')
    for i in Classification.where_questions:
        file.write(i + '\n')

    file = open('../data/classification/who_questions', 'w')
    for i in Classification.who_questions:
        file.write(i + '\n')

    file = open('../data/classification/when_questions', 'w')
    for i in Classification.when_questions:
        file.write(i + '\n')

    file = open('../data/classification/why_questions', 'w')
    for i in Classification.why_questions:
        file.write(i + '\n')

    file = open('../data/classification/which_questions', 'w')
    for i in Classification.which_questions:
        file.write(i + '\n')

    file = open('../data/classification/definition_questions', 'w')
    for i in Classification.definition_questions:
        file.write(i + '\n')

    file = open('../data/classification/list_ques_questions', 'w')
    for i in Classification.list_ques_questions:
        file.write(i + '\n')

    file = open('../data/classification/yes_no_questions', 'w')
    for i in Classification.yes_no_questions:
        file.write(i + '\n')

    file = open('../data/classification/common_ques_questions', 'w')
    for i in Classification.common_ques_questions:
        file.write(i + '\n')

    file = open('../data/classification/other_questions', 'w')
    for i in Classification.other_questions:
        file.write(i + '\n')






