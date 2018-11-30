# -*- coding: utf-8 -*-
# @Time    : 2018/8/14 10:39
# @Author  : wb
# @File    : generate.py

from QAManagement.question_generalization.extract import Extract
import requests

from QAManagement.question_generalization.mysqldb_helper import SQLHelper
from QAManagement.question_generalization.similarity import Similarity
# from QAManagement.question_generalization.templatetree import Templatetree
from QAManagement.ques_generate.LTML import LTML
# 问句泛化

# 之前已经生成好了问句模板
# 接下来通过问句模板构建问句泛化

class Generate():

    # 1.读取需要泛化的句子
    def read(self,question):

        # 对问句同样进行处理
        # 使用extract中的预处理模块，对输入的问句进行分词，词性标注，关键词标注
        extract = Extract()

        words_list,postags_list,type = extract.pretreate(question=question)

        return [words_list, postags_list, type]

    # 2.压缩输入的问句
    def compression(self, words_list, postags_list):
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
            if postags_list[i] == 'a' and postags_list[i + 1] == 'n':
                delete_id.append(i)
            elif postags_list[i] == 'd' and postags_list[i + 1] == 'a':
                delete_id.append(i)
            elif postags_list[i] == 'a' and postags_list[i + 1] == 'a' and i != 0:
                delete_id.append(i)
            elif postags_list[i] == 'u' and postags_list[i + 1] == 'a':
                delete_id.append(i)
            elif postags_list[i] == 'u' and postags_list[i + 1] == 'd':
                delete_id.append(i)
            elif postags_list[i] == 'n' and postags_list[i + 1] == 'n':
                delete_id.append(i)
            elif postags_list[i] == 'b' and postags_list[i + 1] == 'n':
                delete_id.append(i)
            elif postags_list[i] == 'j' and postags_list[i + 1] == 'n':
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
        return [words_list,postags_list,arcs_list,delete_id]

    # 3.根据问句的种类，读取数据库中的模版
    def readtemplate(self,words_list,postags_list,arcs_list,type,delete_id):

        sqlhelper = SQLHelper(host=SQLHelper.host,user=SQLHelper.username,pwd=SQLHelper.password,db=SQLHelper.database)
        similarity = Similarity()

        # template = ' '.join(postags_list)
        # 读取数据库中保存的模板
        # 查询所有的模版
        # check_sql = "SELECT question FROM ${tablename}"
        # check_sim_sql = "SELECT * FROM ${tablename} WHERE question=${}"


        # 需要输入tree的ques_list
        ques_list = []
        ques_list.append(words_list)
        ques_list.append(postags_list)
        ques_list.append(arcs_list)

        # 泛化出的新的问句
        new_questions = []

        if type == 'how_long':
            check_sql = "SELECT question FROM how_long_ques"
            result = sqlhelper.ExecQuery(check_sql)
            # 找到所有的模板中和输入的句子相似度最高的10个句子
            # 输入需要泛化的问句和所有的句子

            # 获取数据库中的模板问句
            model_sen_list = []
            for model in result:
                model_sen_list.append(model[0].split())
            similar_model = similarity.main(words_list,model_sen_list)
            # result的格式为{model:score}

            # 相似度最高的十条模板
            topten = self.topnum(similar_model,10)
            # topten返回值[{'cccc': 10},{'aaaa',9}]

            for model in topten:
                # 查询指定model的template和dependparse
                check_sim_sql = "SELECT * FROM how_long_ques WHERE question="+"'"+list(model.keys())[0]+"'"
                result = sqlhelper.ExecQuery(check_sim_sql)
                '''
                需要获取的数据为
                输入问句分词words_list
                输入词性postags_list
                输入关系arcs_list
                '''
                model_words_list = []
                model_postags_list = []
                model_arcs_list = []
                for res in result:
                    model_words_list.append(res[1].split())
                    model_postags_list.append(res[2].split())
                    model_arcs_list.append(res[3].split())
                # 需要输入tree的model_list
                model_list = model_words_list + model_postags_list + model_arcs_list
                new_question = self.generalize(ques_list=ques_list,model_list=model_list,delete_id=delete_id)
                if new_question != None:
                    new_questions.append(new_question)

        elif type == 'how_much':
            check_sql = "SELECT question FROM how_much_ques"
            result = sqlhelper.ExecQuery(check_sql)
            # 找到所有的模板中和输入的句子相似度最高的10个句子
            # 输入需要泛化的问句和所有的句子

            # 获取数据库中的模板问句
            model_sen_list = []
            for model in result:
                model_sen_list.append(model[0].split())
            similar_model = similarity.main(words_list,model_sen_list)
            # result的格式为{model:score}

            # 相似度最高的十条模板
            topten = self.topnum(similar_model,10)
            # topten返回值[{'cccc': 10},{'aaaa',9}]

            for model in topten:
                # 查询指定model的template和dependparse
                check_sim_sql = "SELECT * FROM how_much_ques WHERE question="+"'"+list(model.keys())[0]+"'"
                result = sqlhelper.ExecQuery(check_sim_sql)

                '''
                需要获取的数据为
                输入问句分词words_list
                输入词性postags_list
                输入关系arcs_list
                '''
                model_words_list = []
                model_postags_list = []
                model_arcs_list = []

                for res in result:
                    model_words_list.append(res[1].split())
                    model_postags_list.append(res[2].split())
                    model_arcs_list.append(res[3].split())
                # 需要输入tree的model_list
                model_list = model_words_list + model_postags_list + model_arcs_list
                new_question = self.generalize(ques_list=ques_list, model_list=model_list, delete_id=delete_id)
                if new_question != None:
                    new_questions.append(new_question)

        elif type == 'how_do':
            check_sql = "SELECT question FROM how_do_ques"
            result = sqlhelper.ExecQuery(check_sql)
            # 找到所有的模板中和输入的句子相似度最高的10个句子
            # 输入需要泛化的问句和所有的句子

            # 获取数据库中的模板问句
            model_sen_list = []
            for model in result:
                model_sen_list.append(model[0].split())
            similar_model = similarity.main(words_list,model_sen_list)
            # result的格式为{model:score}

            # 相似度最高的十条模板
            topten = self.topnum(similar_model,10)
            # topten返回值[{'cccc': 10},{'aaaa',9}]

            for model in topten:
                # 查询指定model的template和dependparse
                check_sim_sql = "SELECT * FROM how_do_ques WHERE question="+"'"+list(model.keys())[0]+"'"
                result = sqlhelper.ExecQuery(check_sim_sql)

                '''
                需要获取的数据为
                输入问句分词words_list
                输入词性postags_list
                输入关系arcs_list
                '''
                model_words_list = []
                model_postags_list = []
                model_arcs_list = []

                for res in result:
                    model_words_list.append(res[1].split())
                    model_postags_list.append(res[2].split())
                    model_arcs_list.append(res[3].split())
                # 需要输入tree的model_list
                model_list = model_words_list + model_postags_list + model_arcs_list
                new_question = self.generalize(ques_list=ques_list, model_list=model_list, delete_id=delete_id)
                if new_question != None:
                    new_questions.append(new_question)

        elif type == 'who':
            check_sql = "SELECT question FROM who_ques"
            result = sqlhelper.ExecQuery(check_sql)
            # 找到所有的模板中和输入的句子相似度最高的10个句子
            # 输入需要泛化的问句和所有的句子

            # 获取数据库中的模板问句
            model_sen_list = []
            for model in result:
                model_sen_list.append(model[0].split())
            similar_model = similarity.main(words_list,model_sen_list)
            # result的格式为{model:score}

            # 相似度最高的十条模板
            topten = self.topnum(similar_model,10)
            # topten返回值[{'cccc': 10},{'aaaa',9}]

            for model in topten:
                # 查询指定model的template和dependparse
                check_sim_sql = "SELECT * FROM who_ques WHERE question="+"'"+list(model.keys())[0]+"'"
                result = sqlhelper.ExecQuery(check_sim_sql)

                '''
                需要获取的数据为
                输入问句分词words_list
                输入词性postags_list
                输入关系arcs_list
                '''
                model_words_list = []
                model_postags_list = []
                model_arcs_list = []

                for res in result:
                    model_words_list.append(res[1].split())
                    model_postags_list.append(res[2].split())
                    model_arcs_list.append(res[3].split())
                # 需要输入tree的model_list
                model_list = model_words_list + model_postags_list + model_arcs_list
                new_question = self.generalize(ques_list=ques_list, model_list=model_list, delete_id=delete_id)
                if new_question != None:
                    new_questions.append(new_question)

        elif type == 'when':
            check_sql = "SELECT question FROM when_ques"
            result = sqlhelper.ExecQuery(check_sql)
            # 找到所有的模板中和输入的句子相似度最高的10个句子
            # 输入需要泛化的问句和所有的句子

            # 获取数据库中的模板问句
            model_sen_list = []
            for model in result:
                model_sen_list.append(model[0].split())
            similar_model = similarity.main(words_list,model_sen_list)
            # result的格式为{model:score}

            # 相似度最高的十条模板
            topten = self.topnum(similar_model,10)
            # topten返回值[{'cccc': 10},{'aaaa',9}]

            for model in topten:
                # 查询指定model的template和dependparse
                check_sim_sql = "SELECT * FROM when_ques WHERE question="+"'"+list(model.keys())[0]+"'"
                result = sqlhelper.ExecQuery(check_sim_sql)

                '''
                需要获取的数据为
                输入问句分词words_list
                输入词性postags_list
                输入关系arcs_list
                '''
                model_words_list = []
                model_postags_list = []
                model_arcs_list = []

                for res in result:
                    model_words_list.append(res[1].split())
                    model_postags_list.append(res[2].split())
                    model_arcs_list.append(res[3].split())
                # 需要输入tree的model_list
                model_list = model_words_list + model_postags_list + model_arcs_list
                new_question = self.generalize(ques_list=ques_list, model_list=model_list, delete_id=delete_id)
                if new_question != None:
                    new_questions.append(new_question)

        elif type == 'why':
            check_sql = "SELECT question FROM why_ques"
            result = sqlhelper.ExecQuery(check_sql)
            # 找到所有的模板中和输入的句子相似度最高的10个句子
            # 输入需要泛化的问句和所有的句子

            # 获取数据库中的模板问句
            model_sen_list = []
            for model in result:
                model_sen_list.append(model[0].split())
            similar_model = similarity.main(words_list,model_sen_list)
            # result的格式为{model:score}

            # 相似度最高的十条模板
            topten = self.topnum(similar_model,10)
            # topten返回值[{'cccc': 10},{'aaaa',9}]

            for model in topten:
                # 查询指定model的template和dependparse
                check_sim_sql = "SELECT * FROM why_ques WHERE question="+"'"+list(model.keys())[0]+"'"
                result = sqlhelper.ExecQuery(check_sim_sql)

                '''
                需要获取的数据为
                输入问句分词words_list
                输入词性postags_list
                输入关系arcs_list
                '''
                model_words_list = []
                model_postags_list = []
                model_arcs_list = []

                for res in result:
                    model_words_list.append(res[1].split())
                    model_postags_list.append(res[2].split())
                    model_arcs_list.append(res[3].split())
                # 需要输入tree的model_list
                model_list = model_words_list + model_postags_list + model_arcs_list
                new_question = self.generalize(ques_list=ques_list, model_list=model_list, delete_id=delete_id)
                if new_question != None:
                    new_questions.append(new_question)

        elif type == 'where':
            check_sql = "SELECT question FROM where_ques"
            result = sqlhelper.ExecQuery(check_sql)
            # 找到所有的模板中和输入的句子相似度最高的10个句子
            # 输入需要泛化的问句和所有的句子

            # 获取数据库中的模板问句
            model_sen_list = []
            for model in result:
                model_sen_list.append(model[0].split())
            similar_model = similarity.main(words_list,model_sen_list)
            # result的格式为{model:score}

            # 相似度最高的十条模板
            topten = self.topnum(similar_model,10)
            # topten返回值[{'cccc': 10},{'aaaa',9}]

            for model in topten:
                # 查询指定model的template和dependparse
                check_sim_sql = "SELECT * FROM where_ques WHERE question="+"'"+list(model.keys())[0]+"'"
                result = sqlhelper.ExecQuery(check_sim_sql)

                '''
                需要获取的数据为
                输入问句分词words_list
                输入词性postags_list
                输入关系arcs_list
                '''
                model_words_list = []
                model_postags_list = []
                model_arcs_list = []

                for res in result:
                    model_words_list.append(res[1].split())
                    model_postags_list.append(res[2].split())
                    model_arcs_list.append(res[3].split())
                # 需要输入tree的model_list
                model_list = model_words_list + model_postags_list + model_arcs_list
                new_question = self.generalize(ques_list=ques_list, model_list=model_list, delete_id=delete_id)
                if new_question != None:
                    new_questions.append(new_question)

        elif type == 'which':
            check_sql = "SELECT question FROM which_ques"
            result = sqlhelper.ExecQuery(check_sql)
            # 找到所有的模板中和输入的句子相似度最高的10个句子
            # 输入需要泛化的问句和所有的句子

            # 获取数据库中的模板问句
            model_sen_list = []
            for model in result:
                model_sen_list.append(model[0].split())
            similar_model = similarity.main(words_list,model_sen_list)
            # result的格式为{model:score}

            # 相似度最高的十条模板
            topten = self.topnum(similar_model,10)
            # topten返回值[{'cccc': 10},{'aaaa',9}]

            for model in topten:
                # 查询指定model的template和dependparse
                check_sim_sql = "SELECT * FROM which_ques WHERE question="+"'"+list(model.keys())[0]+"'"
                result = sqlhelper.ExecQuery(check_sim_sql)

                '''
                需要获取的数据为
                输入问句分词words_list
                输入词性postags_list
                输入关系arcs_list
                '''
                model_words_list = []
                model_postags_list = []
                model_arcs_list = []

                for res in result:
                    model_words_list.append(res[1].split())
                    model_postags_list.append(res[2].split())
                    model_arcs_list.append(res[3].split())
                # 需要输入tree的model_list
                model_list = model_words_list + model_postags_list + model_arcs_list
                new_question = self.generalize(ques_list=ques_list, model_list=model_list, delete_id=delete_id)
                if new_question != None:
                    new_questions.append(new_question)

        elif type == 'list_ques':
            check_sql = "SELECT question FROM list_ques"
            result = sqlhelper.ExecQuery(check_sql)
            # 找到所有的模板中和输入的句子相似度最高的10个句子
            # 输入需要泛化的问句和所有的句子

            # 获取数据库中的模板问句
            model_sen_list = []
            for model in result:
                model_sen_list.append(model[0].split())
            similar_model = similarity.main(words_list,model_sen_list)
            # result的格式为{model:score}

            # 相似度最高的十条模板
            topten = self.topnum(similar_model,10)
            # topten返回值[{'cccc': 10},{'aaaa',9}]

            for model in topten:
                # 查询指定model的template和dependparse
                check_sim_sql = "SELECT * FROM list_ques WHERE question="+"'"+list(model.keys())[0]+"'"
                result = sqlhelper.ExecQuery(check_sim_sql)

                '''
                需要获取的数据为
                输入问句分词words_list
                输入词性postags_list
                输入关系arcs_list
                '''
                model_words_list = []
                model_postags_list = []
                model_arcs_list = []

                for res in result:
                    model_words_list.append(res[1].split())
                    model_postags_list.append(res[2].split())
                    model_arcs_list.append(res[3].split())
                # 需要输入tree的model_list
                model_list = model_words_list + model_postags_list + model_arcs_list
                new_question = self.generalize(ques_list=ques_list, model_list=model_list, delete_id=delete_id)
                if new_question != None:
                    new_questions.append(new_question)

        elif type == 'common_ques':
            check_sql = "SELECT question FROM common_ques"
            result = sqlhelper.ExecQuery(check_sql)
            # 找到所有的模板中和输入的句子相似度最高的10个句子
            # 输入需要泛化的问句和所有的句子

            # 获取数据库中的模板问句
            model_sen_list = []
            for model in result:
                model_sen_list.append(model[0].split())
            similar_model = similarity.main(words_list,model_sen_list)
            # result的格式为{model:score}

            # 相似度最高的十条模板
            topten = self.topnum(similar_model,10)
            # topten返回值[{'cccc': 10},{'aaaa',9}]

            print('最相近的10条语句'+str(topten))

            for model in topten:
                # 查询指定model的template和dependparse
                check_sim_sql = "SELECT * FROM common_ques WHERE question="+"'"+list(model.keys())[0]+"'"
                # print(check_sim_sql)
                result = sqlhelper.ExecQuery(check_sim_sql)
                # model_list = []
                '''
                需要获取的数据为
                输入问句分词words_list
                输入词性postags_list
                输入关系arcs_list
                '''
                model_words_list = []
                model_postags_list = []
                model_arcs_list = []
                for res in result:
                    model_words_list.append(res[1].split())
                    model_postags_list.append(res[2].split())
                    model_arcs_list.append(res[3].split())
                # 需要输入tree的model_list
                model_list = model_words_list + model_postags_list + model_arcs_list
                # print('readtemplate的modellist'+str(model_list))
                new_question = self.generalize(ques_list=ques_list, model_list=model_list, delete_id=delete_id)
                if new_question != None:
                    new_questions.append(new_question)

        return new_questions

    # 辅助函数
    # 找到数组中最大的几个数，k是最大的几个
    # 但这个数组中的每一个值都是dict，就是对里面元素是dict的排序
    def topnum(self,num_list,k):
        # 求其中的最大的10个数
        maxlist = []  # 最大值数组（TopK数组），也就是最后的结果存放地方
        for i in range(0, k):  # 先将目标数组前10个数放到TopK数组
            maxlist.append(num_list[i])

        maxlist.sort(key=lambda k: list(k.values())[0], reverse=True) # 对这个存有10个最大值数组（TopK数组）进行降序排序

        for i in range(k, len(num_list)):  # 对目标数组之后的数字
            if list(num_list[i].values())[0] > list(maxlist[k - 1].values())[0]:  # 如果你大于最大值数组（TopK数组）的最后一个数，因为进行过排序，也就是其中的最小值
                maxlist.pop()  # 那最大值数组（TopK数组）最后一个数，因为进行过排序，也就是其中的最小值滚出
                maxlist.append(num_list[i])  # 那你这个数就进入这个最大值数组（TopK数组）
                maxlist.sort(key=lambda k: list(k.values())[0], reverse=True)  # 之后，我们再对最大值数组（TopK数组）进行降序排序

        return maxlist


    # 泛化函数
    # 输入原始问句，泛化模板
    def generalize(self,ques_list,model_list,delete_id):
        # question = '淘宝 一般 多久 自动 确认 收货 ？'nz a how_long d v n wp
        # model = '淘宝 自动 确认 时间 是 多久 ？'nz d v n modal how_long wp

        # 句子成分之间的关系包含，并且相同词性可以替换
        # 调用tree

        # 输入ques_list和model_list
        # 这两个list中包含三个list
        # 输入问句分词words_list
        # 输入词性postags_list
        # 输入关系arcs_list
        # templatetree = Templatetree()
        #
        # new_ques = ''
        #
        # # 生成出的泛化的句子
        # result = templatetree.main(ques_list,model_list)
        # if result != None:
        #     # 把原来问句中的被删除的词填入新的问句中
        #     new_ques_list = self.revert(ques_list[0],result[1],delete_id)
        #
        #     for i in new_ques_list:
        #         new_ques += i
        #
        #     return new_ques
        # else:
        #     return None

        # if result != None:
        #     return result
        # else:
        #     return None


        # 想到另外一种可能更好的方法，使用语义角色标注
        # roles = Generate.labeller.label(ques_list[0], ques_list[1], ques_list[2])  # 语义角色标注
        # 打印结果
        # for role in roles:
        #     print(role.index,
        #           "".join(["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))

        ques_result = self.ltp_request(ques_list[0])
        model_result = self.ltp_request(model_list[0])

        ques_a0 = 0
        ques_a1 = 0
        model_a0 = 0
        model_a1 = 0

        # for ques_arc in ques_result:
        #     for model_arc in model_result:
        #         # 找根节点
        #         if ques_arc['semrelate'] == 'Root' and model_arc['semrelate'] == 'Root':
        #             # 找出其中的语义角色
        #             if len(ques_arc['arg']) != 0 and len(model_arc['arg']) != 0:
        #                 # 如果A0，A1这些都有的话，那么就可以替换了
        #                 # list_c = [a['type'] for a in ques_arc['arg'][i] if a in model_arc['arg'][j] for i in range(len(ques_arc['arg'])) for j in range(len(model_arc['arg']))]
        #                 # 找其中的一个A0
        #                 for i in ques_arc['arg']:
        #                     if i['type'] == 'A0':
        #                         for j in model_arc['arg']:
        #                             if j['type'] == 'A0':
        #
        #                     elif i['type'] == 'A1':

        # 匹配A0，A1的个数
        for ques_arc in ques_result:
            if ques_arc['semrelate'] == 'Root':
            # 找出其中的语义角色
                if len(ques_arc['arg']) != 0:
                # 找出其中所有的a0和a1的个数
                    for i in ques_arc['arg']:
                        if i['type'] == 'A0':
                            ques_a0 += 1
                        elif i['type'] == 'A1':
                            ques_a1 += 1

        # 匹配A0，A1的个数
        for model_arc in model_result:
            if model_arc['semrelate'] == 'Root':
                # 找出其中的语义角色
                if len(model_arc['arg']) != 0:
                    # 找出其中所有的a0和a1的个数
                    for i in model_arc['arg']:
                        if i['type'] == 'A0':
                            model_a0 += 1
                        elif i['type'] == 'A1':
                            model_a1 += 1
        print(ques_a1)
        print(model_a1)
        if ques_a1 == model_a1:
            print('开始生成')
            # 那么就是可以替换的句子
            # 替换的方式是将所有的与root相关的组进行替换
            # 只能将原句替换到模板句上
            for ques_arc in ques_result:
                for model_arc in model_result:
                    # 找根节点
                    if ques_arc['semrelate'] == 'Root' and model_arc['semrelate'] == 'Root':
                        print('两个的Root')
                        # 找出其中的语义角色
                        if len(ques_arc['arg']) != 0 and len(model_arc['arg']) != 0:
                            print('arc是否存在'+str(ques_arc['arg'])+';'+str(model_arc['arg']))
                            # 如果A0，A1这些都有的话，那么就可以替换了
                            # list_c = [a['type'] for a in ques_arc['arg'][i] if a in model_arc['arg'][j] for i in range(len(ques_arc['arg'])) for j in range(len(model_arc['arg']))]
                            # 找其中的一个A0
                            for i in range(len(ques_arc['arg'])):
                                if ques_arc['arg'][i]['type'] == 'A0':
                                    for j in range(len(model_arc['arg'])):
                                        # 两边都是A0
                                        if model_arc['arg'][j]['type'] == 'A0':
                                            print('找到了两个都是A0')
                                            if i != 0 and ques_arc['arg'][i-1]['end'] +1 == ques_arc['arg'][i]['beg'] and ques_arc['arg'][i-1]['type'] != 'A1':
                                                print('开始生成1')
                                                # 开始替换
                                                # for x in range(ques_arc['arg'][i-1]['end'],ques_arc['arg'][i]['end']):
                                                #     model_list[0][x] = ques_list[0][x]
                                                model_list[0][int(ques_arc['arg'][j]['beg'])-1:int(ques_arc['arg'][j]['end'])-1] = ques_list[0][int(ques_arc['arg'][i-1]['beg'])-1:int(ques_arc['arg'][i]['end'])-1]

                                            elif i != len(ques_arc['arg']) -1 and ques_arc['arg'][i+1]['beg'] == ques_arc['arg'][i]['end'] +1 and ques_arc['arg'][i+1]['type'] != 'A1':
                                                print('开始生成2')
                                                model_list[0][int(ques_arc['arg'][j]['beg'])-1:int(
                                                    ques_arc['arg'][j]['end'])-1] = ques_list[0][int(
                                                    ques_arc['arg'][i]['beg'])-1:int(ques_arc['arg'][i+1]['end'])-1]

                                            # elif ques_arc['arg'][i-1]['end']+1 == ques_arc['arg'][i]['beg'] and ques_arc['arg'][i+1]['beg'] == ques_arc['arg'][i]['end']+1:
                                            #     print('开始生成3')
                                            #     model_list[0][int(ques_arc['arg'][j]['beg'])-1:int(
                                            #         ques_arc['arg'][j]['end'])-1] = ques_list[0][int(
                                            #         ques_arc['arg'][i-1]['beg'])-1:int(ques_arc['arg'][i + 1]['end'])-1]
                                            else:
                                                print('开始生成4')
                                                model_list[0][int(ques_arc['arg'][j]['beg'])-1:int(
                                                    ques_arc['arg'][j]['end'])-1] = ques_list[0][int(
                                                    ques_arc['arg'][i]['beg'])-1:int(ques_arc['arg'][i]['end'])-1]

                                elif ques_arc['arg'][i]['type'] == 'A1':
                                    for j in range(len(model_arc['arg'])):
                                        # 两边都是A1
                                        if model_arc['arg'][j]['type'] == 'A1':
                                            print('找到了两个都是A1')
                                            if i != 0 and ques_arc['arg'][i - 1]['end']+1 == ques_arc['arg'][i]['beg'] and \
                                                    ques_arc['arg'][i - 1]['type'] != 'A0':
                                                print('生成a1')
                                                # 开始替换
                                                # for x in range(ques_arc['arg'][i-1]['end'],ques_arc['arg'][i]['end']):
                                                #     model_list[0][x] = ques_list[0][x]
                                                model_list[0][
                                                int(ques_arc['arg'][j]['beg'])-1:int(ques_arc['arg'][j]['end'])-1] = ques_list[0][int(
                                                    ques_arc['arg'][i - 1]['beg'])-1:int(ques_arc['arg'][i]['end'])-1]

                                            elif i != len(ques_arc['arg']) - 1and ques_arc['arg'][i + 1]['beg'] == \
                                                    ques_arc['arg'][i]['end']+1 and ques_arc['arg'][i - 1]['type'] != 'A0':
                                                print('生成')
                                                model_list[0][int(ques_arc['arg'][j]['beg'])-1:int(
                                                    ques_arc['arg'][j]['end'])-1] = ques_list[0][int(
                                                    ques_arc['arg'][i]['beg'])-1:int(ques_arc['arg'][i + 1]['end'])-1]

                                            elif ques_arc['arg'][i - 1]['end']+1 == ques_arc['arg'][i]['beg'] and \
                                                    ques_arc['arg'][i + 1]['beg'] == ques_arc['arg'][i]['end']+1:
                                                print('找到了两个都是A0')
                                                model_list[0][int(ques_arc['arg'][j]['beg'])-1:int(
                                                    ques_arc['arg'][j]['end'])-1] = ques_list[0][int(
                                                    ques_arc['arg'][i - 1]['beg'])-1:int(ques_arc['arg'][i + 1]['end'])-1]
                                            else:
                                                print('找到了两个都是A0')
                                                model_list[0][int(ques_arc['arg'][j]['beg'])-1:int(
                                                    ques_arc['arg'][j]['end'])-1] = ques_list[0][int(
                                                    ques_arc['arg'][i]['beg'])-1:int(ques_arc['arg'][i]['end'])-1]
                        else:
                            print('不生成')
                    else:
                        print('不生成')


        print(model_list[0])





    # 还原函数
    # 还原被简化的问句
    def revert(self,words_list,new_question_list,delete_id):
        # 原来的句子words_list
        # 根据deleteid找出原来被删除的字
        delete_word = []
        for i in delete_id:
            delete_word.append(words_list[int(i)])
        # 找出这个词原来搭配的词
        pair_word = []
        for i in delete_id:
            pair_word.append(words_list[int(i) + 1])

        for i in range(len(pair_word)):
            for new_question in new_question_list:
                if pair_word[i] == new_question:
                    new_question = delete_word[i] + pair_word[i]

        return new_question_list


    # 运行主函数
    def main(self, question):
        words_list, postags_list, type = self.read(question=question)
        words_list, postags_list, arcs_list, delete_id = self.compression(words_list=words_list,postags_list=postags_list)
        new_questions = self.readtemplate(words_list,postags_list,arcs_list,type,delete_id)

        return new_questions

    # 发送LTP请求的函数
    def ltp_request(self, sentence_list):
        # line = '虚拟化驱动不正常时网络、存储性能降低。'
        # words = Paragraph.segmentor.segment(sentence)  # 分词
        # words_list = list(words)
        # print(words_list)

        # LTML用于构建自定义分词的xml，用于向LTP云传入args
        ltml = LTML()
        ltml.build_from_words(sentence_list)
        xml = ltml.tostring()
        # print(xml)

        url_get_base = "https://api.ltp-cloud.com/analysis/"

        # 这个是加入自定义词典的参数
        args = {
            'api_key': 'a1R923E7s37daeNz7dsMeXiTexWGoookJX2HONwC',
            'pattern': 'all',
            'format': 'json',
            'xml_input': 'true',
            'text': xml
        }

        r = requests.post(url_get_base, data=args)

        content = r.json()

        # for i in content[0][0]:
        #     print(i)

        return content[0][0]
