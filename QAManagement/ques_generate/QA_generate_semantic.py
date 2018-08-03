# coding: utf-8


import requests
from pyltp import Segmentor
import os
from LTML import LTML

# 本页面是用来生产QA对的
# 通过使用依存语义分析

# 先进行自定义的分词
LTP_DATA_DIR = '../data/ltp_data'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
segmentor = Segmentor()  # 初始化实例
segmentor.load_with_lexicon(cws_model_path, '../data/new_dictionary.txt') # 加载模型，第二个参数是您的增量模型路径


line = '虚拟化驱动不正常时网络、存储性能降低。'
words = segmentor.segment(line)# 分词
words_list = list(words)
print(words_list)


# LTML用于构建自定义分词的xml，用于向LTP云传入args
ltml = LTML()
ltml.build_from_words(words_list)
xml  = ltml.tostring()
#print(xml)


url_get_base = "https://api.ltp-cloud.com/analysis/"

# 这个是加入自定义词典的参数
args = { 
    'api_key' : 'a1R923E7s37daeNz7dsMeXiTexWGoookJX2HONwC',
    'pattern' : 'sdp',
    'format' : 'json',
    'xml_input':'true',
     'text' : xml
}
# args_others = { 
#     'api_key' : 'a1R923E7s37daeNz7dsMeXiTexWGoookJX2HONwC',
#     'pattern' : 'sdp',
#     'format' : 'json',
#     'xml_input':'true',
#      'text' : xml
# }
#args_text =  { 'text' : '华为云提供了Web化的服务管理平台（即控制台）和基于HTTPS请求的API（Application programming interface）管理方式。'}
# 两个字典合并
#args = dict(args_others, **args_text)
r = requests.post(url_get_base, data = args)


# In[54]:


content = r.json()
for i in content[0][0]:
    print(i)
#print(r.text)


# In[25]:


# 写两个函数，函数使用来加标点符号的
def ques_punctuation(ques_sen):# 问句的标点符号
    #判断问句的最后一位的标点
    if ques_sen[-1] in ['，', '。','；']:# 说明句子的最后一位是有标点的，但不是问号
        ques_sen = ques_sen[:-1] + '？'
    elif ques_sen[-1] not in ['，','。','？','；','！']:# 句子最后没有标点结尾的
        ques_sen = ques_sen + '?'
    return ques_sen

def ans_punctuation(ans_sen):
    #判断问句的最后一位的标点
    if ans_sen[-1] in ['，', '？','；']:# 说明句子的最后一位是有标点的，但不是句号
        ans_sen = ans_sen[:-1] + '。'
    elif ans_sen[-1] not in ['，','。','？','；','！']:# 句子最后没有标点结尾的
        ans_sen = ans_sen + '。'
    return ans_sen

# 再写一个函数
# 函数用于找节点的父节点的父节点
# 通常用于查询目标节点的子节点
def find_parent(con,content):
    id = con['id']
    parent_id = con['semparent']
    for i in content:
        if i['id'] == parent_id:
            return i['semparent']
            



# 事件的原因，事件的结果 提问
# 第一个，事件的结果
# 离开的结果是见不到
Resu_flag = False
question_sen = ''
answer_sen = ''
for con in content[0][0]:
    if con['semrelate'] == 'eResu': #表明其中有表示结果的关系
        word = con['cont']# 这个词的文字
        id = con['id']# 这个词的id
        semparent = con['semparent']# 这个词的父节点
        parent_word = content[0][0][semparent]['cont']# 这个词的父节点的词
        parent_id = content[0][0][semparent]['id']# 父节点的id
        Resu_flag = True # 里面有可以提问的部分

