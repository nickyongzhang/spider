#-*-coding:utf8-*-
"""
json parsing
"""

import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'}

jscontent = requests.get('http://coral.qq.com/article/1165021596/comment?commentid=0&reqnum=50', headers=head).content
jsDict = json.loads(jscontent)
jsData = jsDict['data']
comments = jsData['commentid']
for each in comments:
    print each['content']