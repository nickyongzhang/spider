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




if __name__ == '__main__':
	url = 'http://weibo.cn/1637628127/profile?vt=4'
	html = requests.get(url).content
	print html
