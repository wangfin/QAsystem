# -*- coding: utf-8 -*-
# @Time    : 2018/7/30 16:09
# @Author  : wb
# @File    : saveines_test.py

from QAManagement.ques_generate.QA_save import SaveInEs
from QAManagement.withweb import Withweb
import  xdrlib ,sys
import xlrd

save = SaveInEs()
withweb = Withweb()


def open_excel(file):
    data = xlrd.open_workbook(file)
    return data

def excel_table_byname(file,colnameindex=0,by_name=u'Sheet1'):
     data = open_excel(file)
     table = data.sheet_by_name(by_name)
     nrows = table.nrows #行数
     colnames =  table.row_values(colnameindex) #某一行数据
     list =[]
     for rownum in range(1,nrows):
          row = table.row_values(rownum)
          if row:
              app = {}
              for i in range(len(colnames)):
                 app[colnames[i]] = row[i]
              list.append(app)
     return list

result = excel_table_byname('QA_pairs.xlsx',0,'Sheet1')

# print(result)

withweb.webinit('qa_test')

for qa_list in result:
    withweb.webinsert('qa_test', qa_list['标准问题'], qa_list['标准问题'], qa_list['答案'], qa_list['答案链接'],qa_list['主题'],int(qa_list['标准问题ID']))
