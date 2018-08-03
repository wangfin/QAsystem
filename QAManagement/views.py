import datetime
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.db.models import Count
import json

from urllib.parse import urlencode

from .models import User,QuestionCount
import time
from .withweb import Withweb
import os
from apscheduler.schedulers.background import BackgroundScheduler
from django.db import connection
import urllib
import requests
# Create your views here.

# 引入两个算法程序
from QAManagement.webextract import hauwei_extractor,moban_extractor
import sre_constants
from QAManagement.ques_generate import QG_paragraph,QA_save
import logging

logger = logging.getLogger(__name__)

# 设置一个全局变量，这个是es的表
myindex = 'qa_test'
# qa_init qa_initial
# qa_sys
# qs_store
# qa_real
# 选择的文件列表
file_list = []
# 生成的QA对列表
result_list = []

def index(request):
    #return HttpResponse("HelloWorld")
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    # 存入日志
    logger.info('访问者IP：' + ip)

    return render(request,"index.html")
def QAManagement(request):
    return render(request,"QAManagement.html")
def QAManage(request):
    # qa_results = []
    # data_json = {}
    # withweb = Withweb()
    # result = withweb.searchall(myindex)
    # for i in range(len(result)):
    #     qa_result = {}
    #     qa_result['id'] = result[i]['_id']
    #     qa_result['question'] = result[i]['_source']['question']
    #     qa_result['answer'] = result[i]['_source']['answer']
    #     qa_result['link'] = result[i]['_source']['link']
    #     qa_result['subject'] = result[i]['_source']['subject']
    #
    #     qa_results.append(qa_result)
    #
    # data_json['datas'] = qa_results
    # data_json['total'] = len(qa_results)
    #
    # #return HttpResponse(json.dumps(data_json))
    # return render(request,"QAManage.html",{'data_json':data_json})
    return render(request, "QAManage.html")
def Regsiter(request):
    return render(request,"register.html")
def Login(request):
    return render(request,"firstPage.html")
def userPage(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    # 存入日志
    logger.info('访问者IP：' + ip)

    return render(request,"UserPage.html")
def upload(request):
    if request.method == 'POST':
        #file_obj = request.FILES.get('fileupload')
        file_obj = request.FILES['file']
        # 这里一开始写反了
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))


        f = open(os.path.join(BASE_DIR, 'static', 'document', file_obj.name), 'wb+')

        # 存入日志
        logger.info(file_obj.name)
        # print(file_obj,type(file_obj))
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        success={'success':'OK'}
        return HttpResponse(json.dumps(success),content_type="application/json")

def search_all(request):
    if request.method == 'POST':
        offset = request.POST.get("pageSize")
        limit = request.POST.get("pageIndex")
        qa_results = []
        data_json = {}
        withweb = Withweb()
        result = withweb.searchall(myindex)
        for i in range(len(result)):
            qa_result = {}
            qa_result['id'] = result[i]['_id']
            qa_result['question'] = result[i]['_source']['question']
            qa_result['answer'] = result[i]['_source']['answer']
            qa_result['link'] = result[i]['_source']['link']
            qa_result['subject'] = result[i]['_source']['subject']

            qa_results.append(qa_result)

        data_json['rows'] = qa_results[(int(limit)-1)*int(offset):int(limit)*int(offset)]
        data_json['total'] = len(qa_results)


        return HttpResponse(json.dumps(data_json))
    else:
        return HttpResponse("add wrong")

def Add(request):
    if request.method == 'POST':
        jsondata = request.POST.get("jsondata")
        received_json_data = json.loads(jsondata)
        id = received_json_data['问题编号']
        question = received_json_data['具体问题']
        answer = received_json_data['答案']
        link = received_json_data['答案链接']
        subject = received_json_data['主题']

        # 存入日志
        logger.info(received_json_data)

        withweb = Withweb()
        result = withweb.webinsert(myindex,question,question,answer,link,subject,id)

        # print(result)
        return HttpResponse("add ok")
    else:
        return HttpResponse("add wrong")