if Resu_flag:
    # question的内容，里面最后的结果
    for con in content[0][0]:
        if con['semrelate'] == 'mNeg':
        # 考虑到了否定标记，这种标记有的时候不是直接作用于关键动词上的，需要手动标记
            mNeg_parentid =  con['semparent'] # 父节点的id
            mNeg_word = con['cont']
            if con['id'] == mNeg_parentid:# 找到了否定词的父节点
                if con['semparent'] == id or con['id'] == id:#如果父节点符合要求的话
                    con['cont'] = mNeg_word+ con['cont']# 将原有的数组中的词改成新的
        # 下面是question的具体拼接
        if con['semparent'] == id or con['id'] == id:# 把与结果词相关的词都挑出来，这些都是结果的内容
            if con['semrelate'] not in ['mPrep','mConj']:# 这些词中没有介词和连词
                question_sen += con['cont']
                # 考虑到了否定标记，这种标记都是作用于其中的某一个词的
                if con['semrelate'] == 'mNeg':
                    question_sen += con['cont']
    question_sen = '为什么' + question_sen
    question_sen = ques_punctuation(question_sen)
    print(question_sen)

    # answer的内容，里面是原因的内容
    for con in content[0][0]:
        if (con['semparent'] == parent_id or con['id'] == parent_id) and con['id'] != id:# 把与父节点有关的词全部挑出来，这些都是原因的内容
            if con['semrelate'] not in ['mPrep','mConj']:# 这些词中没有介词和连词
                answer_sen += con['cont']
    answer_sen = ans_punctuation(answer_sen)
    print(answer_sen)
else:
    print('没有Resu的问题')


# In[57]:


# 第二个 事情的原因
# 他失败的原因是没有好好学习
Cau_flag = False
question_sen = ''
answer_sen = ''
for con in content[0][0]:
    if con['semrelate'] == 'eCau': #表明其中有表示结果的关系
        word = con['cont']# 这个词的文字
        id = con['id']# 这个词的 id
        semparent = con['semparent']# 这个词的父节点
        parent_word = content[0][0][semparent]['cont']# 这个词的父节点的词
        parent_id = content[0][0][semparent]['id']# 父节点的id
        Cau_flag = True
if Cau_flag:
    # question里面的内容，结果的内容
    for con in content[0][0]:
        if (con['semparent'] == parent_id or con['id'] == parent_id) and con['id']!=id:# 把与结果词相关的词都挑出来，这些都是结果的内容
            if con['semrelate'] not in ['mPrep','mConj']:# 这些词中没有介词和连词
                question_sen += con['cont']
    question_sen = '为什么' + question_sen
    question_sen = ques_punctuation(question_sen)
    print(question_sen)

    # answer里面的内容，原因的内容
    for con in content[0][0]:
        if con['semrelate'] == 'mNeg':
        # 考虑到了否定标记，这种标记有的时候不是直接作用于关键动词上的，需要手动标记
            mNeg_parentid =  con['semparent'] # 父节点的id
            mNeg_word = con['cont']
        if con['id'] == mNeg_parentid:# 找到了否定词的父节点
            if con['semparent'] == id or con['id'] == id:#如果父节点符合要求的话
                con['cont'] = mNeg_word+ con['cont']# 将原有的数组中的词改成新的
        # 下面是answer的字的拼接
        if con['semparent'] == id or con['id'] == id :# 把与结果词相关的词都挑出来，这些都是结果的内容
            if con['semrelate'] not in ['mPrep','mConj']:# 这些词中没有介词和连词
                answer_sen += con['cont']
    answer_sen = ans_punctuation(answer_sen)
    print(answer_sen)
else:
    print('没有Cau的问题')


# In[58]:


# 关于目的的提问
Prup_flag = False
question_sen = ''
answer_sen = ''
for con in content[0][0]:
    if con['semrelate'] == 'ePurp': #表明其中有表示目的的内容
        word = con['cont']# 这个词的文字
        id = con['id']# 这个词的 id
        semparent = con['semparent']# 这个词的父节点
        parent_word = content[0][0][semparent]['cont']# 这个词的父节点的词
        parent_id = content[0][0][semparent]['id']# 父节点的id
        Prup_flag = True
        
