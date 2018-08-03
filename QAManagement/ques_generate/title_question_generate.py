
# coding: utf-8

# In[1]:


import os
from pyltp import SementicRoleLabeller
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
import json
import re


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


# 读取抽取好的json文件
# 遍历上传的文件夹中所有的文件
# 还需要判断上传的是文件夹目录还是文件
path = "../data/havetable" #文件夹目录 
files= os.listdir(path) #得到文件夹下的所有文件名称  
urls = []  
for file in files: #遍历文件夹  
     if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开  
          urls.append(path+"/"+file)
#print(urls) #打印结果  
print(len(urls))


# In[7]:


# 读取疑问词的文件
ques_word_file = open('../data/question_word.txt')
ques_words_list = []
for line in ques_word_file:
    ques_words_list.append(line.strip('\n'))
#print(ques_words_list)


# In[9]:


common_json = []# 正常的标题的json
QA_json = []# 是疑问句的标题的json
json_all = []
is_question_title = False# 疑问句标志
# 打开这些文件
for url in urls:
    QA_dict = {}
    file = open(url)
    for line in file.readlines():
        dic = json.loads(line)
        
        json_all.append(dic)# 全部的json存入一个数组
        
        # 抽出文件的标题
        title = dic['title'].strip().strip("\n")        # 对title的格式进行处理，去掉空格和换行
        if title == '':# 文章的标题可能因为一些关系没有抽取出来
            if len(dic['subject'])  > 0 :
                title = dic['subject'][-1].strip().strip("\n")
                
        #1.对标题的判断，判断他是疑问句还是普通的名词
        #2.将疑问句和他的标题内容直接存入QA对中
        #3.对还是名词的词进行更加高级的处理
        
        # 对title进行分类，有些title是名词，有些是疑问句
        words = segmentor.segment(title)# 分词
        words_list = list(words)
        # 根据疑问词判断这句话是不是疑问句，但是有些疑问句中没有用到疑问词，于是就使用最末尾的 ？做判断
        for i in words_list:
            if i in ques_words_list or i == '？' or i == '?':
                is_question_title = True
                break# 一旦有一个判断出了True直接跳出循环
            else:
                is_question_title = False
                
        if is_question_title:# 如果是疑问句
            # 辣么这些title可以直接存入QA对中
            QA_dict['question'] = title
            QA_dict['answer'] = dic['titlecontent']
            if 'link' in dic.keys():
                QA_dict['answer_link'] = dic['link']
            else:
                QA_dict['answer_link'] = ''
            if 'subject' in dic.keys():
                QA_dict['subject'] = dic['subject'][1]
            else:
                QA_dict['subject'] = ''
            QA_json.append(QA_dict)
        else:# 如果不是疑问句
            # 辣么就将这些不是疑问句标题的json存入正常标题json的数组中
            common_json.append(dic)


# In[10]:


print(len(QA_json))


# In[11]:


# 下面是对正常的标题的提问
# 标题的提问主要需要拼接问题，需要将以前的链接上的字段拼上去
# 最后就是根据标题的内容选择疑问词，主要有 
# 列表类（有哪些）、定义类（是什么）、方法类（如何操作）
a = 0
print(len(common_json))
for i in range(len(common_json)):
    if 'subject' in common_json[i].keys() and len(common_json[i]['subject']) > 0 :
        #print(common_json[i]['subject'])
        a = a + 1
print(a)


# In[12]:


# 初步的想法是列表第二个与最后一个的组合，列表第二个是最大的类别，最后一个是最具体的类别
# 感觉需要对最后一个进行句法分析，要通过这个选择合适的疑问词
# 如果页面里面有小标题，那么就是大标题加小标题
# 如果没有小标题，那么就是直接大标题，主要考虑的是是否需要前缀的连接名词，也就是大标题的前置标题
# 进行了依存句法分析，只要里面缺少SBV主谓关系的，可以认为是缺少主语的