def modify(request):
    if request.method == 'POST':
        jsonchangeddata = request.POST.get("jsondata")
        received_json_changed_data = json.loads(jsonchangeddata)
        id = received_json_changed_data['问题编号']
        question = received_json_changed_data['具体问题']
        answer = received_json_changed_data['答案']
        link = received_json_changed_data['答案链接']
        subject = received_json_changed_data['主题']

        # 存入日志
        logger.info(received_json_changed_data)

        #print(id,question,answer,link,subject)
        withweb = Withweb()

        withweb.update(myindex,question,answer,link,subject,id)

        return HttpResponse("modify ok")
    else:
        return HttpResponse("modify wrong")

def search(request):
    if request.method=='POST':
        search_id = request.POST.get("search_id")
        search_question = request.POST.get("search_question")
        qa_results = []
        data_json = {}
        withweb = Withweb()

        if search_question !='':
            print('标题为不空')

        if search_id != '' and search_question == '':
            result = withweb.search_by_id(myindex, search_id)

        elif search_question != '':
            result = withweb.search_by_question(myindex, search_question)
            print(result)

        for i in range(len(result)):
            qa_result = {}
            qa_result['id'] = result[i]['_id']
            qa_result['question'] = result[i]['_source']['question']
            qa_result['answer'] = result[i]['_source']['answer']
            qa_result['link'] = result[i]['_source']['link']
            qa_result['subject'] = result[i]['_source']['subject']

            qa_results.append(qa_result)

        data_json['rows'] = qa_results
        data_json['total'] = len(qa_results)

        # 存入日志
        logger.info(data_json)

        return HttpResponse(json.dumps(data_json))


def delete(request):
    if request.method=='POST':
        delKey = request.POST.get("del_key")
        json_key = json.loads(delKey)
        withweb = Withweb()
        for key in json_key:
            withweb.single_delete(myindex, key)

        return HttpResponse("del OK")
    else:
        return HttpResponse("del error")

def userQuestion(request):
    if request.method=='POST':
        user_question = request.POST.get("userQuestion")


        # 获取本地时间
        Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #print(Time)
        uq = {'userquestion':user_question,'question_time':Time}

        # 存入日志
        logger.info(uq)
        User.objects.create(**uq)
        return HttpResponse("数据库保存成功")

# def Associate(request):
#     if request.method=='POST':
#         userimagine = request.POST.get("userImagine")
#         imgAnswer1 = "Imgine1"
#         imgAnswer2 = "Imgine2"
#         imgAnswer3 = "Imgine3"
#         imgAnswer4 = "Imgine4"
#         imgAnswer5 = "Imgine5"
#         return HttpResponse(json.dumps({
#             'imgA1':imgAnswer1,
#             'imgA2':imgAnswer2,
#             'imgA3':imgAnswer3,
#             'imgA4':imgAnswer4,
#             'imgA5':imgAnswer5
#         }))
#     else:
#         return HttpResponse("imagine false")

# def usermayask(request):
#     if request.method=='POST':
#         mayask1 = "ask1"
#         mayask2 = "ask2"
#         mayask3 = "ask3"
#         mayask4 = "ask4"
#         mayask5 = "ask5"
#         return HttpResponse(json.dumps({
#         'mayask1':mayask1,
#         "mayask2":mayask2,
#         "mayask3":mayask3,
#         "mayask4":mayask4,
#         "mayask5":mayask5
#     }))
#     else:
#         return HttpResponse("mayask false")

# 这个是用户的补完查询，当用户开始输入字的时候，调用补完查询
# 返回查询的准确问题
def completion_search(request):
    if request.method=='POST':
        user_question = request.POST.get("completion_Question")
        #print(user_question)
        withweb = Withweb()
        questions = withweb.buwan_search(myindex,user_question)
        #print(questions)
        # 答案字典
        ques_dict = {}
        if questions != None:# 答案不为空
            for i in range(len(questions)):
                ques_dict['question' + str(i)] = questions[i]
            result_json = json.dumps(ques_dict)
        #return HttpResponse(result_json)
        else:
            result_json = json.dumps({
                'result1': ''
            })
        #return HttpResponse("imagine false")
        # 存入日志
        for value in ques_dict.values():
            logger.info('补全查询输入问题：' + user_question + '|||' + '补全查询返回结果：' + value)
        return HttpResponse(result_json)
