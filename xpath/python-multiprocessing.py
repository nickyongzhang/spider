# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: 
Zhang Yong

XPath与多线程爬虫
//定位根节点
/往下层寻找
提取文本内容：/text()
提取属性内容：/@xxxx
starts-with(@属性名称,属性字符相同的部分)
string(.)

"""
from multiprocessing.dummy import Pool as ThreadPool
import requests
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getsource(url):
    html = requests.get(url)
    print html

urls = []

for i in range(1,21):
    newpage = 'http://tieba.baidu.com/p/3522395718?pn=' + str(i)
    urls.append(newpage)

# time1 = time.time()
# for i in urls:
#     print i
#     getsource(i)
# time2 = time.time()
# print u'单线程耗时：' + str(time2-time1)

pool = ThreadPool(8)
time3 = time.time()
results = pool.map(getsource, urls)
pool.close()
pool.join()
time4 = time.time()
print u'并行耗时：' + str(time4-time3)

