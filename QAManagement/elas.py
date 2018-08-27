########来源，主题，
from elasticsearch import Elasticsearch
class Elas():
    es = Elasticsearch([{'host': '172.16.14.240', 'port': 9200}])

##############初始化函数##############
    def init(self,myindex):

        # 初始化设置
        _index_mappings = {
            "mappings": {
                "user": {
                     "_all":       { "enabled": False  },
                    "properties": {
                        "question": {"type":"text",
                                   #"include_in_all":True,
                                  "index": True,
                                  "analyzer": "ik_max_word",
                                  "search_analyzer": "ik_max_word"

                                  },
                        "accuratequestion": {"type": "keyword",
                                     #"include_in_all": True,
                                     },
                        "questionfh1": {"type": "text",
                                        # "include_in_all":True,
                                        "index": True,
                                        "analyzer": "ik_max_word",
                                        "search_analyzer": "ik_max_word"

                                        },
                        "questionfh2": {"type": "text",
                                        # "include_in_all":True,
                                        "index": True,
                                        "analyzer": "ik_max_word",
                                        "search_analyzer": "ik_max_word"

                                        },
                        "answer": {"type": "keyword",
                                   "ignore_above":1024,

                                   },
                        "link":{"type":"keyword",},
                        "subject":{"type":"keyword",},



                    }
                },

            }
        }

        self.es.indices.create(index=myindex, body=_index_mappings),    #传入的是Index，函数内使用Index，还有调用时Index的格式应是怎样

##################插入函数##############
    def insert(self,myindex,myquestion,myaccuratequestion,myanswer,mylink,mysubject,myid,qfh1,qfh2):###变量为我们的插入.参数为q,a,id,注意此处的id
        doc = {
            "question": myquestion ,
            "accuratequestion":myaccuratequestion,
            "questionfh1": qfh1,
            "questionfh2": qfh2,
             "answer" :myanswer,
            "link":mylink,
            "subject":mysubject

        }

        res = self.es.index(index=myindex, doc_type='user', body=doc,id=myid)  # 插入数据

        return res

        #self.es.indices.refresh(index=myindex)

    #################查询函数###########################

    '''def search(self,myindex,s1):##变量为用户的提问，返回值为
       res = self.es.search(index=myindex,size=5,body={"query": {"match": {"question": s1}}})
       print(res['hits']['hits'])







       for hit in res['hits']['hits'] :  # 根据打分返回查询，并且前三个/前五个
           # print("Got %d Hits:" % res['hits']['total'])
            #  print("%(question)s" % hit["_source"])
           # print(hit['_score'], hit['_source']['answer'])  # 对某一项的打分
           print(hit['_score'], hit['_source']['answer'])

        return res['hits']['hits']'''
# s1是当前问题，s2是之前的问题
    def multisearch(self,myindex,s1,s2):
        body = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "multi_match": {
                                "query": s1,
                                "fields": ["question", "questionfh1", "questionfh2"],
                                "boost": 3
                            }
                        },
                        {
                            "multi_match": {
                                "query": s2,
                                "fields": ["question", "questionfh1", "questionfh2"],
                                "boost": 1
                            }
                        }
                    ]
                }
            }
        }
        res=self.es.search(index=myindex,size=5, body=body)
        return res['hits']['hits']

    def accuratesearch(self,myindex,s1):# 变量为用户的提问，返回值为
        res = self.es.search(index=myindex,doc_type="user",body=
        {"query":{
            "constant_score": {
                "filter": {

                    "term": {
                        "accuratequestion": s1,
                        }
                }
            }

          }
        })




        for hit in res['hits']['hits']:  # 根据打分返回查询，并且前三个/前五个

            return hit['_source']

    def furthersearch(self,myindex,s1,s2):
        body = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "multi_match": {
                                "query": s1,
                                "fields": ["question", "questionfh1", "questionfh2"],
                                "boost": 3
                            }
                        },
                        {
                            "multi_match": {
                                "query": s2,
                                "fields": ["question", "questionfh1", "questionfh2"],
                                "boost": 1
                            }
                        }
                    ]
                }
            }
        }
        res = self.es.search(index=myindex, from_=1,size=5, body=body)



        return res['hits']['hits']

    def searchall(self, myindex):  # 查询所有，返回的是return res['hits']['hits']，之后你可以用for hit in res['hits']['hits'] : print(hit['_source']['answer'])获得单项数据
        result = []
        res = self.es.search(index=myindex, doc_type='user', size=10000,body={"query": {"match_all": {}}})
        for hit in res['hits']['hits']:
            result.append(hit)
        #print(len(res['hits']['hits']))
        return result

    def deleteone(self,myindex,id):#删除单个，我没有写返回值
        res=self.es.delete(index=myindex,doc_type='user',id=id)

        return res

    def deleteall(self,myindex):
        res=self.es.indices.delete(index=myindex,ignore=[400, 404])

    ####修改函数，支持问题修改和答案修改，调用时要分开调用,因为不是查询，所有没有写返回值，你可以考虑下是写返回值，还是修改后通过search查看。
    def updateqa(self, myindex, myquestion,myanswer, mylink,mysubject,hitid,qfh1,qfh2):  # 修改问题，同时精确问题域也要被修改
        res = self.es.update(index=myindex, doc_type='user', id=hitid,
                            body={"doc": {"question": myquestion, "accuratequestion": myquestion,"answer":myanswer,"link":mylink,"subject":mysubject,"questionfh1": qfh1,"questionfh2": qfh2}})

    def idsearch(self,myindex,myid):
        result = []
        res=self.es.get(index=myindex, doc_type='user', id=myid)
        result.append(res)
        return result

    def oldinsert(self,myindex,myquestion,myanswer,myid):###变量为我们的插入.参数为q,a,id,注意此处的id
        doc = {
            "question": myquestion ,

             "answer" :myanswer

        }
        res = self.es.index(index=myindex, doc_type='user', body=doc,id=myid)  # 插入数据

    def multisearch_forall(self,myindex,s1):
        body = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "multi_match": {
                                "query": s1,
                                "fields": ["question", "questionfh1", "questionfh2"],
                                "boost": 3
                            }
                        }
                    ]
                }
            }
        }
        res=self.es.search(index=myindex,size=5, body=body)
        return res['hits']['hits']