# 对大标题的提问，分为两类，定义类（没有VOB动宾关系的词）、操作类（如何，有VOB动宾关系的词）
VOB_flag = False# VOB的标志为False
# 简单的拼接
common_QA_dict = {}
for i in range(len(common_json)):
    # 抽出文件的标题
    title = common_json[i]['title'].strip()        # 对title的格式进行处理，去掉空格和换行
    if title == '':# 文章的标题可能因为一些关系没有抽取出来
        if 'subject' in common_json[i].keys() and len(common_json[i]['subject'])  > 0 :
            title = dic['subject'][-1].strip().strip("\n")
            
    words = segmentor.segment(title)# 分词
    #print(' '.join(words))
    words_list = list(words)

    postags = postagger.postag(words_list)  # 词性标注
    postags_list = list(postags)
    #print('\t'.join(postags))

    arcs = parser.parse(words_list, postags_list)  # 句法分析
    #print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
    for arc in arcs:
        if arc.relation == 'VOB':# 词里面有动宾关系，可以提问如何xxx
            VOB_flag = True
        else:
            VOB_flag = False
            
    if VOB_flag:
        if 'subject' in common_json[i].keys() and len(common_json[i]['subject']) > 0:
            splicing = common_json[i]['subject'][1] + '如何' + common_json[i]['subject'][-1]
            # 简单的拼接之后，加入疑问词，是什么
            question = splicing + '？'
            subject = common_json[i]['subject'][1]
        else:
            question = '如何' + common_json[i]['title'] + '？'
            subject = common_json[i]['title']
    else:
        if 'subject' in common_json[i].keys() and len(common_json[i]['subject']) > 0:
            splicing = common_json[i]['subject'][1] + '的' + common_json[i]['subject'][-1]
            # 简单的拼接之后，加入疑问词，是什么
            question = splicing + '是什么？'
            subject = common_json[i]['subject'][1]
        else:
            question = common_json[i]['title'] + '是什么？'
            subject = common_json[i]['title']

    if 'link' in common_json[i].keys():
        link = common_json[i]['link']
    else:
        link = ''

    if common_json[i]['titlecontent'].strip() != '':
        answer = common_json[i]['titlecontent']
        common_QA_dict['question'] = question
        common_QA_dict['answer'] = answer
        common_QA_dict['answer_link'] = link
        common_QA_dict['subject'] = subject
        #print(common_QA_dict)
        QA_json.append(common_QA_dict)
    #print(common_QA_json)


# In[13]:


print(len(QA_json))


# In[15]:


# 对子标题进行提问
# 子标题应该与大标题的提问方式一致
# 首先判断子标题的类型，是定义类的，还是操作类的
subtitle_VOB_flag = False# VOB的标志为False
# 简单的拼接
common_QA_dict = {}
for i in range(len(common_json)):
    # 抽出文件的标题
    title = common_json[i]['title'].strip()        # 对title的格式进行处理，去掉空格和换行
    if title == '':# 文章的标题可能因为一些关系没有抽取出来
        if 'subject' in common_json[i].keys() and len(common_json[i]['subject'])  > 0 :
            title = dic['subject'][-1].strip().strip("\n")
            
    num_subtilte = 0# subtilte的个数
    pattern = re.compile(r'subtitle')
    
    for json in common_json[i].keys():
        if len(pattern.findall(json)) != 0:
            num_subtilte += 1
    #print(num_subtilte)
    
    if num_subtilte > 0:
        for num in range(num_subtilte):
            #subtitle = common_json[i]['subtitle' + str(num + 1)]
            subtitle = re.sub(r'<.*?>', '', common_json[i]['subtitle' + str(num + 1)].strip())
            answer = common_json[i]['subcontent' + str(num + 1)].strip()
            #print(subtitle.strip())
            words = segmentor.segment(subtitle)# 分词
            words_list = list(words)

            postags = postagger.postag(words_list)  # 词性标注
            postags_list = list(postags)

            arcs = parser.parse(words_list, postags_list)  # 句法分析

            for arc in arcs:
                if arc.relation == 'VOB':# 词里面有动宾关系，可以提问如何xxx
                    subtitle_VOB_flag = True
                else:
                    subtitle_VOB_flag = False


            if subtitle_VOB_flag:
                # 动作类的提问，加入如何
                if 'subject' in common_json[i].keys() and len(common_json[i]['subject']) > 0:
                    splicing = common_json[i]['subject'][1] + '中' + common_json[i]['subject'][-1] + '如何' + subtitle
                    question = splicing + '？'
                    subject = common_json[i]['subject'][1]
                else:
                    question =  common_json[i]['title'] + '如何' + subtitle +  '？'
                    subject = common_json[i]['title']
            else:
                if 'subject' in common_json[i].keys() and len(common_json[i]['subject']) > 0:
                    splicing = common_json[i]['subject'][1] + common_json[i]['subject'][-1] + '的' + subtitle
                    # 简单的拼接之后，加入疑问词，是什么
                    question = splicing + '是什么？'
                    subject = common_json[i]['subject'][1]
                else:
                    question = common_json[i]['title'] + '的' + subtitle + '是什么？'
                    subject = common_json[i]['title']

            if 'link' in common_json[i].keys():
                link = common_json[i]['link']
            else:
                link = ''

            if common_json[i]['titlecontent'].strip() != '':
                #answer = common_json[i]['titlecontent']
                common_QA_dict['question'] = question
                common_QA_dict['answer'] = answer
                common_QA_dict['answer_link'] = link
                common_QA_dict['subject'] = subject
                print(common_QA_dict)
                QA_json.append(common_QA_dict)


# In[16]:


print(len(QA_json))

