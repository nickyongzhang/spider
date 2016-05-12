# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
__author__ = Zhang Yong

send emails reminding the update of weibo of certain person

"""

import smtplib
from email.mime.text import MIMEText
import requests
from lxml import etree
import os
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class mailhelper(object):
	"""
	send an email
	"""
	def __init__(self):

		self.mail_host="smtp.gmail.com"  #设置服务器
		self.mail_user="nickzylove"    #用户名
		self.mail_pass="901217zy"   #密码
		self.mail_postfix="gmail.com"  #发件箱的后缀
		
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
	爬取特定人的微博
	"""
	def __init__(self):
		self.url = 'http://weibo.cn/1637628127/profile?vt=4'
		self.url_login = 'http://login.weibo.cn/login/'
		self.new_url = self.url_login

	def getSource(self):
		html = requests.get(self.url).content
		return html

	def getData(self,html):
		selector = etree.HTML(html)
		password = selector.xpath('//input[@type="password"]/@name')[0]
		vk = selector.xpath('//input[@name="vk"]/@value')[0]
		action = selector.xpath('//form[@method="post"]/@action')[0]
		self.new_url = self.url_login + action
		data = {
		'mobile':'13732226697',
		password:'901217zy',
		'remember':'on',
		'backURL': self.url,
		'backTitle':u'微博',
		'tryCount':'',
		'vk':vk,
		'submit':u'登录'
		}
		return data 

	def getContent(self,data):
		newhtml = requests.post(self.new_url,data=data).content
		new_selector = etree.HTML(newhtml)
		content = new_selector.xpath('//span[@class="ctt"]')[0]
		#first weibo is started from third span
		#mail function may fail if link is start with http://
		newcontent = unicode(content.xpath('string(.)')).replace('http://','')
		sendtime = new_selector.xpath('//span[@class="ct"]/text()')[0]
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
	mailto_list=['960752103@qq.com']
	helper = targetweibo()
	while True:
		source = helper.getSource()
		data = helper.getData(source)
		content = helper.getContent(data)
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




