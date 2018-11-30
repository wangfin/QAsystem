# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 9:35
# @Author  : wb
# @File    : extract.py

import os
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
from QAManagement.question_generalization.mysqldb_helper import SQLHelper
# 模版抽取

# 从不同类型的问句中抽取出不同的问句模板

class Extract():


    # 导入LTP的文件
    LTP_DATA_DIR = '/home/wang/data/ltp_data'  # ltp模型目录的路径

    # 分词
    cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
    segmentor = Segmentor()  # 初始化实例
    segmentor.load_with_lexicon(cws_model_path, '/home/wang/data/new_dictionary.txt')  # 加载模型，第二个参数是您的增量模型路径

    # 词性标注
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
    postagger = Postagger()  # 初始化实例
    postagger.load(pos_model_path)  # 加载模型

    # 依存句法分析
    par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
    parser = Parser()  # 初始化实例
    parser.load(par_model_path)  # 加载模型

    # 分类的疑问词
    # 多久 how-long
    how_long = ['多长时间', '多少时间', '多久']
    # 多少 how-much
    how_much = ['多少', '几']
    # 地点 where
    where = ['什么地方', '什么地点', '哪里', '何处', '哪个地方']
    # 方式 how_do
    how_do = ['怎样', '怎么', '怎么样', '如何', '哪些方法', '哪些方式', '哪些途径', '何种方法', '什么方法', '什么方式', '什么途径']
    # 人物 who
    who = ['什么人', '谁', '哪个人', '何人', '哪些人', '哪一个人']
    # 时间 when
    when = ['什么时间', '什么时候', '何时', '哪个时候']
    # 原因 why
    why = ['什么原因', '哪些原因', '什么因素', '哪些因素', '为什么', '为何']
    # 是否类 yes_no
    yes_no = ['能', '能够', '会可', '可能', '可以', '有', '是']
    # 定义类
    definition = ['是什么', '什么是']
    # 列表类 list_ques
    list_ques = ['哪些', '有什么', '有哪些', '有啥']
    # 哪个 which
    which = ['哪个', '哪']
    # 正常疑问句
    common_ques = ['什么']
    # 疑问语气词
    modal = ['吗', '呢', '吧', '么', '嘛']

    # 1. 分词，词性标注
    def pretreate(self,question):

        # 对输入的句子进行分词和词性标注
        words = Extract.segmentor.segment(question)  # 分词
        words_list = list(words)

        postags = Extract.postagger.postag(words_list)  # 词性标注
        postags_list = list(postags)

        # arcs = Extract.parser.parse(words_list, postags_list)  # 句法分析
        # # print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
        # arcs_list = []
        # for arc in arcs:
        #     arcs_list.append(str(arc.head) + ':' + str(arc.relation))

        # # 将疑问词替换成标签
        # if type == 'how_do':
        #     # 首先先将疑问词替换成标注
        #     for ques_type_word in Extract.how_do:
        #         if ques_type_word in question:
        #             question.replace(ques_type_word,type)
        # elif type == 'how_long':
        #     # 首先先将疑问词替换成标注
        #     for ques_type_word in Extract.how_long:
        #         if ques_type_word in question:
        #             question.replace(ques_type_word,type)
        # elif type == 'how_much':
        #     # 首先先将疑问词替换成标注
        #     for ques_type_word in Extract.how_much:
        #         if ques_type_word in question:
        #             question.replace(ques_type_word,type)
        # elif type == 'where':
        #     # 首先先将疑问词替换成标注
        #     for ques_type_word in Extract.where:
        #         if ques_type_word in question:
        #             question.replace(ques_type_word,type)
        # elif type == 'when':
        #     # 首先先将疑问词替换成标注
        #     for ques_type_word in Extract.when:
        #         if ques_type_word in question:
        #             question.replace(ques_type_word,type)
        # elif type == 'which':
        #     # 首先先将疑问词替换成标注
        #     for ques_type_word in Extract.which:
        #         if ques_type_word in question:
        #             question.replace(ques_type_word,type)
        # elif type == 'who':
        #     # 首先先将疑问词替换成标注
        #     for ques_type_word in Extract.who:
        #         if ques_type_word in question:
        #             question.replace(ques_type_word,type)
        # elif type == 'why':
        #     # 首先先将疑问词替换成标注
        #     for ques_type_word in Extract.why:
        #         if ques_type_word in question:
        #             question.replace(ques_type_word,type)
        # # elif type == 'definition':
        # #     # 首先先将疑问词替换成标注
        # #     for ques_type_word in Extract.definition:
        # #         if ques_type_word in question:
        # #             question.replace(ques_type_word,type)
        # elif type == 'list_ques':
        #     # 首先先将疑问词替换成标注
        #     for ques_type_word in Extract.list_ques:
        #         if ques_type_word in question:
        #             question.replace(ques_type_word,type)
        # elif type == 'common_ques':
        #     # 首先先将疑问词替换成标注
        #     for ques_type_word in Extract.common_ques:
        #         if ques_type_word in question:
        #             question.replace(ques_type_word,type)


        # 这里没有设置yes_no问题的标注
        # 定义类的是什么也不大好

        # 对替换之后的问句在进行分词

        # 将分词好的序列中的疑问词替换成标签

        type = None
        for i in range(len(words_list)):
            if words_list[i] in Extract.how_long:
                postags_list[i] = 'how_long'
                type = 'how_long'
            elif words_list[i] in Extract.how_much:
                postags_list[i] = 'how_much'
                type = 'how_much'
            elif words_list[i] in Extract.how_do:
                postags_list[i] = 'how_do'
                type = 'how_do'
            elif words_list[i] in Extract.which:
                postags_list[i] = 'which'
                type = 'which'
            elif words_list[i] in Extract.when:
                postags_list[i] = 'when'
                type = 'when'
            elif words_list[i] in Extract.where:
                postags_list[i] = 'where'
                type = 'where'
            elif words_list[i] in Extract.who:
                postags_list[i] = 'who'
                type = 'who'
            elif words_list[i] in Extract.why:
                postags_list[i] = 'why'
                type = 'why'
            elif words_list[i] in Extract.common_ques:
                postags_list[i] = 'common_ques'
                type = 'common_ques'
            elif words_list[i] in Extract.list_ques:
                postags_list[i] = 'list_ques'
                type = 'list_ques'
            elif words_list[i] in Extract.yes_no:
                postags_list[i] = 'modal'

        # print(words_list)
        # print(postags_list)

        return [words_list,postags_list,type]

    # 2.压缩模版
    def compression(self,words_list,postags_list):
        # 对输入的词性模版进行压缩
        # 同时需要对words_list 中的相对应的部分进行删除
        '''
        具体如下：
        a -> n 形容词修饰名词
        d -> a 副词修饰形容词
        a -> a && a != head 形容词修饰形容词
        u -> a 助词修饰形容词
        u -> d 助词修饰副词
        n -> n 名词修饰名词
        b -> n 名词修饰语修饰名词
        j -> n 缩写词修饰名词
        '''

        # 需要被删除的id
        delete_id = []

        for i in range(len(postags_list) - 1):
            if postags_list[i] == 'a' and postags_list[i+1] == 'n':
                delete_id.append(i)
            elif postags_list[i] == 'd' and postags_list[i+1] == 'a':
                delete_id.append(i)
            elif postags_list[i] == 'a' and postags_list[i+1] == 'a' and i != 0:
                delete_id.append(i)
            elif postags_list[i] == 'u' and postags_list[i+1] == 'a':
                delete_id.append(i)
            elif postags_list[i] == 'u' and postags_list[i+1] == 'd':
                delete_id.append(i)
            elif postags_list[i] == 'n' and postags_list[i+1] == 'n':
                delete_id.append(i)
            elif postags_list[i] == 'b' and postags_list[i+1] == 'n':
                delete_id.append(i)
            elif postags_list[i] == 'j' and postags_list[i+1] == 'n':
                delete_id.append(i)

        for i in range(len(delete_id)):
            words_list.pop(delete_id[i] - i)
            postags_list.pop(delete_id[i] - i)


        # 对更改过的模型进行依存语句分析
        arcs = Extract.parser.parse(words_list, postags_list)  # 句法分析
        arcs_list = []

        for arc in arcs:
            arcs_list.append(str(arc.head) + ':' + str(arc.relation))


        # print(postags_list)
        return [words_list,postags_list,arcs_list]

    # 3.将原句与模版存入模板库中
    def savedb(self,words_list,postags_list,arcs_list,type):
        # 将模版存入mysql数据库中
        sqlhelper = SQLHelper(host=SQLHelper.host,user=SQLHelper.username,pwd=SQLHelper.password,db=SQLHelper.database)

        question = ''
        for word in words_list:
            if word == "'":
                question += "/'/'" + ' '
            # elif word == '"':
            #     question += '/"'
            else:
                question += word + ' '

        # question = ' '.join(words_list)
        template = ' '.join(postags_list)

        # print(arcs_list)

        dependparse = ' '.join(arcs_list)

        print(question)
        print(template)
        print(dependparse)

        # tablename = ''
        sql = "INSERT INTO ${tablename} (question, template , dependparse) VALUES ('%s', '%s' , '%s')" % (question, template ,dependparse)

        # 在存入前先进行去重，查询是否有相同的模板
        check_sql = "SELECT * FROM ${tablename} WHERE template = '%s'" % template

        if type == 'how_long':
            check_sql = check_sql.replace('${tablename}' , 'how_long_ques')
            if len(sqlhelper.ExecQuery(check_sql)) == 0:
                sql = sql.replace('${tablename}' , 'how_long_ques')
                sqlhelper.ExecNonQuery(sql=sql)
        elif type == 'how_much':
            check_sql = check_sql.replace('${tablename}', 'how_much_ques')
            if len(sqlhelper.ExecQuery(check_sql)) == 0:
                sql = sql.replace('${tablename}' , 'how_much_ques')
                sqlhelper.ExecNonQuery(sql=sql)
        elif type == 'how_do':
            check_sql = check_sql.replace('${tablename}', 'how_do_ques')
            if len(sqlhelper.ExecQuery(check_sql)) == 0:
                sql = sql.replace('${tablename}' , 'how_do_ques')
                sqlhelper.ExecNonQuery(sql=sql)
        elif type == 'who':
            check_sql = check_sql.replace('${tablename}', 'who_ques')
            if len(sqlhelper.ExecQuery(check_sql)) == 0:
                sql = sql.replace('${tablename}' , 'who_ques')
                sqlhelper.ExecNonQuery(sql=sql)
        elif type == 'when':
            check_sql = check_sql.replace('${tablename}', 'when_ques')
            if len(sqlhelper.ExecQuery(check_sql)) == 0:
                sql = sql.replace('${tablename}' , 'when_ques')
                sqlhelper.ExecNonQuery(sql=sql)
        elif type == 'why':
            check_sql = check_sql.replace('${tablename}', 'why_ques')
            if len(sqlhelper.ExecQuery(check_sql)) == 0:
                sql = sql.replace('${tablename}' , 'why_ques')
                sqlhelper.ExecNonQuery(sql=sql)
        elif type == 'where':
            check_sql = check_sql.replace('${tablename}', 'where_ques')
            if len(sqlhelper.ExecQuery(check_sql)) == 0:
                sql = sql.replace('${tablename}' , 'where_ques')
                sqlhelper.ExecNonQuery(sql=sql)
        elif type == 'which':
            check_sql = check_sql.replace('${tablename}', 'which_ques')
            if len(sqlhelper.ExecQuery(check_sql)) == 0:
                sql = sql.replace('${tablename}' , 'which_ques')
                sqlhelper.ExecNonQuery(sql=sql)
        elif type == 'list_ques':
            check_sql = check_sql.replace('${tablename}', 'list_ques')
            if len(sqlhelper.ExecQuery(check_sql)) == 0:
                sql = sql.replace('${tablename}' , 'list_ques')
                sqlhelper.ExecNonQuery(sql=sql)
        elif type == 'common_ques':
            check_sql = check_sql.replace('${tablename}', 'common_ques')
            if len(sqlhelper.ExecQuery(check_sql)) == 0:
                sql = sql.replace('${tablename}' , 'common_ques')
                print(sql)
                sqlhelper.ExecNonQuery(sql=sql)

    # 4.运行主函数
    def main(self,question):
        # 三步走完结束

        words_list,postags_list,type = self.pretreate(question=question)

        words_list,postags_list,arcs_list = self.compression(words_list=words_list,postags_list=postags_list)

        self.savedb(words_list=words_list,postags_list=postags_list,arcs_list=arcs_list,type=type)

if __name__ == "__main__":
    # 生成并存储模板
    # 读取各个种类的问句

    question_type = ['how_much','how_long','how_do','when','where','which','who','why','list_ques','common_ques']

    extract = Extract()
    # 各个种类的问句
    for type in question_type:
        filename = '/home/wang/data/classification/' + type + '_questions'
        file = open(filename)

        question_list = []
        for line in file:
            question_list.append(line.strip('\n'))

        for question in question_list:
            extract.main(question=question)





