# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
__author__ = Zhang Yong

This example simulates logging in weibo with username and password

"""
import re
import StringIO
from PIL import Image
from lxml import etree
from multiprocessing.dummy import Pool
import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getImg(page):
    pattern = re.compile('<img src="(.*?)" alt',re.S)
    result = re.search(pattern,page)
    if result:
        return result.group(1)
    else:
        return None

if __name__ == '__main__':
	url = 'http://weibo.cn/1637628127' #此处请修改为微博地址
	url_login = 'https://login.weibo.cn/login/'

	html = requests.get(url).content
	selector = etree.HTML(html)
	# the password field may have special name. We should retrive its name
	password = selector.xpath('//input[@type="password"]/@name')[0]
	vk = selector.xpath('//input[@name="vk"]/@value')[0]
	capId = selector.xpath('//input[@name="capId"]/@value')[0]
	action = selector.xpath('//form[@method="post"]/@action')[0]
	imgUrl = getImg(html)
	buffer = requests.get(imgUrl).content
	# buffer=urllib2.urlopen(imgUrl).read()
	im=Image.open(StringIO.StringIO(buffer))
	im.show()
	captcha_solution= raw_input("Captcha is:")
	new_url = url_login + action
	data = {
	'mobile':'13732226697',
	password:'901217zy',
	'remember':'on',
	'backURL': url,
	'backTitle':u'手机新浪网',
	'tryCount':'',
	'vk':vk,
	'capId': capId,
	'code': captcha_solution,
	'submit':u'登录'
	}

	newhtml = requests.post(new_url,data=data).content
	new_selector = etree.HTML(newhtml)

	content = new_selector.xpath('//span[@class="ctt"]')
	for each in content:
		text = each.xpath('string(.)')
		print text