if Prup_flag:# 有目的的问题
    # question的内容，里面是为了的内容
    for con in content[0][0]:
        # 父节点，父节点的子节点，
        if (con['semparent'] == parent_id or con['id'] == parent_id) and con['id'] != id:# 把与父节点有关的词全部挑出来，这些都是原因的内容
            if con['semrelate'] not in ['mPrep','mConj']:# 这些词中没有介词和连词
                question_sen += con['cont']
    
    # answer的内容，里面是为了的结果
    for con in content[0][0]:
        if con['semrelate'] == 'mNeg' or con['semrelate'] == 'mAux':
        # 考虑到了否定标记和的 标记，这种标记有的时候不是直接作用于关键动词上的，需要手动标记
            mNeg_parentid =  con['semparent'] # 父节点的id
            mNeg_word = con['cont']
            #print(mNeg_parentid)
        if mNeg_parentid and con['id'] == mNeg_parentid:# 找到了否定词的父节点
            if con['semparent'] == id or con['id'] == id:#如果父节点符合要求的话
                if mNeg_parentid > id:
                    con['cont'] = mNeg_word+ con['cont'] # 将原有的数组中的词改成新的
                else:
                    con['cont'] =  con['cont'] + mNeg_word
        
        # 下面是answer的具体拼接
        if con['semparent'] == id or con['id'] == id:# 把与结果词相关的词都挑出来，这些都是结果的内容
            if con['semrelate'] not in ['mPrep','mConj']:# 这些词中没有介词和连词
                answer_sen += con['cont']
                # 考虑到了否定标记，这种标记都是作用于其中的某一个词的
                if con['semrelate'] == 'mNeg':
                    answer_sen += con['cont']
    question_sen = '为什么' + question_sen
    question_sen = ques_punctuation(question_sen)
    print(question_sen)
    
    answer_sen = word + parent_word
    answer_sen = ans_punctuation(answer_sen)
    # 最终的答案
    print(answer_sen)
    
    
#     # 问题的拼接
#     # 为什么
#     for con in content[0][0]:
#          if find_parent(con,content[0][0]) == parent_id or con['semparent'] == parent_id or con['id'] == parent_id:
#             question_sen += con['cont'] 
    
#     # 答案的拼接
#     for con in content[0][0]:
#         if find_parent(con,content[0][0]) == id or con['semparent'] == id or con['id'] == id:
#             answer_sen += con['cont']
       
#     question_sen = ques_punctuation(question_sen)
#     print(question_sen)
    
#     answer_sen = ans_punctuation(answer_sen)
#     print(answer_sen)
#         if find_parent(con,con[0][0]) == id or con['id'] == id:
#             if con['semrelate'] not in ['mPrep','mConj']:# 这些词中没有介词和连词
#                 question_sen += con['cont'] 
                
#     question_sen = ques_punctuation(question_sen)
#     print(question_sen)
    
else:
    print('没有Prup的问题')


# In[59]:


# 数量词的问题，多少的问题
Quan_flag = False
question_sen = ''
answer_sen = ''
sen_list = []
for con in content[0][0]:
    if con['semrelate'] == 'Quan': #表明其中有表示数量的内容
        word = con['cont']# 这个词的文字
        id = con['id']# 这个词的 id
        semparent = con['semparent']# 这个词的父节点
        parent_word = content[0][0][semparent]['cont']# 这个词的父节点的词
        parent_id = content[0][0][semparent]['id']# 父节点的id
        Quan_flag = True

# 问句只需要把这个表示数量的词换成多少
if Quan_flag:
    
    for con in content[0][0]:
        if con['id'] == id:# 找到了这个表示数量的词
            # 将这个词替换成多少
            sen_list.append('多少')
        else:
            sen_list.append(con['cont'])
    for i in sen_list:
        question_sen += i
    question_sen = ques_punctuation(question_sen)
    # 最终的问句
    print(question_sen)
    
    answer_sen = word + parent_word
    answer_sen = ans_punctuation(answer_sen)
    # 最终的答案
    print(answer_sen)
