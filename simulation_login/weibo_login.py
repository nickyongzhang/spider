# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
__author__ = Zhang Yong

"""

from lxml import etree
from multiprocessing.dummy import Pool
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def spider_login(url):
	url_login = 'http://login.weibo.cn/login/'
	html = requests.get(url).content
	selector = etree.HTML(html)
	password = selector.xpath('//input[@type="password"]/@name')[0]
	vk = selector.xpath('//input[@name="vk"]/@value')[0]
	action = selector.xpath('//form[@method="post"]/@action')[0]
	new_url = url_login + action
	data = {
	'mobile':'13732226697',
	password:'901217zy',
	'remember':'on',
	'backURL': url,
	'backTitle':u'微博',
	'tryCount':'',
	'vk':vk,
	'submit':u'登录'
	}

	newhtml = requests.post(new_url,data=data).content
	new_selector = etree.HTML(newhtml)

	content = new_selector.xpath('//span[@class="ctt"]')
	for each in content:
		text = each.xpath('string(.)')
		print text


if __name__ == '__main__':
	pool = Pool(4)
	pages = []
	for i in range(1,11):
		url = 'http://weibo.cn/1637628127/profile?page=%d&vt=4'%(i)
		pages.append(url)

	results = pool.map(spider_login,pages)
	pool.close()
	pool.join()