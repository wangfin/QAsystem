# -*- coding: utf-8 -*-
# @Time    : 2018/8/11 15:13
# @Author  : wb
# @File    : classification_test.py

# 分类文件的测试

# how_do = ['怎样','怎么','怎么样','如何','哪些方法','哪些方式','哪些途径','何种方法','什么方法','什么方式','什么途径']
#
# question = '数码大师生成视频后如何修改'
# for question_word in how_do:
#     if question_word in question:
#         print('yes')
#     else:
#         print('no')


# class Test():
#     a = 1
#     b = 2
#     c = 3
#
# x = ['a','b','c']
#
# test = Test()
# for i in x:
#     print(test + '.' + i)


yes_no = ['能','能够','会可','可能','可以','有','是']
# 定义类
definition = ['是什么']
# 列表类 list_ques
list_ques = ['哪些', '有什么', '有哪些', '有啥']
# 哪个 which
which = ['哪个', '哪']
# 正常疑问句
common_ques = ['什么']
# 疑问语气词
modal = ['吗','呢','吧','么','嘛']

def check_question_type(question, question_words_list):
    # 疑问词之间有重复
    # 同时是否类的疑问词，是助动词与语气词的拼接
    # 对疑问词列表的中的疑问词进行分词
    result = None

    # 直接判断疑问句中是否有此字符串
    for question_word in question_words_list:
        # print(question_word)
        if question_word in question:
            result = True
            break
        else:
            result = False

    return result

question = '什么是创客教育？'

result1 = check_question_type(question, yes_no)
result2 = check_question_type(question, modal)
result3 = check_question_type(question, which)
print(result1)
print(result2)
print(result3)