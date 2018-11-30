# -*- coding: utf-8 -*-
# @Time    : 2018/8/27 10:24
# @Author  : wb
# @File    : baiduDnn.py

# 百度api提供的语言模型服务

from aip import AipNlp

""" 你的 APPID AK SK """
APP_ID = '11731139'
API_KEY = '7sUyLlu1wYdBy9rozkIZVN1u'
SECRET_KEY = '6tM1yqYphPN4XAshGFDiyqRD1lrFQarf'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

text = "云解析服务中查询内网Zone的名称服务器的功能介绍是什么？"

""" 
调用DNN语言模型 
log_id	uint64	请求唯一标识码
word	string	句子的切词结果
prob	float	该词在句子中的概率值,取值范围[0,1]
ppl	float	描述句子通顺的值：数值越低，句子越通顺
"""

result = client.dnnlm(text)

print(result)

title = "云容器引擎的产品优势"

content = "CCE基于业界主流的Docker和Kubernetes开源技术，并进行了大量的商用增强，在系统可靠性、高性能、开源社区的兼容性等多个方面具有独特的优势。"

""" 调用文章标签 """
result1 = client.keyword(title, content)
print(result1)
