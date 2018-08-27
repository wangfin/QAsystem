##########link和父主题
##########如果符合四个case，则返回json文件名，不符合则返回None

#import requests
import re
import json
encoding='utf-8'
class Extract():
    #json_filename = 'F:/中软杯数据集/submit.json'  # 这是json文件存放的位置



    def findpic_newcontent(self, mycontent_part, mycode):
        newcontent = re.findall(mycontent_part + r'</div>(.*?)</div>',
                                mycode,
                                re.S)
        mystr = ''
        str_newcontent = mystr.join(newcontent)
        return str_newcontent





    ##########说明处理函数群




    def findnote_newcontent(self, mycontent_part, mycode):
        newcontent = re.findall(mycontent_part + r'</div></div>(.*?)</div>',
                                mycode,
                                re.S)
        mystr = ''
        str_newcontent = mystr.join(newcontent)
        return str_newcontent




    def inserthtml(self,myhtml,myjson,mylink):
        json_filename = myjson  # 这是json文件存放的位置

        shu=1


        case = 0



        #htmlf = open(myhtml, 'r', encoding="utf-8")
        htmlcont = myhtml.read()
        myhtml.close()





        aa = len((re.findall(r'<div class="tablenoborder">(.*?)</div>', htmlcont, re.S)))

        bb = len((re.findall(r'<div class="fignone"(.*?)</div>', htmlcont, re.S)))



        a = re.sub(r'<div class="fignone(.*?)div>', "", htmlcont, count=bb, flags=re.S)  # a为经过去图片的网页源代码
        subnum = len(re.findall(r'<h4 class="sectiontitle">(.*?)</h4>', a,re.S))
        titnum = len(re.findall(r'<h3 class="tit">', a,re.S))







        if (re.findall(r'<h1 class="topictitle1">(.*?)</h1>', a,re.S)):
            case = 1

        elif (re.findall(r'<h4 class="sectiontitle">(.*?)</h4>', a,re.S)):
            case = 2
        elif(re.findall(r'<h1 class="poster-caption">(.*?)</h1>',a,re.S)):

            case = 3


        elif (re.findall(r'<h1 class="poster-caption">(.*?)</h1>',a,re.S)) and (re.findall(r'<h3 class="tit">',a,re.S)):
            case = 4













        temp_dict = { }





        if case == 1 :
            title = re.findall(r'<h1 class="topictitle1">(.*?)</h1>', a,re.S)  # 找到了大标题
            str1 = ''
            str_title = str1.join(title)
            temp_dict['title']=str_title




            titlecontent = re.findall(r'<h1 class="topictitle1">' + str_title + r'</h1>(.*?)</div>', a, re.S)  ######大标题下的内容
            str2 = ''
            str_titlecontent = str2.join(titlecontent)





            if '<div class="notetitle"' in str_titlecontent:

                string_newcontent = self.findnote_newcontent(str_titlecontent, a)
                str_titlecontent = str_titlecontent+string_newcontent

                while '<span class="notetitle">' in string_newcontent or '<div class="tablenoborder">' in string_newcontent:
                    if '<span class="notetitle">' in string_newcontent:
                        string_newcontent = self.findnote_newcontent(string_newcontent, a)

                        str_titlecontent = str_titlecontent + string_newcontent

                    if '<div class="tablenoborder">' in string_newcontent:
                        if '<span class="noticetitle">' in string_newcontent:
                            string_newcontent = self.findnote_newcontent(string_newcontent, a)
                            str_titlecontent =str_titlecontent + string_newcontent
                            string_newcontent = self.findpic_newcontent(string_newcontent, a)

                            str_titlecontent = str_titlecontent + string_newcontent
                        # 跳一个

                        else:
                            string_newcontent = self.findpic_newcontent(string_newcontent, a)

                            str_titlecontent = str_titlecontent + string_newcontent




            if '<div class="tablenoborder">' in str_titlecontent:



                if '<span class="noticetitle">' in str_titlecontent:
                    string_newcontent = self.findnote_newcontent(str_titlecontent, a)
                    str_titlecontent = str_titlecontent + string_newcontent
                    string_newcontent = self.findpic_newcontent(string_newcontent, a)
                    str_titlecontent = str_titlecontent + string_newcontent


                else:
                    string_newcontent = self.findpic_newcontent(str_titlecontent, a)

                    str_titlecontent = str_titlecontent + string_newcontent







                while '<span class="notetitle">' in string_newcontent or '<div class="tablenoborder">' in string_newcontent:
                    if '<span class="notetitle">' in string_newcontent:
                        string_newcontent = self.findnote_newcontent(string_newcontent, a)

                        str_titlecontent = str_titlecontent + string_newcontent

                    if '<div class="tablenoborder">' in string_newcontent:
                        if '<span class="noticetitle">' in string_newcontent:
                            string_newcontent = self.findnote_newcontent(string_newcontent, a)
                            str_titlecontent =str_titlecontent + string_newcontent
                            string_newcontent = self.findpic_newcontent(string_newcontent, a)

                            str_titlecontent = str_titlecontent + string_newcontent
                        # 跳一个

                        else:
                            string_newcontent = self.findpic_newcontent(string_newcontent, a)

                            str_titlecontent = str_titlecontent + string_newcontent



            tablei=1
            fuck = re.findall(r'<div class="tablenoborder">(.*?)</table>', a, re.S)
            for f in fuck:
                f = '<div class="tablenoborder">' + str(f) + '</table>'
                str_titlecontent=re.sub(f,'this is table'+str(tablei),str_titlecontent,flags=re.S)
                temp_dict['table'+str(tablei)]=f
                tablei=tablei+1





            #str_titlecontent = re.sub(r'<div class="tablenoborder">(.*?)table>', "", str_titlecontent, count=aa,flags=re.S)  # a为经过去表格的网页源代码

            #print(1)
            cleartitlecontent = re.sub(r'<.*?>', "", str_titlecontent,flags=re.S)
            temp_dict['titlecontent'] = cleartitlecontent


            temp_dict['link'] = str(mylink)




            label = re.findall(r'<div class="crumbs">(.*?)</div>', a, re.S)
            label = re.sub(r'\">\"', "", str(label), flags=re.S)
            label = re.sub(r'</a>', "</a", str(label), flags=re.S)
            label = re.sub(r'</span>', "</span", str(label), flags=re.S)
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
            title = re.findall(r'<h1 class="topictitle1">(.*?)</h1>', a,re.S)  # 找到了大标题
            str1 = ''
            str_title = str1.join(title)
            temp_dict['title'] = str_title





            titlecontent = re.findall(r'<h1 class="topictitle1">' + str_title + r'</h1>(.*?)<h4 class="sectiontitle">', a,re.S)  ######大标题下的内容
            str2 = ''
            str_titlecontent = str2.join(titlecontent)



            tablei = 1
            fuck = re.findall(r'<div class="tablenoborder">(.*?)</table>', str_titlecontent, re.S)
            for f in fuck:
                f = '<div class="tablenoborder">' + str(f) + '</table>'
                str_titlecontent = re.sub(f, 'this is table' + str(tablei), str_titlecontent, flags=re.S)
                temp_dict['table' + str(tablei)] = f
                tablei = tablei + 1

            #str_titlecontent = re.sub(r'<div class="tablenoborder(.*?)table>', "", str_titlecontent, count=aa,
                                    #flags=re.S)  # a为经过去表格的网页源代码

            cleartitlecontent = re.sub(r'<.*?>', "", str_titlecontent,re.S)
            temp_dict['titlecontent'] = cleartitlecontent


                #  2        各个小标题的正文

            q = re.findall(r'<h4 class="sectiontitle">(.*?)</h4>', a,re.S)
            for str_subtitle in q :
                if shu<subnum:
                    temp_dict['subtitle'+str(shu)] = str_subtitle


                    subcontent = re.findall(r'<h4 class="sectiontitle">' + str_subtitle + r'</h4>(.*?)<h4 class="sectiontitle">', a, re.S)
                    ###删除子程序：找到<>，删除
                    str3 = ''
                    str_subcontent=str3.join(subcontent)

                    fuck = re.findall(r'<div class="tablenoborder">(.*?)</table>',  str_subcontent, re.S)
                    for f in fuck:
                        f = '<div class="tablenoborder">' + str(f) + '</table>'
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

                    subcontent = re.findall(r'<h4 class="sectiontitle">' + str_subtitle + r'</h4>(.*?)</div>', a, re.S)




                    str3 = ''
                    str_subcontent = str3.join(subcontent)

                    if '<div class="notetitle"' in str_subcontent:

                        string_newsubcontent = self.findnote_newcontent(str_subcontent, a)
                        str_subcontent = str_subcontent + string_newsubcontent

                        while '<span class="notetitle">' in string_newsubcontent or '<div class="tablenoborder">' in string_newsubcontent:
                            if '<span class="notetitle">' in string_newsubcontent:
                                string_newsubcontent = self.findnote_newcontent(string_newsubcontent, a)

                                str_subcontent = str_subcontent + string_newsubcontent

                            if '<div class="tablenoborder">' in string_newsubcontent:
                                if '<span class="noticetitle">' in string_newsubcontent:
                                    string_newsubcontent = self.findnote_newcontent(string_newsubcontent, a)
                                    str_subcontent = str_subcontent + string_newsubcontent
                                    string_newsubcontent = self.findpic_newcontent(string_newsubcontent, a)

                                    str_subcontent = str_subcontent + string_newsubcontent
                                # 跳一个

                                else:
                                    string_newsubcontent = self.findpic_newcontent(string_newsubcontent, a)

                                    str_subcontent = str_subcontent + string_newsubcontent

                    if '<div class="tablenoborder">' in str_subcontent:

                        if '<span class="noticetitle">' in  str_subcontent:
                            string_newsubcontent = self.findnote_newcontent(str_subcontent, a)
                            str_subcontent = str_titlecontent + string_newsubcontent
                            string_newsubcontent = self.findpic_newcontent(string_newsubcontent, a)
                            str_subcontent = str_subcontent + string_newsubcontent


                        else:
                            string_newsubcontent = self.findpic_newcontent(str_subcontent, a)

                            str_subcontent = str_subcontent + string_newsubcontent

                        while '<span class="notetitle">' in string_newsubcontent or '<div class="tablenoborder">' in string_newsubcontent:
                            if '<span class="notetitle">' in string_newsubcontent:
                                string_newsubcontent = self.findnote_newcontent(string_newsubcontent, a)

                                str_subcontent = str_subcontent + string_newsubcontent

                            if '<div class="tablenoborder">' in string_newsubcontent:
                                if '<span class="noticetitle">' in string_newsubcontent:
                                    string_newsubcontent = self.findnote_newcontent(string_newsubcontent, a)
                                    str_subcontent = str_subcontent + string_newsubcontent
                                    string_newsubcontent = self.findpic_newcontent(string_newsubcontent, a)

                                    str_subcontent = str_subcontent + string_newsubcontent
                                # 跳一个

                                else:
                                    string_newsubcontent = self.findpic_newcontent(string_newsubcontent, a)

                                    str_subcontent =  str_subcontent + string_newsubcontent

                    fuck = re.findall(r'<div class="tablenoborder">(.*?)</table>', str_subcontent, re.S)
                    for f in fuck:
                        f = '<div class="tablenoborder">' + str(f) + '</table>'
                        str_subcontent = re.sub(f, 'this is table' + str(tablei), str_subcontent, flags=re.S)
                        temp_dict['table' + str(tablei)] = f
                        tablei = tablei + 1

                    #str_subcontent= re.sub(r'<div class="tablenoborder(.*?)table>', "", str_subcontent, count=aa,flags=re.S)  # a为经过去表格的网页源代码
                    clearsubcontent = re.sub(r'<.*?>', "", str_subcontent)

                    temp_dict['subcontent' + str(shu)] = clearsubcontent

                    temp_dict['link'] = str(mylink)

                    label = re.findall(r'<div class="crumbs">(.*?)</div>', a, re.S)
                    label = re.sub(r'\">\"', "", str(label), flags=re.S)
                    label = re.sub(r'</a>', "</a", str(label), flags=re.S)
                    label = re.sub(r'</span>', "</span", str(label), flags=re.S)
                    label = re.findall(r'>(.*?)</', str(label), re.S)
                    labellist = []
                    for onelabel in label:
                        labellist.append(onelabel)

                    temp_dict['subject'] = labellist

                    with open(json_filename, 'w', encoding='utf-8') as json_file:
                        json.dump(temp_dict, json_file, ensure_ascii=False)
                        json_file.close()




        if case ==3:
            title = re.findall(r'<h1 class="poster-caption">(.*?)</h1>', a,re.S)  # 找到了大标题
            str1 = ''
            str_title = str1.join(title)
            temp_dict['title'] = str_title

            titlecontent = re.findall(r'<h1 class="poster-caption">' + str_title + r'</h1>(.*?)</div>', a,
                                      re.S)  ######大标题下的内容
            str2 = ''
            str_titlecontent = str2.join(titlecontent)

            if '<div class="notetitle"' in str_titlecontent:

                string_newcontent = self.findnote_newcontent(str_titlecontent, a)
                str_titlecontent = str_titlecontent + string_newcontent

                while '<span class="notetitle">' in string_newcontent or '<div class="tablenoborder">' in string_newcontent:
                    if '<span class="notetitle">' in string_newcontent:
                        string_newcontent = self.findnote_newcontent(string_newcontent, a)

                        str_titlecontent = str_titlecontent + string_newcontent

                    if '<div class="tablenoborder">' in string_newcontent:
                        if '<span class="noticetitle">' in string_newcontent:
                            string_newcontent = self.findnote_newcontent(string_newcontent, a)
                            str_titlecontent = str_titlecontent + string_newcontent
                            string_newcontent = self.findpic_newcontent(string_newcontent, a)

                            str_titlecontent = str_titlecontent + string_newcontent
                        # 跳一个

                        else:
                            string_newcontent = self.findpic_newcontent(string_newcontent, a)

                            str_titlecontent = str_titlecontent + string_newcontent

            if '<div class="tablenoborder">' in str_titlecontent:

                if '<span class="noticetitle">' in str_titlecontent:
                    string_newcontent = self.findnote_newcontent(str_titlecontent, a)
                    str_titlecontent = str_titlecontent + string_newcontent
                    string_newcontent = self.findpic_newcontent(string_newcontent, a)
                    str_titlecontent = str_titlecontent + string_newcontent


                else:
                    string_newcontent = self.findpic_newcontent(str_titlecontent, a)

                    str_titlecontent = str_titlecontent + string_newcontent

                while '<span class="notetitle">' in string_newcontent or '<div class="tablenoborder">' in string_newcontent:
                    if '<span class="notetitle">' in string_newcontent:
                        string_newcontent = self.findnote_newcontent(string_newcontent, a)

                        str_titlecontent = str_titlecontent + string_newcontent

                    if '<div class="tablenoborder">' in string_newcontent:
                        if '<span class="noticetitle">' in string_newcontent:
                            string_newcontent = self.findnote_newcontent(string_newcontent, a)
                            str_titlecontent = str_titlecontent + string_newcontent
                            string_newcontent = self.findpic_newcontent(string_newcontent, a)

                            str_titlecontent = str_titlecontent + string_newcontent
                        # 跳一个

                        else:
                            string_newcontent = self.findpic_newcontent(string_newcontent, a)

                            str_titlecontent = str_titlecontent + string_newcontent

            tablei = 1
            fuck = re.findall(r'<div class="tablenoborder">(.*?)</table>', str_titlecontent, re.S)
            for f in fuck:
                f = '<div class="tablenoborder">' + str(f) + '</table>'
                str_titlecontent = re.sub(f, 'this is table' + str(tablei), str_titlecontent, flags=re.S)
                temp_dict['table' + str(tablei)] = f
                tablei = tablei + 1

            #str_titlecontent = re.sub(r'<div class="tablenoborder(.*?)table>', "", str_titlecontent, count=aa,
                                   # flags=re.S)  # a为经过去表格的网页源代码

            cleartitlecontent = re.sub(r'<.*?>', "", str_titlecontent,flags=re.S)
            temp_dict['titlecontent'] = cleartitlecontent
            temp_dict['link'] = str(mylink)

            label = re.findall(r'<div class="crumbs">(.*?)</div>', a, re.S)
            label = re.sub(r'\">\"', "", str(label), flags=re.S)
            label = re.sub(r'</a>', "</a", str(label), flags=re.S)
            label = re.sub(r'</span>', "</span", str(label), flags=re.S)
            label = re.findall(r'>(.*?)</', str(label), re.S)
            labellist = []
            for onelabel in label:
                labellist.append(onelabel)

            temp_dict['subject'] = labellist
            with open(json_filename, 'w', encoding='utf-8') as json_file:
                json.dump(temp_dict, json_file, ensure_ascii=False)
                json_file.close()





        if case==4:
            title = re.findall(r' <h1 class="poster-caption">(.*?)</h1>', a, re.S)  # 找到了大标题
            str1 = ''
            str_title = str1.join(title)
            temp_dict['title'] = str_title

            titlecontent = re.findall(r' <h1 class="poster-caption">' + str_title + r'</h1>(.*?)<h3 class="tit">', a,
                                      re.S)  ######大标题下的内容
            str2 = ''
            str_titlecontent = str2.join(titlecontent)

            tablei = 1
            fuck = re.findall(r'<div class="tablenoborder">(.*?)</table>', str_titlecontent, re.S)
            for f in fuck:
                f = '<div class="tablenoborder">' + str(f) + '</table>'
                str_titlecontent = re.sub(f, 'this is table' + str(tablei), str_titlecontent, flags=re.S)
                temp_dict['table' + str(tablei)] = f
                tablei = tablei + 1


           # str_titlecontent = re.sub(r'<div class="tablenoborder(.*?)table>', "", str_titlecontent, count=aa,
                                                  #  flags=re.S)  # a为经过去表格的网页源代码

            cleartitlecontent = re.sub(r'<.*?>', "", str_titlecontent, re.S)
            temp_dict['titlecontent'] = cleartitlecontent

            #  2        各个小标题的正文

            q = re.findall(r'<h3 class="tit">(.*?)</h3>', a, re.S)
            for str_subtitle in q:
                if shu < titnum:
                    temp_dict['subtitle' + str(shu)] = str_subtitle

                    subcontent = re.findall(
                        r'<h3 class="tit">' + str_subtitle + r'</h3>(.*?)<h3 class="tit">', a, re.S)
                    ###删除子程序：找到<>，删除
                    str3 = ''
                    str_subcontent = str3.join(subcontent)
                    fuck = re.findall(r'<div class="tablenoborder">(.*?)</table>',str_subcontent, re.S)
                    for f in fuck:
                        f = '<div class="tablenoborder">' + str(f) + '</table>'
                        str_subcontent = re.sub(f, 'this is table' + str(tablei), str_subcontent, flags=re.S)
                        temp_dict['table' + str(tablei)] = f
                        tablei = tablei + 1
                    #str_subcontent = re.sub(r'<div class="tablenoborder(.*?)table>', "", str_subcontent, count=aa,
                                           # flags=re.S)  # a为经过去表格的网页源代码
                    clearsubcontent = re.sub(r'<.*?>', "", str_subcontent, re.S)
                    temp_dict['subcontent' + str(shu)] = clearsubcontent
                    shu = shu + 1
                    with open(json_filename, 'w', encoding='utf-8') as json_file:
                        json.dump(temp_dict, json_file, ensure_ascii=False)

                    #########处理最后一段

                else:

                    temp_dict['subtitle' + str(shu)] = str_subtitle

                    subcontent = re.findall(r'<h3 class="tit">' + str_subtitle + r'</h3>(.*?)</div>', a, re.S)

                    str3 = ''
                    str_subcontent = str3.join(subcontent)

                    if '<div class="notetitle"' in str_subcontent:

                        string_newsubcontent = self.findnote_newcontent(str_subcontent, a)
                        str_subcontent = str_subcontent + string_newsubcontent

                        while '<span class="notetitle">' in string_newsubcontent or '<div class="tablenoborder">' in string_newsubcontent:
                            if '<span class="notetitle">' in string_newsubcontent:
                                string_newsubcontent = self.findnote_newcontent(string_newsubcontent, a)

                                str_subcontent = str_subcontent + string_newsubcontent

                            if '<div class="tablenoborder">' in string_newsubcontent:
                                if '<span class="noticetitle">' in string_newsubcontent:
                                    string_newsubcontent = self.findnote_newcontent(string_newsubcontent, a)
                                    str_subcontent = str_subcontent + string_newsubcontent
                                    string_newsubcontent = self.findpic_newcontent(string_newsubcontent, a)

                                    str_subcontent = str_subcontent + string_newsubcontent
                                # 跳一个

                                else:
                                    string_newsubcontent = self.findpic_newcontent(string_newsubcontent, a)

                                    str_subcontent = str_subcontent + string_newsubcontent

                    if '<div class="tablenoborder">' in str_subcontent:

                        if '<span class="noticetitle">' in str_subcontent:
                            string_newsubcontent = self.findnote_newcontent(str_subcontent, a)
                            str_subcontent = str_titlecontent + string_newsubcontent
                            string_newsubcontent = self.findpic_newcontent(string_newsubcontent, a)
                            str_subcontent = str_subcontent + string_newsubcontent


                        else:
                            string_newsubcontent = self.findpic_newcontent(str_subcontent, a)

                            str_subcontent = str_subcontent + string_newsubcontent

                        while '<span class="notetitle">' in string_newsubcontent or '<div class="tablenoborder">' in string_newsubcontent:
                            if '<span class="notetitle">' in string_newsubcontent:
                                string_newsubcontent = self.findnote_newcontent(string_newsubcontent, a)

                                str_subcontent = str_subcontent + string_newsubcontent

                            if '<div class="tablenoborder">' in string_newsubcontent:
                                if '<span class="noticetitle">' in string_newsubcontent:
                                    string_newsubcontent = self.findnote_newcontent(string_newsubcontent, a)
                                    str_subcontent = str_subcontent + string_newsubcontent
                                    string_newsubcontent = self.findpic_newcontent(string_newsubcontent, a)

                                    str_subcontent = str_subcontent + string_newsubcontent
                                # 跳一个

                                else:
                                    string_newsubcontent = self.findpic_newcontent(string_newsubcontent, a)

                                    str_subcontent = str_subcontent + string_newsubcontent

                    fuck = re.findall(r'<div class="tablenoborder">(.*?)</table>', str_subcontent, re.S)
                    for f in fuck:
                        f = '<div class="tablenoborder">' + str(f) + '</table>'
                        str_subcontent = re.sub(f, 'this is table' + str(tablei), str_subcontent, flags=re.S)
                        temp_dict['table' + str(tablei)] = f
                        tablei = tablei + 1

                   # str_subcontent = re.sub(r'<div class="tablenoborder(.*?)table>', "", str_subcontent, count=aa,
                                         #   flags=re.S)  # a为经过去表格的网页源代码
                    clearsubcontent = re.sub(r'<.*?>', "", str_subcontent)

                    temp_dict['subcontent' + str(shu)] = clearsubcontent
                    temp_dict['link'] = str(mylink)

                    label = re.findall(r'<div class="crumbs">(.*?)</div>', a, re.S)
                    label = re.sub(r'\">\"', "", str(label), flags=re.S)
                    label = re.sub(r'</a>', "</a", str(label), flags=re.S)
                    label = re.sub(r'</span>', "</span", str(label), flags=re.S)
                    label = re.findall(r'>(.*?)</', str(label), re.S)
                    labellist = []
                    for onelabel in label:
                        labellist.append(onelabel)

                    temp_dict['subject'] = labellist

                    with open(json_filename, 'w', encoding='utf-8') as json_file:
                        json.dump(temp_dict, json_file, ensure_ascii=False)
                        json_file.close()


        if (re.findall(r'<h1 class="topictitle1">(.*?)</h1>', a,re.S)):
            return myjson

        elif (re.findall(r'<h4 class="sectiontitle">(.*?)</h4>', a,re.S)):
            return myjson
        elif(re.findall(r'<h1 class="poster-caption">(.*?)</h1>',a,re.S)):

            return myjson


        elif (re.findall(r'<h1 class="poster-caption">(.*?)</h1>',a,re.S)) and (re.findall(r'<h3 class="tit">',a,re.S)):
            return myjson


        else:
            return None




