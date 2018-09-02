from elasticsearch import Elasticsearch


class k2():
    es = Elasticsearch([{'host': '172.16.14.240', 'port': 9200}])

    ##############初始化函数##############
    def init(self, myindex):
        # 初始化设置
        _index_mappings = {
            "mappings": {
                "user": {
                    "_all": {"enabled": False},
                    "properties": {
                        "subject_k": {"type": "keyword"
                                     # "include_in_all":True,


                                     }

                    }
                }

            }
        }

        self.es.indices.create(index=myindex, body=_index_mappings),  # 传入的是Index，函数内使用Index，还有调用时Index的格式应是怎样

    ##################插入函数##############
    def insert(self, myindex, mysubject):  ###变量为我们的插入.参数为q,a,id,注意此处的id
        doc = {
            "subject_k": mysubject

        }

        res = self.es.index(index=myindex, doc_type='user', body=doc)  # 插入数据

        return res

        # self.es.indices.refresh(index=myindex)

    def searchall(self,
                  myindex):  # 查询所有，返回的是return res['hits']['hits']，之后你可以用for hit in res['hits']['hits'] : print(hit['_source']['answer'])获得单项数据
        result = []
        res = self.es.search(index=myindex, doc_type='user', size=10000, body={"query": {"match_all": {}}})
        for hit in res['hits']['hits']:
            result.append(hit['_source']['subject_k'])
        # print(len(res['hits']['hits']))
        return result

###区别：mysql是每个用户的访问记录一张表，es的是所有查询记录一张表，mysql为用户挖掘服务（还有打星评分），es的两种新表是为kibana可视化服务；mysql用户结果的读取是在网页端去驱动；showquestion的函数在我这写