# 用户点击的发送按钮的查询
# 返回的结果分为两种，第一种是当某一个答案的评分超过其他几个答案的评分，那么就返回一个
# 如果评分相同，那么就返回五个
def enter_search(request):
    isclear = 4
    if request.method == 'POST':
        user_question = request.POST.get("enter_Question")
        print(user_question)
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': '3d5f8b1b8a5f4adeaf0a5646fd2634c1',
        }

        params = urllib.parse.urlencode({
            # Query parameter
            'q': user_question,
            # Optional request parameters, set to default values
            'timezoneOffset': '0',
            'verbose': 'true',
        })
        try:
            r = requests.get(
                'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/5f7d357a-7c28-4891-b4dc-d810f8b564ef',
                headers=headers, params=params)
            res = r.json()
            maxscore = 0
            for intent in res["intents"]:
                if (intent["score"] >= maxscore):
                    maxscore = intent["score"]
                    userintent = intent["intent"]
            if userintent == "闲聊":
                # 调用图灵机器人
                url = "http://www.tuling123.com/openapi/api"
                params2 = {
                    "key": "588d7fd064554687b34f0568c107efae",
                    "info": request.POST.get("enter_Question"),
                    "userid": "123456"
                }
                params2 = urlencode(params2)
                f = urllib.request.urlopen("%s?%s" % (url, params2))

                content = f.read()
                res = json.loads(content)
                if res:
                    # error_code = res["intent"]["code"]
                    error_code = res["code"]
                    if ((error_code == 40001 & error_code != 40002) & error_code != 40004) & error_code != 40007:
                        # 成功请求
                        print(res["text"])
                        # res["result"]["values"]
                        result_json = json.dumps(
                            {
                                "isclear": isclear,
                                "answer": res["text"],
                            })
                    else:
                        print("%s" % (res["code"]))
                        result_json = json.dumps(
                            {
                                "isclear": isclear,
                                "answer": "对不起，小Q出现了一点问题QAQ",
                            })
                else:
                    # print"request api error"
                    result_json = json.dumps(
                        {
                            "isclear": isclear,
                            "answer": "error",
                        })
            elif userintent == "提问":
                # user_question = request.POST.get("enter_Question")

                # print(user_question)
                withweb = Withweb()
                accurate_result = withweb.accurate_search(myindex, user_question)

                if accurate_result != None:
                    print(accurate_result)
                    result_json = json.dumps({
                        'isclear': 1,
                        'answer': accurate_result
                    })
                    # return accurate_result
                else:
                    result = withweb.enter_search(myindex, user_question)
                    # print(len(result))# 1-问题明确 2-问题模糊 3-问题极度模糊
                    if len(result) == 5:  # 当用户问的不明确时，返回五个相似的问题
                        isclear = 2
                    elif len(result) == 1:  # 当用户问题很明确的时候，返回一个明确的答案
                        isclear = 1
                    ques_dict = {}
                    if (isclear == 1):
                        question_time_today = datetime.date.today()
                        question_time_now = time.strftime(" %H:%M:%S")
                        Time = str(question_time_today) + question_time_now

                        uq = {'userquestion': user_question, 'question_time': Time}
                        User.objects.create(**uq)

                        result_json = json.dumps({
                            "isclear": isclear,
                            "answer": result[0]
                        })
                    elif (isclear == 2):
                        # 模糊问题
                        for i in range(len(result)):  # 这里返回的是五个相似的问题
                            ques_dict['question' + str(i)] = result[i]
                        ques_dict['isclear'] = 'isclear'
                        result_json = json.dumps(ques_dict)
                    elif (isclear == 3):
                        result_json = json.dumps({
                            "isclear": isclear,
                            "answer": "对不起，匹配失败",
                        })

            else:
                result_json = json.dumps({
                    "isclear": isclear,
                    "answer": "QAQ 小Q没明白您的意思",
                })

        # 这个地方会报异常AttributeError: 'AttributeError' object has no attribute 'errno' 很迷。。。
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

        if isclear == 2:
            for value in ques_dict.values():
                logger.info('点击发送按钮输入：' + user_question + "|||" + '返回相似问题：' + value)
        else:# 存入日志
            logger.info('点击发送按钮输入：' + user_question + "|||" + '返回结果：' + json.loads(result_json)['answer'])
        return HttpResponse(result_json)