else:
    print('没有Quan的问题')


# In[60]:


# 表示时间的问题
Time_flag = False
if_quan_time_flag = True
question_sen = ''
answer_sen = ''
sen_list = []
for con in content[0][0]:
    # 时间的问题需要判断是否有与数量词相连的情况
    # 如果有数量词相连，如 几分钟之内到达 ， 直接将分钟替换成什么时候，这样问句就会变成 几什么时候到达？
    # 如果有这样的词的话不生成问句
    if con['semrelate'] == 'Time': #表明其中有表示时间的内容
        word = con['cont']# 这个词的文字
        id = con['id']# 这个词的 id
        semparent = con['semparent']# 这个词的父节点
        parent_word = content[0][0][semparent]['cont']# 这个词的父节点的词
        parent_id = content[0][0][semparent]['id']# 父节点的id
        Time_flag = True
        
    if con['semrelate'] == 'Quan': #表明其中有表示数量的内容
        quan_semparent = con['semparent']# 这个词的父节点
        quan_parent_word = content[0][0][quan_semparent]['semrelate']# 这个词的父节点的词
        if quan_parent_word == 'Time':
            if_quan_time_flag = False


if Time_flag and if_quan_time_flag:
    for con in content[0][0]:
        if con['id'] == id:# 找到了这个表示时间的词
            # 将这个词替换成多少
            answer_sen += con['cont']
            sen_list.append('什么时候')
        else:
            sen_list.append(con['cont'])

    for i in sen_list:
        question_sen += i
    question_sen = ques_punctuation(question_sen)
    # 最终的问句
    print(question_sen)
    
    answer_sen = ans_punctuation(answer_sen)
    # 最终的答案
    print(answer_sen)
elif not if_quan_time_flag:
    print('时间词前面跟了数量词，不生成时间的问句')
else:
    print('没有Time的问题')


# In[61]:


# 关于地点的问题
Loc_flag = False
question_sen = ''
answer_sen = ''
sen_list = []
preposition = ['在','从','往','沿着','至','将']# 表示地点的介词
for con in content[0][0]:
    if con['semrelate'] == 'Loc': #表明其中有表示地点的内容
        word = con['cont']# 这个词的文字
        id = con['id']# 这个词的 id
        semparent = con['semparent']# 这个词的父节点
        parent_word = content[0][0][semparent]['cont']# 这个词的父节点的词
        parent_id = content[0][0][semparent]['id']# 父节点的id
        Loc_flag = True
        
if Loc_flag:
    for con in content[0][0]:
        if con['semparent'] == id or con['id'] == id or find_parent(con,content[0][0]) == id:
            # 找这个词的子节点，这个词，和这个词的子节点的子节点
            answer_sen += con['cont']
            if con['cont'] in preposition:
                question_sen += con['cont'] + '哪里'
        else:
            question_sen += con['cont']
            
    question_sen = ques_punctuation(question_sen)
    # 最终的问题
    print(question_sen)
    answer_sen = ans_punctuation(answer_sen)
     # 最终的答案
    print(answer_sen)
    
else:
    print('没有LOC的问题')


# In[62]:


# 依据角色的提问
# 例如，通过华为云用户手册，您可以登录华为云服务器。
Accd_flag = False
question_sen = ''
answer_sen = ''
sen_list = []
preposition = ['通过','按照','以','凭','本着','拿']# 依据角色的介词
for con in content[0][0]:
    if con['semrelate'] == 'Accd': #表明其中有表示数量的内容
        word = con['cont']# 这个词的文字
        id = con['id']# 这个词的 id
        semparent = con['semparent']# 这个词的父节点
        parent_word = content[0][0][semparent]['cont']# 这个词的父节点的词
        parent_id = content[0][0][semparent]['id']# 父节点的id
        Accd_flag = True
