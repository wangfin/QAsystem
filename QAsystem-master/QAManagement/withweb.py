import heapq
from QAManagement.elas import Elas
from QAManagement.elas_f_k1 import k1
from QAManagement.elas_f_k2 import k2
from .models import UserMining
import datetime,time,calendar
myelas = Elas()
myk1 = k1()
myk2 = k2()
# import elas
#
# myelas = elas.Elas()
####插入
# myelas.init('index35')




class Withweb(object):
    questionlist=[]
    ques_num=0
    favorsub=''
    sublist=[]
    tend=''
    qbefore=''
    def __init__(self, myip):
        self.ip = myip # 注意在实例化 时，要调用ip获取函数

    '''def searchallk1(self,myindex):
        res= myk1.searchall(myindex)
        return res

    def searchallk2(self,myindex):
        res=myk2.searchall(myindex)
        return res
'''
    def accurate_search(self, amyindex, aq, index_k1, index_k2,userattention,userlike,times):
        usermsg = {}
        source = myelas.accuratesearch(amyindex, aq)
        if source != None:
            answer = source['answer']
            sub = source['subject']
            myk1.insert(index_k1, aq)
            myk2.insert(index_k2, sub)
            source['ip']=self.ip
            # 用户信息写入数据库
            usermsg['userip']=self.ip
            usermsg['userquestion']=source['question']
            usermsg['usersub']=source['subject']
            usermsg['userattention']=userattention
            #usermsg['usercollect']=usercollect
            usermsg['userlike']=userlike
            usermsg['times']=times
            UserMining.objects.create(**usermsg)
            return source['answer']
        else:
            return None

    def buwan_search(self,myindex,q,qbefore):
        # 补完搜索阶段
		# 创建返回结果集
        results = []
        # 如果有，显示五个
        # 返回的是相近的问题
        if (myelas.multisearch(myindex,q,qbefore)):

            for hit in myelas.multisearch(myindex, q,qbefore):  # 根据打分返回查询，并且前三个/前五个

                results.append(hit['_source']['question'])

            return results

    ############enter搜索阶段
    def enter_search(self,myindex,q,index_k1,index_k2,qbefore,userattention,userlike,times):

        if (myelas.multisearch(myindex, q,qbefore)):
            ###先找到最大值，再把它和其他四个比较，如果大于，直接返回，否则：
            maxscore = 0
            maxanswer = ''
            maxsub=''
            maxq=''
            totalscore = 0
            maxsource={ }
            results = []
            for hit in myelas.multisearch(myindex,q,qbefore):  #####只有五个
                totalscore = totalscore + hit['_score']

                if hit['_score'] > maxscore:
                    maxsource=hit['_source']
                    maxscore = hit['_score']
                    maxanswer = hit['_source']['answer']
                    maxsub = hit['_source']['subject']
                    maxq = hit['_source']['question']
                #print(hit['_score'])

            #print(totalscore)
            if maxscore > 0.35*totalscore :#####由一半，修改为0.35
                #results.append(maxanswer)
                myk1.insert(index_k1,maxq)
                myk2.insert(index_k2,maxsub)
                maxsource['ip']=self.ip
                # 用户信息写入数据库
                usermsg = {}
                usermsg['userip'] = self.ip
                usermsg['userquestion'] = maxq
                usermsg['usersub'] = maxsub
                usermsg['userattention'] = userattention
                # usermsg['usercollect'] = usercollect
                usermsg['userlike'] = userlike
                usermsg['times'] = times
                UserMining.objects.create(**usermsg)
                return maxanswer
            else:
                #######显示五个
                for hit in myelas.multisearch(myindex,  q,qbefore):  # 根据打分返回查询，并且前三个/前五个
                    #print(hit['_source']['answer'])
                    results.append(hit['_source']['question'])
                return results



        ##如果点了都不是
        else:
            #print('查询不到结果，请您重新输入')
            result = '根据您搜索的内容，查询不到结果，请您重新输入'
            return result

    def further_search(self,myindex,preq,qbefore):
        results = []
        #######进一步推荐搜索
        if (myelas.furthersearch(myindex, preq,qbefore)):


            #######显示五个
            for hit in myelas.furthersearch(myindex, preq,qbefore):  # 根据打分返回查询，并且前三个/前五个

                results.append(hit['_source']['question'])

            return results

        ##如果点了都不是
        else:
            return results





# 1.从数据库中读出某个ip的所有问题，返回值为数组，元素为问题
    def search_ipq(self):
        # 读出某个ip所有记录
        usermsgread = UserMining.objects.filter(userip=self.ip)
        all_question =[]
        for i in usermsgread:
            all_question.append(i['userquestion'])
        return all_question