# 用户选择完问题的精确搜索
def accurate_search(request):
    if request.method == 'POST':
        user_question = request.POST.get("accurate_Question")
        #print('用户问题'+user_question)
        withweb = Withweb()
        answer = withweb.accurate_search(myindex, user_question)
        #print(answer)
        # 存入日志
        logger.info('精确搜索输入：' + user_question + '|||' + '回复答案：' + answer.strip())
        return HttpResponse(answer)

# 当用户提问完问题后，调用推荐提问
# 根据用户提出的问题，查询相似的问题，返回给用户
def further_search(request):
    if request.method == 'POST':
        user_question = request.POST.get("accurate_Question")
        withweb = Withweb()
        questions = withweb.further_search(myindex, user_question)
        #print(questions)
        ques_dict = {}
        if len(questions) > 0:  # 返回的推荐问题的数目不为空
            for i in range(len(questions)):
                ques_dict['question' + str(i)] = questions[i]
            result_json = json.dumps(ques_dict)
        else:
            result_json = ''

        # 存入日志

        for value in ques_dict.values():
            logger.info('推荐问题输入：' + user_question + '|||' + '返回：' + value)
        return HttpResponse(result_json)

def usermayask(request):
    if request.method=='POST':
        questions_dict = {}
        questions = QuestionCount.objects.all()
        i = 0
        for question in questions:
            questions_dict['mayask'+ str(i)] = question.userquestion
            questions_dict['count' + str(i)] = question.questioncount
            i = i + 1
        return HttpResponse(json.dumps(questions_dict))

# 聊天系统 没有集成是个假的
def chat(request):
    if request.method=='POST':
        question = request.POST.get("enter_Question")
        if question == '你好':
            result = "好啊，吃了么"
        elif question == 'QAQ':
            result = '怎么了'
        elif question == '很差劲':
            result = '很抱歉没有帮到您'
        elif question == '很棒':
            result = '很有幸为您带来了帮助'
        return HttpResponse(result)

# 运行算法程序
def Doexe(request):
    if request.method == 'POST':
        # 选择的解析模版
        modelName = request.POST.get("filename")

        myextract = hauwei_extractor.Extract()
        QA_generate = QG_paragraph.Paragraph()

        json_paths = []

        global file_list
        # print(file_list)

        for onehtml in file_list:

            onehtml = onehtml.strip("\"")

            # 基础文件系统
            BASE_DIR = os.path.abspath(os.path.dirname(__file__))
            # HTML上传的地址
            file_dir = os.path.join(BASE_DIR, 'static', 'document')

            mylink = onehtml

            onehtml = os.path.join(file_dir, onehtml)

            onehtml = open(onehtml, 'r', encoding="utf-8")

            # 导出的文件名为，原文件名，后缀为json
            onejson = mylink.replace('.html','.json')

            json_dir = os.path.join(BASE_DIR, 'static', 'json')

            jsonpath = os.path.join(json_dir, onejson)

            try:
                # 首先解析HTML文件，返回生成的json的文件名
                jsonname = myextract.inserthtml(onehtml, jsonpath, mylink)  ######此处写入的是变量

                if jsonpath != None:
                    json_paths.append(jsonname)
            except sre_constants.error:
                continue

        print('jsonpath:'+str(json_paths))

        # 然后运行QA对生成函数
        result = QA_generate.main(json_paths)

        # 存入日志
        logger.info(result)

        global result_list
        result_list = result
        # print(result)
        num = len(result)

        # 只有生成了QA对的时候才能存入
        if num > 0:
            # 存入数据库中
            saveines = QA_save.SaveInEs()
            for res in result:
                saveines.main(myindex,res)

        # if fileName == '华为云网页抽取模版':
        # time.sleep(60)

        result_json = json.dumps({
            "num": num,
            "qa": result,
        })

        return HttpResponse(result_json)
    else:
        return HttpResponse("失败")
# 获取在服务器上的文件名
def getfilename(request):
    if request.method == "POST":
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        file_dir = os.path.join(BASE_DIR, 'static', 'document')
        print(file_dir)
        for root, dirs, files in os.walk(file_dir):
            # print(root) #当前目录路径
            # print(dirs) #当前路径下所有子目录
            fileName = files  # 当前路径下所有非目录子文件
        return HttpResponse(json.dumps({
            "filenum": fileName.__len__(),
            "filename": fileName
        }))

