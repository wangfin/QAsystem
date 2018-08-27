# -*- coding: utf-8 -*-
# @Time    : 2018/8/14 10:39
# @Author  : wb
# @File    : generate.py

from extract import Extract
from mysqldb_helper import SQLHelper
from similarity import Similarity
from templatetree import Templatetree
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
        templatetree = Templatetree()

        new_ques = ''

        # 生成出的泛化的句子
        result = templatetree.main(ques_list,model_list)
        if result != None:
            # 把原来问句中的被删除的词填入新的问句中
            new_ques_list = self.revert(ques_list[0],result[1],delete_id)

            for i in new_ques_list:
                new_ques += i

            return new_ques
        else:
            return None

        # if result != None:
        #     return result
        # else:
        #     return None

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

