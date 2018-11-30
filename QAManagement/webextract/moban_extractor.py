####这个是自定义模板抽取的主函数
#########可以抽取，返回json文件名，不符合返回None
##########link和父主题


#import requests
import re
import json
encoding='utf-8'
class Extract():
    def __init__(self,tabletzs,tabletze,pictzs,pictze,titletzs,titletze,subtitletzs,subtitletze,subjecttzs,subjecttze,notetzs):
        self.tabletzs = tabletzs
        self.tabletze = tabletze
        self.pictzs = pictzs
        self.pictze = pictze
        self.titletzs = titletzs
        self.titletze = titletze
        self.subtitletzs = subtitletzs
        self.subtitletze = subtitletze
        self.subjecttzs = subjecttzs
        self.subjecttze = subjecttze
        ## contenttze= input("请输入内容结尾特征（一般为</div>):")
        ######目前来看，表格内部的说明和正文内部的说明是一种形式
        self.notetzs = notetzs


#########需要往下一个的函数，不需要重构
    def findpic_newcontent(self, mycontent_part, mycode):
        newcontent = re.findall(mycontent_part + r'</div>(.*?)</div>',
                                mycode,
                                re.S)
        mystr = ''
        str_newcontent = mystr.join(newcontent)
        return str_newcontent





    ##########说明处理函数群
    ##########往下取两个的函数，不需要重构


    def findnote_newcontent(self, mycontent_part, mycode):
        newcontent = re.findall(mycontent_part + r'</div></div>(.*?)</div>',
                                mycode,
                                re.S)
        mystr = ''
        str_newcontent = mystr.join(newcontent)
        return str_newcontent



######抽取主函数，myhtml是html内容，myjson为传进的要导出的json文件，mylink为原来的html链接
    def inserthtml(self,myhtml,myjson,mylink):
        json_filename = myjson  # 这是json文件存放的位置

        shu=1


        case = 0



        #htmlf = open(myhtml, 'r', encoding="utf-8")
        htmlcont = myhtml.read()
        myhtml.close()

#########计数器，类型辨别，需要重构




#########表格计数器
        aa = len((re.findall(self.tabletzs+r'(.*?)'+self.tabletze, htmlcont, re.S)))
#########图片计数器
        bb = len((re.findall(self.pictzs+r'(.*?)'+self.pictze, htmlcont, re.S)))

#########对网页去除图片
        a = re.sub(self.pictzs+r'(.*?)'+self.pictze, "", htmlcont, count=bb, flags=re.S)  # a为经过去图片的网页源代码

#######副标题的数量
        subnum = len(re.findall(self.subtitletzs+r'(.*?)'+self.subtitletze, a,re.S))
#######h3 tit的数量,可以忽略，因为这已经属于是另一种模板了
        ####titnum = len(re.findall(r'<h3 class="tit">', a,re.S))

#######类型识别器
        if (re.findall(self.titletzs+r'(.*?)'+self.titletze, a,re.S)):
            case = 1
        elif (re.findall(self.subtitletzs+r'(.*?)'+self.subtitletze, a,re.S)):
            case = 2