# 选择文件
def choose_file(request):
    if request.method == 'POST':

        # file_list = []
        fileName = request.POST.get("filename")

        global file_list

        file_list = fileName.strip("[").strip("]").split(',')
        # print(file_list)
    return HttpResponse(json.dumps({
        "filenum": file_list.__len__(),
        "filename": file_list
    }))

# 显示生成的QA对页面
def show_result(request):
    global result_list
    # print(result_list)
    global file_list

    return render(request, "show_result.html", {"result_list":result_list,'length':len(file_list),'files':file_list})

# 创建模版来生成QA对
def create_model(request):
    if request.method == 'POST':
        data = request.POST.get("createdata")
        data = json.loads(data)
        begintitle = data["begintitle"]
        endtitle = data["endtitle"]
        littlebegintitle = data["littlebegintitle"]
        littleendtitle = data["littleendtitle"]
        tabbegin = data["tabbegin"]
        tabend = data["tabend"]
        imgbegin = data["imgbegin"]
        imgend = data["imgend"]
        topicalbegin = data["topicalbegin"]
        topicalend = data["topicalend"]
        description = data["description"]

        # print(data)

        myextract = moban_extractor.Extract(tabbegin,tabend,imgbegin,imgend,begintitle,endtitle,littlebegintitle,littleendtitle,topicalbegin,topicalend,description)

        QA_generate = QG_paragraph.Paragraph()

        json_paths = []

        global file_list
        # print(file_list)

        for onehtml in file_list:

            onehtml = onehtml.strip("\"")

            # 基础文件系统
            BASE_DIR = os.path.abspath(os.path.dirname(__file__))
            # HTML上传的地址
            file_dir = os.path.join(BASE_DIR, 'static', 'document')

            mylink = onehtml

            onehtml = os.path.join(file_dir, onehtml)

            onehtml = open(onehtml, 'r', encoding="utf-8")

            # 导出的文件名为，原文件名，后缀为json
            onejson = mylink.replace('.html', '.json')

            json_dir = os.path.join(BASE_DIR, 'static', 'json')

            jsonpath = os.path.join(json_dir, onejson)

            try:
                # 首先解析HTML文件，返回生成的json的文件名
                jsonpath = myextract.inserthtml(onehtml, jsonpath, mylink)  ######此处写入的是变量

                if jsonpath != None:
                    json_paths.append(jsonpath)
            except sre_constants.error:
                continue

        print('jsonpath:' + str(json_paths))

        # 然后运行QA对生成函数
        result = QA_generate.main(json_paths)

        # 存入日志
        logger.info(result)

        global result_list
        result_list = result
        # print(result)
        num = len(result)

        # 只有生成了QA对的时候才能存入
        if num > 0:
            # 存入数据库中
            saveines = QA_save.SaveInEs()
            for res in result:
                saveines.main(myindex,res)

        # if fileName == '华为云网页抽取模版':
        # time.sleep(60)

        result_json = json.dumps({
            "num": num,
            "qa": result,
        })

        return HttpResponse(result_json)
    else:
        return HttpResponse("失败")


def statistics():
    #print("do")
    # 批量清空
    cursor = connection.cursor()

    # Data modifying operation
    cursor.execute("delete from QAManagement_questioncount")
    # transaction.set_dirty()
    cursor.execute("alter table QAManagement_questioncount auto_increment=1")
    # 对用户问题出现的次数进行计数
    query = User.objects.all().values('userquestion').annotate(count=Count('userquestion')).values('userquestion', 'count')
    questioncount_list = list(query)
    # 对统计好出现次数的问题进行排序
    questioncount_sort = sorted(questioncount_list, key=lambda e: e.__getitem__('count'),reverse=True)
    i = 0
    # 出现次数最多的前五条插入数据库
    for qs in questioncount_sort:
        i = i+1
        #print(qs['count'])
        # if tempqc:
        #     tempqc.userquestion = qs['userquestion']
        #     tempqc.questioncount = qs['count']
        #     tempqc.save()
        # else:
        qc = {'userquestion': qs['userquestion'], 'questioncount': qs['count']}
        QuestionCount.objects.create(**qc)
        if(i==5):
            break


scheduler = BackgroundScheduler()# 后台运行
scheduler.add_job(statistics, 'interval', seconds=3600)
scheduler.start()    # 这里的调度任务是独立的一个线程