# 获得问题总数,其中参数l为all_question，返回值为问题数量
    def sum_q(self,l):
        ques_num = len(l)
        return ques_num
# 获得近五条问题，返回值为数组，元素为五条问题
    def recent_5q(self):
        q_list=[]
        usermsgread = UserMining.objects.filter(userip=self.ip)
        l1 = heapq.nlargest(5, usermsgread, key=lambda s: s['times'])
        for i in l1:
            q_list.append(i['userquestion'])
        return q_list
# 获得近一月问题，返回值为数组，元素为问题
    def mouth_q(self):
        time_temp = time.strftime("%Y-%m-%d %H:%M:%S",
                                  time.localtime())  #########################要再加一个usermsgread日期格式的转换
        dt = datetime.date(int(time_temp[0:4]), int(time_temp[5:7]), int(time_temp[8:10]))
        usermsgread = UserMining.objects.filter(userip=self.ip)
        for i in usermsgread:
            time_temp = i['times']
            i['times'] = datetime.date(int(time_temp[0:4]), int(time_temp[5:7]), int(time_temp[8:10]))
        res = []
        temp_dict = {}
        for item in usermsgread:
            temp_dict['question'] = item['userquestion']
            temp_dict['time'] = item['times']
            str1 = str(temp_dict)
            temp = eval(str1)
            res.append(temp)

        month = dt.month - 1 - 1
        year = int(dt.year + month / 12)
        month = int(month % 12 + 1)
        day = min(dt.day, calendar.monthrange(year, month)[1])
        dt = dt.replace(year=year, month=month, day=day)
        onemonth = []
        for j in res:
            if j['time'] > dt:
                onemonth.append(j['question'])
        return onemonth

# 2.读出所有主题列表，返回值为数组，元素为主题
    def search_sub(self):
        sublist = []
        usermsgread = UserMining.objects.filter(userip=self.ip)
        for i in usermsgread:
            sublist.append(i['usersub'])
        return sublist

# 得出最优主题,其中参数l为sublist，返回值为最感兴趣主题
    def best_sub(self,l):
        myset = set(l)
        temp_dict = {}
        max_num = 0
        max_subject = ''
        for item in myset:
            # print("the %d has found %d" %(item,mylist.count(item)))
            temp_dict['subject'] = item
            temp_dict['num'] = l.count(item)
            if temp_dict['num'] > max_num:
                max_num = temp_dict['num']
                max_subject = temp_dict['subject']
        return max_subject

# 主题占比，其中参数l为sublist，返回值为数组（元素为字典,包含了问题question,数量num，和占比shares）
    def sub_divide(self,l):
        res = []
        myset = set(l)
        temp_dict = {}
        sum = len(l)

        for item in myset:
            # print("the %d has found %d" %(item,mylist.count(item)))
            temp_dict['subject'] = item
            temp_dict['num'] = l.count(item)
            temp_dict['shares'] = '{:.2%}'.format(temp_dict['num'] / sum)
            # print(type(temp_dict['num']))
            str1 = str(temp_dict)
            temp = eval(str1)
            res.append(temp)
        res = heapq.nlargest(4, res, key=lambda s: s['num'])
        else_sub = sum
        for sub_4 in res:
            else_sub = else_sub - sub_4['num']
            print(sub_4, else_sub, sum)
        temp_dict['subject'] = '其他'
        temp_dict['num'] = else_sub
        temp_dict['shares'] = '{:.2%}'.format(temp_dict['num'] / sum)
        str1 = str(temp_dict)
        temp = eval(str1)
        res.append(temp)
        return res

    #def sub_like(self,l,s):
    #usermsgread = UserMining.objects.filter(userip=self.ip)
# 3.读出用户倾向列表，返回值为数组，元素为主题
    def searchtend(self):
        #sublist = []
        tendlist = []
        usermsgread = UserMining.objects.filter(userip=self.ip)
        for i in usermsgread:
            tendlist.append(i['userattention'])
        return tendlist
# 得出用户倾向，参数l为tendlist，返回值为数组，元素为两类意图的百分数
    def get_tend(self,l):
        res=[]
        chat_num=l.count('闲聊')
        ask_num=l.count('提问')
        sum=len(l)
        chat='{:.2%}'.format(chat_num / sum)
        res.append(chat)
        ask='{:.2%}'.format(ask_num / sum)
        res.append(ask)
        return res

#4 读出收藏与否列表

#5 读出喜欢与否列表

#6 读出用户提问时间

# 近五个问题，跟时间有关
# 近五个月最感兴趣的主题



# 还缺的：查询时的数据库插入和数据分析；把上下文的整合到elas里；ip获得；注意withweb两个类的使用范围
