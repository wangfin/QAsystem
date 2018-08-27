#####一个网页的正文可以理解为与它的邻域不相同的地方
######7.30 返回值保存为result变量

#############
#test672:驱动程序
#有表格1.0：havetable,表格直接混在抽取正文里
#有表格2.0：test671，表格被单独拿出来
#没表格2.0：notable_final





import sre_constants

from .hauwei_extractor import Extract
#from havetable import Extract

import os

myextract = Extract()



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




    json_domain=os.path.abspath(r'F:\中软杯数据集\havetable_testtime')
    onejson=str(myjson_num)+'.json'

    jsonpath=os.path.join(json_domain,onejson)






    try:
        result=myextract.inserthtml(onehtml,jsonpath,mylink)######此处写入的是变量
        print(result)
    except sre_constants.error:
        continue





