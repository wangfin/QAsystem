
# coding: utf-8

# In[1]:


import os
from pyltp import SementicRoleLabeller
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser


# In[2]:


LTP_DATA_DIR = '../data/ltp_data'  # ltp模型目录的路径


# In[3]:


# 分词
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
segmentor = Segmentor()  # 初始化实例
segmentor.load_with_lexicon(cws_model_path, '../data/new_dictionary.txt') # 加载模型，第二个参数是您的增量模型路径


# In[4]:


# 词性标注
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
postagger = Postagger() # 初始化实例
postagger.load(pos_model_path)  # 加载模型


# In[5]:


# 依存句法分析
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
parser = Parser() # 初始化实例
parser.load(par_model_path)  # 加载模型


# In[6]:


# 语义角色标注 
srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl.model')  # 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。
labeller = SementicRoleLabeller() # 初始化实例
labeller.load(srl_model_path)  # 加载模型


# In[27]:


line = '虚拟化驱动不正常时网络、存储性能降低。'
words = segmentor.segment(line)# 分词
print(' '.join(words))
words_list = list(words)


# In[28]:


postags = postagger.postag(words_list)  # 词性标注
postags_list = list(postags)
print('\t'.join(postags))


# In[29]:


arcs = parser.parse(words_list, postags_list)  # 句法分析
print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
arcs_list = list(arcs)


# In[30]:


roles = labeller.label(words, postags, arcs)  # 语义角色标注

