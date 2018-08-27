#from .withweb import Withweb
import withweb

withweb = withweb.Withweb()
#myelas = elas.Elas()
# withweb.webinsert('qa_sys','机器学习的概念？','机器学习的概念？','机器学习真的是很厉害的工具。','www.bca.com','机器学习',2)
# withweb.webinsert('qa_sys','机器学习有什么价值？','机器学习有什么价值？','价值很高','www.bca.com','机器学习',3)
# withweb.webinsert('qa_sys','华为云服务器能做什么？','华为云服务器能做什么？','华为云服务器能完成很多的功能','www.bcca.com','云服务器',4)
# withweb.webinsert('qa_sys','华为云服务器有什么方便的地方？','华为云服务器有什么方便的地方？','他的便利之处很多，有很多好用的功能','www.bcda.com','云服务器',5)
# withweb.webinsert('qa_sys','机器学习有什么不方便的地方？','机器学习有什么不方便的地方？','有很多不方便的地方','www.bcda.com','机器学习',6)
# withweb.webinsert('qa_sys','你爱机器学习嘛？','你爱机器学习嘛？','当然啦，肯定喜欢','www.abcda.com','机器学习',7)

#withweb.webinit('qa_sys')
#print('aaa')
print(withweb.accurate_search('qa_sys','机器学习的概念？'))
