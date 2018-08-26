from QAManagement.elas import Elas
from QAManagement.elas_f_k1 import k1
from QAManagement.elas_f_k2 import k2
myelas = Elas()
myk1=k1()
myk2=k2()
# import elas
#
# myelas = elas.Elas()
####插入
# myelas.init('index35')






class Withweb_all():
    def webinit(self,myindex):
        myelas.init(myindex)
    def initk1(self,myindex):
        myk1.init(myindex)
    def initk2(self,myindex):
        myk2.init(myindex)

    def webinsert(self,myindex,q,accurateq,a,link,subject,myid,qf1,qf2):
        res = myelas.insert(myindex,q,accurateq,a,link,subject,myid,qf1,qf2)

        return res



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
    def update(self,myindex, question,answer, link,subject,hitid,qfh1,qfh2):
        myelas.updateqa(myindex,question,answer,link,subject,hitid,qfh1,qfh2)


    # 返回10个的搜索，用于管理员页面进行搜索的场景

    def search_by_question(self,myindex,q):
        # 管理员查询问题
        # 创建返回结果集
        results = []
        # 如果有，显示10个
        if (myelas.multisearch_forall(myindex,q)):

            for hit in myelas.multisearch_forall(myindex ,q):  # 根据打分返回查询，并且前三个/前五个

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