if Accd_flag:
    for con in content[0][0]:
        if con['semparent'] == id or con['id'] == id or find_parent(con,content[0][0]) == id:
            # 找这个词的子节点，这个词，和这个词的子节点的子节点
            answer_sen += con['cont']
            if con['cont'] in preposition:
                question_sen += con['cont'] + '什么'
        else:
            question_sen += con['cont']
   
    question_sen = ques_punctuation(question_sen)
    # 最终的问题
    print(question_sen)
    answer_sen = ans_punctuation(answer_sen)
     # 最终的答案
    print(answer_sen)
        
else:
    print('没有Accd的问题')


# In[63]:


# Yes or NO的问题
# 找出句子中的否定词，将否定词
Neg_flag = False
question_sen = ''
answer_sen = ''
sen_list = []
for con in content[0][0]:
    if con['semrelate'] == 'mNeg': #表明其中有表示数量的内容
        word = con['cont']# 这个词的文字
        id = con['id']# 这个词的 id
        semparent = con['semparent']# 这个词的父节点
        parent_word = content[0][0][semparent]['cont']# 这个词的父节点的词
        parent_id = content[0][0][semparent]['id']# 父节点的id
        Neg_flag = True
        
if Neg_flag:
    for con in content[0][0]:
        if con['id'] != id:
            question_sen += con['cont']
    
    answer_sen = word + parent_word
    
    question_sen = ques_punctuation(question_sen)
    # 最终的问句
    print(question_sen.replace('？','吗？'))
    
    answer_sen = ans_punctuation(answer_sen)
    # 最终的答案
    print(answer_sen)
    
else:
    print('没有YES_NO的问题')


# In[64]:


# 为这个莫名其妙的 EXP（当事关系）写一个问题生成
# 例如，通过华为云用户手册，您可以登录华为云服务器。
Exp_flag = False
question_sen = ''
answer_sen = ''
sen_list = []
is_ques_word = True
preposition = ['通过','按照','以','凭','本着','拿']# 依据角色的介词
for con in content[0][0]:
    if con['semrelate'] == 'Exp': #表明其中有表示数量的内容
        word = con['cont']# 这个词的文字
        id = con['id']# 这个词的 id
        semparent = con['semparent']# 这个词的父节点
        parent_word = content[0][0][semparent]['cont']# 这个词的父节点的词
        parent_id = content[0][0][semparent]['id']# 父节点的id
        Exp_flag = True
if Exp_flag:
    for con in content[0][0]:
        if con['semparent'] == id or con['id'] == id or find_parent(con,content[0][0]) == id:
            # 找这个词的子节点，这个词，和这个词的子节点的子节点
            answer_sen += con['cont']
            if is_ques_word:
                question_sen += '什么'
                is_ques_word = False
        else:
            question_sen += con['cont']
   
    question_sen = ques_punctuation(question_sen)
    # 最终的问题
    print(question_sen)
    answer_sen = ans_punctuation(answer_sen)
     # 最终的答案
    print(answer_sen)
        
else:
    print('没有EXP的问题')


# In[ ]:


# 列表型的问题
# 等，们 表示多数的标记，找到这些标记，找出这些标记有关的所有有并列的词
# eg：华为云提供了Web化的服务管理平台（即控制台）和基于HTTPS请求的API（Application programming interface）管理方式
# 华为云提供了哪些管理方式


# In[50]:


# 书名号的提问
# 具体操作请参见《CDN参考手册》
# 提问：具体操作请参见什么东西
Book_flag = False
question_sen = ''
answer_sen = ''
sen = list(words_list)
# 找到里面的 《 ，以《 切分
if "《" in words_list:
    for i in range(len(words_list)):
        if words_list[i] == '《':
            Book_start = i
        elif words_list[i] == '》':
            Book_end = i
    
    for i in sen[Book_start:Book_end+1]:
        answer_sen += i
    answer_sen = ans_punctuation(answer_sen)
    sen[Book_start:Book_end+1] = '什么'
    for i in sen:
        question_sen += i
    question_sen = ques_punctuation(question_sen)

    print(question_sen)

    print(answer_sen)
else:
    print('无')

