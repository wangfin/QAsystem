#####一个网页的正文可以理解为与它的邻域不相同的地方
###7.30 返回值保存为result变量

#############
#test672:驱动程序
#有表格1.0：havetable,表格直接混在抽取正文里
#有表格2.0：test671，表格被单独拿出来
#没表格2.0：notable_final





import sre_constants

from .moban_extractor import Extract
#from havetable import Extract

import os
mytabletzs = input("请输入表格开头特征:")                                                    #<div class="tablenoborder">
mytabletze = input("请输入表格结尾特征(如</table>):")                                      #</table>
mypictzs = input("请输入图片开头特征:")                                                      #<div class="fignone">
mypictze = input("请输入图片结尾特征:")                                                      #</div>
mytitletzs = input("请输入大标题开头特征:")                                                  #<h1 class="topictitle1">
mytitletze = input("请输入大标题结尾特征:")                                                  #</h1>
mysubtitletzs = input("请输入小标题开头特征:")                                               #<h4 class="sectiontitle">
mysubtitletze = input("请输入小标题结尾特征:")                                               #</h4>
mysubjecttzs = input("请输入主题开头特征:")                                                  #<div class="crumbs">
mysubjecttze = input("请输入主题结尾特征:")                                                  #</div>
## contenttze= input("请输入内容结尾特征（一般为</div>):")
######目前来看，表格内部的说明和正文内部的说明是一种形式
mynotetzs = input('请输入正文内说明开头特征(如<span class="notetitle">):')              #<span class="notetitle">
myextract = Extract(mytabletzs,mytabletze,mypictzs ,mypictze,mytitletzs,mytitletze,mysubtitletzs,mysubtitletze,mysubjecttzs,mysubjecttze,mynotetzs)



htmldata=os.listdir(r'F:\中软杯数据集\support.huaweicloud.com')
#htmldata=os.listdir(r'F:\中软杯数据集\linktest')

#htmldata=os.listdir(r'F:\中软杯数据集\test')
myjson_num=0
for onehtml in htmldata:
    myjson_num=myjson_num+1
    domain = os.path.abspath(r'F:\中软杯数据集\support.huaweicloud.com')
    #domain = os.path.abspath(r'F:\中软杯数据集\linktest')

    #domain = os.path.abspath(r'F:\中软杯数据集\test')
    mylink=onehtml
    onehtml=os.path.join(domain,onehtml)

    onehtml = open(onehtml, 'r',encoding="utf-8")




    json_domain=os.path.abspath(r'F:\中软杯数据集\havetable_testmoban_3')
    onejson=str(myjson_num)+'.json'

    jsonpath=os.path.join(json_domain,onejson)






    try:
        result=myextract.inserthtml(onehtml,jsonpath,mylink)######此处写入的是变量

    except sre_constants.error:
        continue





