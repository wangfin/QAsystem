# 配置同义问题，多域查找，选一个分最高的保存为自己的分。问题：怎么插入，body的结构是怎样的？解决方法：多匹配查询
'''GET / _search
{
  “query”：{
    “multi_match”：{
      “query”：“brown fox”，
      “type”：“best_fields”，
      “fields”：[“subject”，“message”]，
      “tie_breaker”：0.3
    }
  }
}'''





########历史搜索记录
#######热点搜索
#######数据挖掘对搜索的影响：最有可能搜索的东西

from .elas import Elas
myelas = Elas()
# import elas
#
# myelas = elas.Elas()
####插入
# myelas.init('index35')






class Withweb:
    def webinit(self,myindex):
        myelas.init(myindex)


    def webinsert(self,myindex,q,accurateq,a,link,subject,myid):
        res = myelas.insert(myindex,q,accurateq,a,link,subject,myid)

        return res


    def accurate_search(self,amyindex,aq):
        answer = myelas.accuratesearch(amyindex, aq)
        return answer



    def buwan_search(self,myindex,q):
        # 补完搜索阶段
		# 创建返回结果集
        results = []
        # 如果有，显示五个
        # 返回的是相近的问题
        if (myelas.search(myindex,q)):

            for hit in myelas.search(myindex, q):  # 根据打分返回查询，并且前三个/前五个

                results.append(hit['_source']['question'])

            return results

    # 如果点击了某一个，则调用精确搜索
    # def accurate_search(self,myindex,q):
    #     answer = self.accuratesearch(myindex,q)
    #     print(answer)
    #     return answer

        #####如果点击了某一个，则调用精确搜索。
        #self.accuratesearch(amyindex,aq)



    ############enter搜索阶段
    def enter_search(self,myindex,q):

        if (myelas.search(myindex, q)):
            ###先找到最大值，再把它和其他四个比较，如果大于，直接返回，否则：
            maxscore = 0
            maxanswer = ''
            totalscore = 0
            results = []
            for hit in myelas.search(myindex,q):  #####只有五个
                totalscore = totalscore + hit['_score']

                if hit['_score'] > maxscore:
                    maxscore = hit['_score']
                    maxanswer = hit['_source']['answer']
                print(hit['_score'])

            print(totalscore)
            if maxscore > totalscore - maxscore:
                results.append(maxanswer)
                return results
            else:
                #######显示五个
                for hit in myelas.search(myindex,  q):  # 根据打分返回查询，并且前三个/前五个
                    #print(hit['_source']['answer'])
                    results.append(hit['_source']['question'])
                return results



        ##如果点了都不是
        else:
            #print('查询不到结果，请您重新输入')
            result = '根据您搜索的内容，查询不到结果，请您重新输入'
            return result




    def further_search(self,myindex,preq):
        results = []
        #######进一步推荐搜索
        if (myelas.furthersearch(myindex, preq)):


            #######显示五个
            for hit in myelas.furthersearch(myindex, preq):  # 根据打分返回查询，并且前三个/前五个

                results.append(hit['_source']['question'])

            return results

        ##如果点了都不是
        else:
            return results

    # 删除一个
    def single_delete(self,myindex, id):
        res = myelas.deleteone(myindex,id)
        return res

    # 删除整张表
    def all_delete(self, myindex):
        myelas.deleteall(myindex)

    # 搜索全部的
    def searchall(self,myindex):
        return myelas.searchall(myindex)

    # 修改qa
    def update(self,myindex, question,answer, link,subject,hitid):
        myelas.updateqa(myindex,question,answer,link,subject,hitid)


    # 返回10个的搜索，用于管理员页面进行搜索的场景

    def search_by_question(self,myindex,q):
        # 管理员查询问题
        # 创建返回结果集
        results = []
        # 如果有，显示10个
        if (myelas.search(myindex,q)):

            for hit in myelas.search(myindex ,q):  # 根据打分返回查询，并且前三个/前五个

                results.append(hit)

            return results
        else:
            print('无结果')

            return results

    # 通过id搜索，只返回一个
    def search_by_id(self,myindex,myid):

        result = myelas.idsearch(myindex,myid)
        print(result)

        return result


