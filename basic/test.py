# !/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

url = 'http://tieba.baidu.com/p/3522395718?pn='
html = requests.get(url)
selector = etree.HTML(html.text)
content_field = selector.xpath('//div[@class="l_post l_post_bright  "]')
print content_field[0].xpath('/text()')






