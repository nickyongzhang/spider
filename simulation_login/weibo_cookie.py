# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: 
Zhang Yong


"""
import requests
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

cookie = {'Cookie':'_T_WM=c298ace103906cee2a8b7aafaa476051; SUB=_2A254yzMRDeTxGedI6FUX8ibNyTuIHXVYNF1ZrDV6PUJbrdAKLUTxkW2I_sNILC39X-19V7x2sv3-C2RPWQ..; gsid_CTandWM=4umu31701VLS8Fj9MH4t86S1m23'}
url = 'http://weibo.cn/1637628127/profile?vt=4'

#content is bytes data
html = requests.get(url,cookies=cookie).content
##text is unicode data needed to be transformed to bytes data
# html = requests.get(url,cookies=cookie).text
# html = bytes(bytearray(html,encoding='utf-8'))

selector = etree.HTML(html)
content = selector.xpath('//span[@class="ctt"]')
for each in content:
	text = each.xpath('string(.)')
	b = 1
	print text