# 打印结果
for role in roles:
    print(role.index, "".join(["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))


# In[31]:


# 写两个函数，函数使用来加标点符号的
def ques_punctuation(ques_sen):# 问句的标点符号
    #判断问句的最后一位的标点
    if len(ques_sen) > 0:
        if ques_sen[-1] in ['，', '。','；']:# 说明句子的最后一位是有标点的，但不是问号
            ques_sen = ques_sen[:-1] + '？'
        elif ques_sen[-1] not in ['，','。','？','；','！']:# 句子最后没有标点结尾的
            ques_sen = ques_sen + '?'
    else:
        print('异常')
    return ques_sen
    

def ans_punctuation(ans_sen):
    #判断问句的最后一位的标点
    if len(ans_sen) > 0:
        if ans_sen[-1] in ['，', '？','；']:# 说明句子的最后一位是有标点的，但不是句号
            ans_sen = ans_sen[:-1] + '。'
        elif ans_sen[-1] not in ['，','。','？','；','！']:# 句子最后没有标点结尾的
            ans_sen = ans_sen + '。'
    else:
        print('异常')
        
    return ans_sen


# In[33]:


# 因为所以的问题
prp_start = prp_end = dis_start = dis_end = -1
purpose_flag = True #假设他是一个因为所以的问句 
# 因为所以的问题
for role in roles:
    for arg in role.arguments:
        # 里面有因为
        if arg.name == 'PRP':
            prp_start = arg.range.start
            prp_end = arg.range.end
        # 所以
        if arg.name == 'DIS':
            dis_start = arg.range.start
            dis_end = arg.range.end

if prp_start >=0 and dis_start <0:# 说明只有因为
    # 如果缺的话只能去补，怎么补呢？？？
    print('只有因为')
elif prp_start < 0 and dis_start >= 0:# 说明只有所以
    print('只有所以')
elif prp_start >=0 and dis_start >=0:# 因为所以都有
    # 使用浅拷贝的方式，因为原来的直接赋值，两个数组是内存地址相同的，只要一个改变，另一个也会改变
    sen = list(words_list)
    # 把从因为到所以的所有字替换成，为什么
    sen[prp_start:dis_end+1] = '为什么'
    question_sen = ''
    for i in sen:
        question_sen += i
    question_sen = ques_punctuation(question_sen)
    print(question_sen)# 最终的疑问句

    sen = list(words_list)
    answer_sen = ''    
    for i in sen[prp_start:dis_start]:
        answer_sen += i
    answer_sen = ans_punctuation(answer_sen)
    print(answer_sen)# 最终的答案的陈述句
else:# 说明不是因为所以的句子，可以用于其他的判断去了
    purpose_flag = False


# In[34]:


# 这个是判断地点的问题
# 与地点搭配的介词
preposition = ['在','从','往','沿着','至']
loc_start = loc_end = -1
loc_flag = True# 设置可以提问关于地点的问题
prepos_flag = False
for role in roles:
    for arg in role.arguments:
        # 地点词
        if arg.name == 'LOC':
            loc_start = arg.range.start
            loc_end = arg.range.end
            
# 在什么地方，什么地方
if loc_start >=0:
    sen = list(words_list)
    # 把地点名词组换成 在哪里
    # 查看是否有介词在短语中
    for word in sen[loc_start:loc_end+1]:
        if word in preposition:
            prepos_flag = True
            prepos_word = word
    # 有介词
    if prepos_flag:
        sen[loc_start:loc_end+1] = prepos_word + '哪里'
    else:# 没有介词
        sen[loc_start:loc_end+1] = '哪里'
    # 疑问句   
    question_sen = ''
    for i in sen:
        question_sen += i
    # 疑问句的标点   
    question_sen = ques_punctuation(question_sen)
    print(question_sen)# 最终的疑问句
    
    
    sen = list(words_list)
    # 陈述句
    answer_sen = ''
    for i in sen[loc_start:loc_end+1]:
        # 判断下答案中有没有介词
        if prepos_flag:# 如果有介词的话
            # 跳过这次循环
            continue
    else:# 没有介词，直接是答案
        answer_sen += i
    answer_sen = ans_punctuation(answer_sen)
    print(answer_sen)# 最终的答案
else:
    loc_flag = False#没有这种的问题


# In[35]:


# 方式的问题，通过什么方式，完成了什么
# 使用的介词：通过，按照，以，凭，本着
preposition = ['通过','按照','以','凭','本着','拿','用']
way_start = way_end = -1
way_flag = True# 设置可以提问关于方式的问题
prepos_flag = False
for role in roles:
    for arg in role.arguments:
        # 方式词
        if arg.name == 'MNR':
            way_start = arg.range.start
            way_end = arg.range.end
            
# 通过什么方式，什么方式
if way_start >=0:
    sen = list(words_list)
    # 把方式词组换成 介词+什么方式
    # 查看是否有介词在短语中
    
    for word in sen[way_start:way_end+1]:
        if word in preposition:
            prepos_flag = True
            prepos_word = word
    # 有介词
    if prepos_flag:
        sen[way_start:way_end+1] = prepos_word + '什么方式'
    else:# 没有介词
        sen[way_start:way_end+1] = '什么方式'
        
    # 疑问句
    question_sen = ''
    for i in sen:
        question_sen += i
    question_sen = ques_punctuation(question_sen)
    print(question_sen)# 最终的疑问句
    
    sen = list(words_list)
    # 陈述句的标点
    answer_sen = ''
    for i in sen[way_start:way_end+1]:
        # 判断下答案中有没有介词
        if i in preposition:# 如果有介词的话
            # 跳过这次循环
            continue
        else:# 没有介词，直接是答案
            answer_sen += i
    answer_sen = ans_punctuation(answer_sen)
    print(answer_sen)# 最终的答案
else:
    way_flag = False#没有这种的问题


# In[36]:


# 判断时间的问题
# 与地点搭配的介词
preposition = ['在','当']
tmp_start = tmp_end = -1
tmp_flag = True# 设置可以提问关于地点的问题
prepos_flag = False
for role in roles:
    for arg in role.arguments:
        # 时间词
        if arg.name == 'TMP':
            tmp_start = arg.range.start
            tmp_end = arg.range.end
            
if tmp_start >=0:
    sen = list(words_list)
    # 把地点名词组换成 在哪里
    # 查看是否有介词在短语中
    for word in sen[tmp_start:tmp_end]:
        if word in preposition:
            prepos_flag = True
            prepos_word = word
    # 有介词
    if prepos_flag:
        sen[tmp_start:tmp_end+1] = prepos_word + '什么时候'
    else:# 没有介词
        sen[tmp_start:tmp_end+1] = '什么时候'
    # 疑问句   
    question_sen = ''
    for i in sen:
        question_sen += i
    # 疑问句的标点   
    question_sen = ques_punctuation(question_sen)
    print(question_sen)# 最终的疑问句
    
    
    sen = list(words_list)
    # 陈述句
    answer_sen = ''
    for i in sen[tmp_start:tmp_end+1]:
        answer_sen += i
    answer_sen = ans_punctuation(answer_sen)
    print(answer_sen)# 最终的答案
else:
    loc_flag = False#没有这种的问题


# In[37]:


# 对动作的提问
# A0 xxx 了A1
a0_start = a0_end = -1
a1_start = a1_end = -1
act_flag = True# 设置可以提问关于动作的问题
role_num = -1# 设置role的index
for role in roles:
    for arg in role.arguments:
        # 地点词
        if arg.name == 'A0':
            a0_start = arg.range.start
            a0_end = arg.range.end
            role_num = role.index
        if arg.name == 'A1' and role.index == role_num:# 检查a0和a1是不是在同一个role下面
            a1_start = arg.range.start
            a1_end = arg.range.end
            
        
# 防止问句重复
if a0_start >= 0 and a1_start >= 0:
    sen = list(words_list)
    # 查看是否有介词在短语中

    sen[a1_start:a1_end+1] = '什么'

    # 疑问句   
    question_sen = ''
    for i in sen:
        question_sen += i
    # 疑问句的标点   
    question_sen = ques_punctuation(question_sen)
    print(question_sen)# 最终的疑问句


    sen = list(words_list)
    # 陈述句
    answer_sen = ''
    for i in sen[a1_start:a1_end+1]:
        answer_sen += i
    answer_sen = ans_punctuation(answer_sen)
    print(answer_sen)# 最终的答案
else:
    act_flag = False#没有这种的问题   