####一个放置用的空数组
        temp_dict = { }





        if case == 1 :
            title = re.findall(self.titletzs+r'(.*?)'+self.titletze, a,re.S)  # 找到了大标题
            str1 = ''
            str_title = str1.join(title)
            temp_dict['title']=str_title




            titlecontent = re.findall(self.titletzs + str_title + self.titletze+r'(.*?)</div>', a, re.S)  ######大标题下的内容
            str2 = ''
            str_titlecontent = str2.join(titlecontent)





            if self.notetzs in str_titlecontent:

                string_newcontent = self.findnote_newcontent(str_titlecontent, a)
                str_titlecontent = str_titlecontent+string_newcontent

                while self.notetzs in string_newcontent or self.tabletzs in string_newcontent:
                    if self.notetzs in string_newcontent:
                        string_newcontent = self.findnote_newcontent(string_newcontent, a)

                        str_titlecontent = str_titlecontent + string_newcontent

                    if self.tabletzs in string_newcontent:
                        if self.notetzs in string_newcontent:
                            string_newcontent = self.findnote_newcontent(string_newcontent, a)
                            str_titlecontent =str_titlecontent + string_newcontent
                            string_newcontent = self.findpic_newcontent(string_newcontent, a)

                            str_titlecontent = str_titlecontent + string_newcontent
                        # 跳一个

                        else:
                            string_newcontent = self.findpic_newcontent(string_newcontent, a)

                            str_titlecontent = str_titlecontent + string_newcontent




            if self.tabletzs in str_titlecontent:



                if self.notetzs in str_titlecontent:
                    string_newcontent = self.findnote_newcontent(str_titlecontent, a)
                    str_titlecontent = str_titlecontent + string_newcontent
                    string_newcontent = self.findpic_newcontent(string_newcontent, a)
                    str_titlecontent = str_titlecontent + string_newcontent


                else:
                    string_newcontent = self.findpic_newcontent(str_titlecontent, a)

                    str_titlecontent = str_titlecontent + string_newcontent







                while self.notetzs in string_newcontent or self.tabletzs in string_newcontent:
                    if self.notetzs in string_newcontent:
                        string_newcontent = self.findnote_newcontent(string_newcontent, a)

                        str_titlecontent = str_titlecontent + string_newcontent

                    if self.tabletzs in string_newcontent:
                        if self.notetzs in string_newcontent:
                            string_newcontent = self.findnote_newcontent(string_newcontent, a)
                            str_titlecontent =str_titlecontent + string_newcontent
                            string_newcontent = self.findpic_newcontent(string_newcontent, a)

                            str_titlecontent = str_titlecontent + string_newcontent
                        # 跳一个

                        else:
                            string_newcontent = self.findpic_newcontent(string_newcontent, a)

                            str_titlecontent = str_titlecontent + string_newcontent



            tablei=1
            fuck = re.findall(self.tabletzs+r'(.*?)'+self.tabletze, a, re.S)
            for f in fuck:
                f = self.tabletzs + str(f) + self.tabletze+'</div>'
                ######定位table用的
                str_titlecontent=re.sub(f,'this is table'+str(tablei),str_titlecontent,flags=re.S)
                temp_dict['table'+str(tablei)]=f
                tablei=tablei+1





            #str_titlecontent = re.sub(r'<div class="tablenoborder">(.*?)table>', "", str_titlecontent, count=aa,flags=re.S)  # a为经过去表格的网页源代码

            #print(1)
            cleartitlecontent = re.sub(r'<.*?>', "", str_titlecontent,flags=re.S)
            temp_dict['titlecontent'] = cleartitlecontent


            temp_dict['link'] = str(mylink)




            label = re.findall(self.subjecttzs+r'(.*?)'+self.subjecttze, a, re.S)
            label = re.sub(r'\">\"', "", str(label), flags=re.S)
            label = re.sub(r'<i> &gt; </i>', ">", str(label), flags=re.S)
            #label = re.sub(r'</span>', "", str(label), flags=re.S)
            label = re.sub(r'</a>', "</a", str(label), flags=re.S)
            label=re.findall(r'>(.*?)</',str(label),re.S)
            labellist=[]
            for onelabel in label:
                labellist.append(onelabel)

            temp_dict['subject']=labellist










            #onelabel=re.sub(r'<.*?>',"",str(onelabel),flags=re.S)
            #print(onelabel)







            with open(json_filename, 'w', encoding='utf-8') as json_file:
                json.dump(temp_dict, json_file, ensure_ascii=False)
                json_file.close()






        #############有sectiontitle

        if case == 2 :
            #  1        大标题的正文
            title = re.findall(self.titletzs+r'(.*?)'+self.titletze, a,re.S)  # 找到了大标题
            str1 = ''
            str_title = str1.join(title)
            temp_dict['title'] = str_title





            titlecontent = re.findall(self.titletzs+ str_title + self.titletze+r'(.*?)'+self.subtitletzs, a,re.S)  ######大标题下的内容
            str2 = ''
            str_titlecontent = str2.join(titlecontent)



            tablei = 1
            fuck = re.findall(self.tabletzs+r'(.*?)'+self.tabletze, str_titlecontent, re.S)
            for f in fuck:
                f =self.tabletzs + str(f) + self.tabletze
                str_titlecontent = re.sub(f, 'this is table' + str(tablei), str_titlecontent, flags=re.S)
                temp_dict['table' + str(tablei)] = f
                tablei = tablei + 1

            #str_titlecontent = re.sub(r'<div class="tablenoborder(.*?)table>', "", str_titlecontent, count=aa,
                                    #flags=re.S)  # a为经过去表格的网页源代码

            cleartitlecontent = re.sub(r'<.*?>', "", str_titlecontent,re.S)
            temp_dict['titlecontent'] = cleartitlecontent


                #  2        各个小标题的正文

            q = re.findall(self.subtitletzs+r'(.*?)'+self.subtitletze, a,re.S)
            for str_subtitle in q:
                if shu<subnum:
                    temp_dict['subtitle'+str(shu)] = str_subtitle


                    subcontent = re.findall(self.subtitletzs + str_subtitle +self.subtitletze+r'(.*?)'+self.subtitletzs, a, re.S)
                    ###删除子程序：找到<>，删除
                    str3 = ''
                    str_subcontent=str3.join(subcontent)

                    fuck = re.findall(self.tabletzs+r'(.*?)'+self.tabletze,  str_subcontent, re.S)
                    for f in fuck:
                        f = self.tabletzs + str(f) + self.tabletze
                        str_subcontent = re.sub(f, 'this is table' + str(tablei),  str_subcontent, flags=re.S)
                        temp_dict['table' + str(tablei)] = f
                        tablei = tablei + 1


                    #str_subcontent = re.sub(r'<div class="tablenoborder(.*?)table>', "", str_subcontent, count=aa,
                                           # flags=re.S)  # a为经过去表格的网页源代码
                    clearsubcontent = re.sub(r'<.*?>', "", str_subcontent,re.S)
                    temp_dict['subcontent'+str(shu)] = clearsubcontent
                    shu = shu + 1
                    with open(json_filename, 'w', encoding='utf-8') as json_file:
                        json.dump(temp_dict, json_file, ensure_ascii=False)




                    #########处理最后一段

                else:

                    temp_dict['subtitle' + str(shu)] = str_subtitle

                    subcontent = re.findall(self.subtitletzs + str_subtitle + self.subtitletze+r'(.*?)</div>', a, re.S)

                    str3 = ''
                    str_subcontent = str3.join(subcontent)

                    if self.notetzs in str_subcontent:

                        string_newsubcontent = self.findnote_newcontent(str_subcontent, a)
                        str_subcontent = str_subcontent + string_newsubcontent

                        while self.notetzs in string_newsubcontent or self.tabletzs in string_newsubcontent:
                            if self.notetzs in string_newsubcontent:
                                string_newsubcontent = self.findnote_newcontent(string_newsubcontent, a)


                                str_subcontent = str_subcontent + string_newsubcontent

                            if self.tabletzs in string_newsubcontent:
                                if self.notetzs in string_newsubcontent:
                                    string_newsubcontent = self.findnote_newcontent(string_newsubcontent, a)
                                    str_subcontent = str_subcontent + string_newsubcontent
                                    string_newsubcontent = self.findpic_newcontent(string_newsubcontent, a)

                                    str_subcontent = str_subcontent + string_newsubcontent
                                # 跳一个

                                else:
                                    string_newsubcontent = self.findpic_newcontent(string_newsubcontent, a)

                                    str_subcontent = str_subcontent + string_newsubcontent

                    if self.tabletzs in str_subcontent:

                        if self.notetzs in  str_subcontent:
                            string_newsubcontent = self.findnote_newcontent(str_subcontent, a)
                            str_subcontent = str_titlecontent + string_newsubcontent
                            string_newsubcontent = self.findpic_newcontent(string_newsubcontent, a)
                            str_subcontent = str_subcontent + string_newsubcontent


                        else:
                            string_newsubcontent = self.findpic_newcontent(str_subcontent, a)

                            str_subcontent = str_subcontent + string_newsubcontent

                        while self.notetzs in string_newsubcontent or self.tabletzs in string_newsubcontent:
                            if self.notetzs in string_newsubcontent:
                                string_newsubcontent = self.findnote_newcontent(string_newsubcontent, a)

                                str_subcontent = str_subcontent + string_newsubcontent

                            if self.tabletzs in string_newsubcontent:
                                if self.notetzs in string_newsubcontent:
                                    string_newsubcontent = self.findnote_newcontent(string_newsubcontent, a)
                                    str_subcontent = str_subcontent + string_newsubcontent
                                    string_newsubcontent = self.findpic_newcontent(string_newsubcontent, a)

                                    str_subcontent = str_subcontent + string_newsubcontent
                                # 跳一个

                                else:
                                    string_newsubcontent = self.findpic_newcontent(string_newsubcontent, a)

                                    str_subcontent =  str_subcontent + string_newsubcontent

                    fuck = re.findall(self.tabletzs+r'(.*?)'+self.tabletze, str_subcontent, re.S)
                    for f in fuck:
                        f =self.tabletzs + str(f) + self.tabletze+'</div>'
                        str_subcontent = re.sub(f, 'this is table' + str(tablei), str_subcontent, flags=re.S)
                        temp_dict['table' + str(tablei)] = f
                        tablei = tablei + 1

                    #str_subcontent= re.sub(r'<div class="tablenoborder(.*?)table>', "", str_subcontent, count=aa,flags=re.S)  # a为经过去表格的网页源代码
                    clearsubcontent = re.sub(r'<.*?>', "", str_subcontent)

                    temp_dict['subcontent' + str(shu)] = clearsubcontent

                    temp_dict['link'] = str(mylink)

                    label = re.findall(self.subjecttzs+r'(.*?)'+self.subjecttze, a, re.S)
                    label = re.sub(r'\">\"', "", str(label), flags=re.S)
                    label = re.sub(r'<i> &gt; </i>', ">", str(label), flags=re.S)
                    # label = re.sub(r'</span>', "", str(label), flags=re.S)
                    label = re.sub(r'</a>', "</a", str(label), flags=re.S)
                    label = re.findall(r'>(.*?)</', str(label), re.S)
                    labellist = []
                    for onelabel in label:
                        labellist.append(onelabel)

                    temp_dict['subject'] = labellist

                    with open(json_filename, 'w', encoding='utf-8') as json_file:
                        json.dump(temp_dict, json_file, ensure_ascii=False)
                        json_file.close()

        if (re.findall(self.titletzs+r'(.*?)'+self.titletze, a,re.S)):

            return myjson
        elif (re.findall(self.subtitletzs+r'(.*?)'+self.subtitletze, a,re.S)):
            return myjson

        else:
            return None