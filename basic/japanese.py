# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: 
Zhang Yong

A basic webpage crawler code

In this code we use requests instead of urllib2, it's much easier than urllib2

"""
import requests
import re
import sys
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('gb18030')
type = sys.getfilesystemencoding()

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'
header = {'User-Agent':user_agent}
html = requests.get('http://jp.tingroom.com/yuedu/yd300p/')
html.encoding = 'utf-8'
htmltext = html.text.encode('utf-8')

title = re.findall('color:#666666;">(.*?)</span>',htmltext, re.S)
for each in title:
	print each

chinese = re.findall('color: #039;">(.*?)</a>',htmltext,re.S)
for each in chinese:
	print each





















