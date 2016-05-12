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
string(.):get all strings under a tag

"""
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

'''重新运行之前请删除content.txt，因为文件操作使用追加方式，会导致内容太多。'''

def towrite(contentdict):
    f.writelines(u'回帖时间:' + str(contentdict['topic_reply_time']) + '\n')
    f.writelines(u'回帖内容:' + unicode(contentdict['topic_reply_content']) + '\n')
    f.writelines(u'回帖人:' + contentdict['user_name'] + '\n\n')

def spider(url):
    html = requests.get(url)
    selector = etree.HTML(html.text)
    content_field = selector.xpath('//div[@class="l_post l_post_bright  "]')
    item = {}
    # print content_field
    for each in content_field:
        reply_info = json.loads(each.xpath('@data-field')[0].replace('&quot',''))
        author = reply_info['author']['user_name']
        content = each.xpath('div[@class="d_post_content_main"]/div/cc/div')[0]
        content = content.xpath('string(.)')
        reply_time = reply_info['content']['date']
        print(content)
        print(reply_time)
        print(author)
        item['user_name'] = author
        item['topic_reply_content'] = content
        item['topic_reply_time'] = reply_time
        towrite(item)

if __name__ == '__main__':
    pool = ThreadPool(4)
    f = open('content.txt','a')
    page = []
    for i in range(1,21):
        newpage = 'http://tieba.baidu.com/p/3522395718?pn=' + str(i)
        page.append(newpage)

    # for url in page:
    #     spider(url)
    results = pool.map(spider, page)
    pool.close()
    pool.join()
    f.close()