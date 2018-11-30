# -*- coding: utf-8 -*-
# @Time    : 2018/8/30 2:01
# @Author  : wb
# @File    : temporary_generate.py
import random

from QAManagement.question_generalization.clean import Clean

# 临时生成泛化
class Temporary():
    # w2v = KeyedVectors.load_word2vec_format('/home/wang/data/chinese_model.txt', limit=500000)
    # 分类的疑问词
    # 多久 how-long
    how_long = ['多长时间', '多少时间', '多久']
    # 多少 how-much
    how_much = ['多少', '几']
    # 地点 where
    where = ['什么地方', '什么地点', '哪里', '何处', '哪个地方']
    # 方式 how_do
    how_do = ['怎样', '怎么', '怎么样', '如何', '哪些方法', '哪些方式', '哪些途径', '何种方法', '什么方法', '什么方式', '什么途径']
    # 人物 who
    who = ['什么人', '谁', '哪个人', '何人', '哪些人', '哪一个人']
    # 时间 when
    when = ['什么时间', '什么时候', '何时', '哪个时候']
    # 原因 why
    why = ['什么原因', '哪些原因', '什么因素', '哪些因素', '为什么', '为何']
    # 是否类 yes_no
    yes_no = ['能', '能够', '会可', '可能', '可以', '有', '是']
    # 定义类
    definition = ['是什么', '什么是']
    # 列表类 list_ques
    list_ques = ['哪些', '有什么', '有哪些', '有啥','有什么']
    # 哪个 which
    which = ['哪个', '哪']
    # 正常疑问句
    common_ques = ['什么']
    # 疑问语气词
    modal = ['吗', '呢', '吧', '么', '嘛']


    def main(self,question):


        words = Clean.segmentor.segment(question)  # 分词
        words_list = list(words)

        result = []

        # 定义类
        definition = [i for i in words_list if i in Temporary.definition]
        how_long = [i for i in words_list if i in Temporary.how_long]
        how_much = [i for i in words_list if i in Temporary.how_much]
        list_ques = [i for i in words_list if i in Temporary.list_ques]
        how_do = [i for i in words_list if i in Temporary.how_do]
        why = [i for i in words_list if i in Temporary.why]
        where = [i for i in words_list if i in Temporary.where]
        yes_no = [i for i in words_list if i in Temporary.yes_no]

        if '是什么' in question:
            result.append(question.replace('是什么','定义是什么'))
            question = '什么是' + question.replace('是什么','')
            result.append(question)
            return result

        elif len(how_long) > 0:

            randomIndex = random.sample(range(len(Temporary.how_long)), 2)
            for i in randomIndex:
                result.append(question.replace(how_long[0], Temporary.how_long[i]))
                #result.append(
                    #question.replace(how_long[0], Temporary.how_long[random.randint(0, len(Temporary.how_long) - 1)]))
            return result
        elif len(how_much) > 0:
            randomIndex = random.sample(range(len(Temporary.how_much)), 2)
            for i in randomIndex:
                result.append(question.replace(how_much[0], Temporary.how_much[i]))
            #result.append(
                #question.replace(how_much[0], Temporary.how_much[random.randint(0, len(Temporary.how_much) - 1)]))
            return result
        elif len(list_ques) > 0:
            randomIndex = random.sample(range(len(Temporary.list_ques)), 2)
            for i in randomIndex:
                result.append(question.replace(list_ques[0], Temporary.list_ques[i]))
            # result.append(
                # question.replace(list_ques[0], Temporary.list_ques[random.randint(0, len(Temporary.list_ques) - 1)]))
            return result
        elif len(how_do) > 0:
            randomIndex = random.sample(range(len(Temporary.how_do)), 2)
            for i in randomIndex:
                result.append(question.replace(how_do[0], Temporary.how_do[i]))
            # result.append(question.replace(how_do[0], Temporary.how_do[random.randint(0, len(Temporary.how_do) - 1)]))
            return result
        elif len(why) > 0:
            randomIndex = random.sample(range(len(Temporary.why)), 2)
            for i in randomIndex:
                result.append(question.replace(why[0], Temporary.why[i]))
            # result.append(question.replace(why[0], Temporary.why[random.randint(0, len(Temporary.why) - 1)]))
            return result
        elif len(where) > 0:
            randomIndex = random.sample(range(len(Temporary.where)), 2)
            for i in randomIndex:
                result.append(question.replace(where[0], Temporary.where[i]))
            # result.append(question.replace(where[0], Temporary.why[random.randint(0, len(Temporary.where) - 1)]))
            return result
        elif len(yes_no) > 0:
            randomIndex = random.sample(range(len(Temporary.yes_no)), 2)
            for i in randomIndex:
                result.append(question.replace(yes_no[0], Temporary.yes_no[i]))
            # result.append(question.replace(yes_no[0], Temporary.yes_no[random.randint(0, len(Temporary.yes_no) - 1)]))
            return result


