# -*- coding: utf-8 -*-
# @Time    : 2018/7/28 9:15
# @Author  : wb
# @File    : QA_test.py

# 测试QA生成模块

from QAManagement.ques_generate.QG_paragraph import Paragraph
import os
from xlrd import open_workbook
from xlutils.copy import copy



paragaph = Paragraph()
# 读取抽取好的json文件
# 遍历上传的文件夹中所有的文件
# 还需要判断上传的是文件夹目录还是文件
path = "../data/notable" # 文件夹目录
files= os.listdir(path) # 得到文件夹下的所有文件名称
urls = []
for file in files: # 遍历文件夹
     if not os.path.isdir(file): # 判断是否是文件夹，不是文件夹才打开
          urls.append(path+"/"+file)

# print(urls) # 打印结果
# print(len(urls))
# print(urls[101])
# paths = [urls[101]]
#
result = paragaph.main(urls)

rexcel = open_workbook("../data/QA_pairs.xlsx") # 用wlrd提供的方法读取一个excel文件
rows = rexcel.sheets()[0].nrows # 用wlrd提供的方法获得现在已有的行数
excel = copy(rexcel) # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
table = excel.get_sheet(0) # 用xlwt对象的方法获得要操作的sheet
# values = ["1", "2", "3"]
row = rows
for value in result:
    table.write(row, 0, row) # xlwt对象的写方法，参数分别是行、列、值
    table.write(row, 1, value['question'])
    table.write(row, 2, value['subject'])
    table.write(row, 3, value['answer'])
    table.write(row, 4, value['answer_link'])
    row += 1
excel.save("../data/QA_pairs.xlsx") # xlwt对象的保存方法，这时便覆盖掉了原来的excel


# print(result)
# for url in urls:
#     result = paragaph.main(url)
#     print(result)
