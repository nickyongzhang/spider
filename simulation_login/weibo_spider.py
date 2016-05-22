# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
__author__ = Zhang Yong

send emails reminding the timeline update of the author's weibo.

If you just want to get the update of one person's weibo, you don't have 
to login actually. That would be very easy job.

"""

import urllib
import urllib2
import cookielib
import smtplib
from email.mime.text import MIMEText
import requests
from lxml import etree
import os
import re
import StringIO
from PIL import Image
from bs4 import BeautifulSoup
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class mailhelper(object):
	"""
	send an email
	"""
	def __init__(self):

		self.mail_host="smtp.gmail.com"  #server
		self.mail_user="nickzylove"    #user name
		self.mail_pass="xxxx"   #psw
		self.mail_postfix="gmail.com"  #postfix of send box
		
	def send_mail(self,to_list,sub,content):
		me = 'targetweibo'+'<'+self.mail_user+'@'+self.mail_postfix+'>'
		msg = MIMEText(content,_subtype='plain',_charset='utf-8')
		msg['Subject'] = sub
		msg['From'] = me
		msg['To'] = ';'.join(to_list)
		try:
			server = smtplib.SMTP()
			server.connect(self.mail_host)
			server.starttls()
			server.login(self.mail_user,self.mail_pass)
			server.sendmail(me,to_list,msg.as_string())
			server.close()
			return True
		except Exception, e:
			print str(e)
			return False


class targetweibo(object):
	"""
	a class to spider certain person's weibo
	"""
	def __init__(self):
		self.url = 'http://weibo.cn/1637628127'
		self.url_login = 'http://login.weibo.cn/login/'
		self.new_url = self.url_login
		self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'
		self.headers = {
		    'User-Agent': self.user_agent
		}

	def getSource(self):
		html = requests.get(self.url).content
		return html

	def getImg(self, page):
		pattern = re.compile('<img src="(.*?)" alt',re.S)
		result = re.search(pattern,page)
		if result:
			return result.group(1)
		else:
			return None

	def getData(self,html):
		selector = etree.HTML(html)
		password = selector.xpath('//input[@type="password"]/@name')[0]
		vk = selector.xpath('//input[@name="vk"]/@value')[0]
		capId = selector.xpath('//input[@name="capId"]/@value')[0]
		action = selector.xpath('//form[@method="post"]/@action')[0]
		imgUrl = self.getImg(html)
		buffer = requests.get(imgUrl).content
		im=Image.open(StringIO.StringIO(buffer))
		im.show()
		captcha_solution= raw_input("Captcha is:")
		self.new_url = self.url_login + action
		data = {
		'mobile':'xxxx',
		password:'xxxx',
		'remember':'on',
		'backURL': self.url,
		'backTitle':u'手机新浪网',
		'tryCount':'',
		'vk':vk,
		'capId': capId,
		'code': captcha_solution,
		'submit':u'登录'
		}
		return data 

	def getCookie(self, data):
		filename = 'cookie.txt'
		cookie=cookielib.MozillaCookieJar(filename)
		opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		# urllib2.install_opener(opener)

		post_data=urllib.urlencode(data)

		newreq=urllib2.Request(self.url, headers=self.headers)
		newhtml=urllib2.urlopen(newreq,timeout=5).read()
		selector = etree.HTML(newhtml)
		action = selector.xpath('//form[@method="post"]/@action')[0]
		self.jump_url = self.url_login + action

		jumpreq=urllib2.Request(self.jump_url, post_data, self.headers)
		# jumphtml=urllib2.urlopen(jumpreq,timeout=1).read()
		jumphtml = opener.open(jumpreq).read()
		cookie.save(ignore_discard=True, ignore_expires=True)
		return jumphtml

	def getContent(self,html):
		selector = etree.HTML(html)
		link = 'http://weibo.cn'+selector.xpath('//a[@class="nl"]/@href')[4]
		cookie = cookielib.MozillaCookieJar()
		cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)

		finalreq=urllib2.Request(link,headers=self.headers)
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		# finalhtml = urllib2.urlopen(finalreq).read()
		finalhtml=opener.open(finalreq).read()
		final_selector = etree.HTML(finalhtml)
		content = final_selector.xpath('//span[@class="ctt"]')[0]
		#first weibo is started from third span
		#mail function may fail if link is start with http://
		newcontent = unicode(content.xpath('string(.)')).replace('http://','')
		sendtime = final_selector.xpath('//span[@class="ct"]/text()')[0]
		sendtext = newcontent + sendtime
		return sendtext

	def tosave(self,text):
		f = open('weibo.txt','a')
		f.write(text+'\n')
		f.close()

	def tocheck(self,data):
		if not os.path.exists('weibo.txt'):
			return True
		else:
			f = open('weibo.txt','r')
			existweibo = f.readlines()
			if data + '\n' in existweibo:
				return False
			else:
				return True


if __name__ == '__main__':
	mailto_list=['xxx@xxx.com']
	helper = targetweibo()
	source = helper.getSource()
	data = helper.getData(source)
	html= helper.getCookie(data)	
	while True:
		content = helper.getContent(html)
		if helper.tocheck(content):
			if mailhelper().send_mail(mailto_list,u"zy updates his weibo", content):
				print u"successfully sent"

			else:
				print u"sending failed"
			helper.tosave(content)
			print content
		else:
			print u'pass'
		time.sleep(30)




