# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: 
Zhang Yong

We directly use cookie to login in weibo.
In this sample we use mobile version of weibo because it is simple.

The cookie can be found in the web inspector after login. It is in the network menu.

"""

import urllib
import urllib2
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

cook = 'xxxxx'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'
headers = {
    'User-Agent': user_agent,
    'Cookie': cook
}

url = 'http://weibo.cn'
req = urllib2.Request(url, headers=headers)
try:
    response = urllib2.urlopen(req).read()
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason


selector = etree.HTML(response)

content = selector.xpath('//span[@class="ctt"]')
for each in content:
	text = each.xpath('string(.)')
	print text
