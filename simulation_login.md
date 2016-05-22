<link rel="stylesheet" href="/Users/zhangyong/highlight/styles/default.css">
<script src="/Users/zhangyong/highlight/highlight.pack.js"></script>
<script>hljs.initHighlightingOnLoad();</script>


# Simulation_login

Simulation_login is a technique that a program simulates logging into a website that needs verifying identification. In this section, two methods are introduced:

### [Cookie login](http://github.com/nickzylove/spider/blob/master/basic.md#cookie-login)
### [Direct Crawling](http://github.com/nickzylove/spider/blob/master/basic.md#direct-crawling)
***
## Cookie login

> An HTTP cookie (also called web cookie, Internet cookie, browser cookie or simply cookie) is a small piece of data sent from a website and stored in the user's web browser while the user is browsing. Every time the user loads the website, the browser sends the cookie back to the server to notify the user's previous activity. Cookies were designed to be a reliable mechanism for websites to remember stateful information (such as items added in the shopping cart in an online store) or to record the user's browsing activity (including clicking particular buttons, logging in, or recording which pages were visited in the past). Cookies can also store passwords and form content a user has previously entered, such as a credit card number or an address.  
> ---Wiki

From the definition of cookie. We can see that it's a useful mechanism that can save us a lot of trouble. We don't have to type in identification information everytime we login a website because it's all done by the browser. If the program or application can have the cookie, it can also easily simulate login. However, we must be careful because the cookie is very personal and putting it public can be insecure. No bullshit, let's  directly have a look at the code.

First we need to import the necessary packages.

	import urllib
	import urllib2
	from lxml import etree
	import sys

As we are trying to login a chinese website. We also add two lines to avoid encoding error.

	reload(sys)
	sys.setdefaultencoding('utf-8')

The website we want to login is a social network website, like twitter of China. We choose the mobile version website because it's much simpler. We have introduced how to get the html content of a website in previous sections.

	url = 'http://weibo.cn'
	req = urllib2.Request(url)
	try:
    	response = urllib2.urlopen(req).read()
	except urllib2.URLError, e:
    	if hasattr(e,"code"):
        	print e.code
    	if hasattr(e,"reason"):
        	print e.reason
     
    print response

Sometimes the website may refuse a program visiting and return back a error code. In our case, we will also get a HTTPError 403. Therefore, we need to simulate visiting through an explorer. `headers` can help.

	user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'
	headers = {
    	'User-Agent': user_agent
    	}
    	
    req = urllib2.Request(url, headers=headers)
    
Finally we get some useful staff. We don't post the html page content here because it takes too much space. Readers can try yourselves and you can find that it is actually a login page. This is where the identification information is needed. 

In this case, we want to directly use cookie to login in weibo. We can find the cookie in the web inspector after login. We have to login once and then no troubles any longer. The following picture depicts how to find the cookie in the Chrome.

![cookie](https://raw.githubusercontent.com/nickzylove/spider/master/simulation_login/cookie.png)

After getting the cookie, we can put it in the headers dictionary. Okay, everything is done. Let's have a look at the entire code.

	import urllib
	import urllib2
	from lxml import etree
	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')

	cook = 'xxx'  #type in your own cookie
	user_agent = 'xxx' type in your own user-agent
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

We use `xpath` to find the content we need in the code. It is much easier than using regular expressions. The introduction of `xpath` can be found in [xpath.md](https://github.com/nickzylove/spider/blob/master/xpath.md).


## Direct Crawling
Using cookie is very simple method to login a website. We encourage using it as long as the cookie information is not lost. However, if you just don't want to use explicit cookie, this section give you another choice.

We can post all the identification information directly to login. Here is how we do.

We want to login in someone's weibo (we already know his/her account and password). 

	url = 'http://weibo.cn/xxxxx' #change to weibo site of the person
	url_login = 'https://login.weibo.cn/login/'	

	html = requests.get(url).content
	print html
	
We use `requests` package instead of `urllib` and `urllib2` because it is often much simpler. Reader can use `pip install requests` to get the package. `.content()` get the html source code, it is in binary format. Users can also use `.text()` but it's in unicode format and must be transformed to binary format. Of course, you can use `urllib` and `urllib2` if you like. It's also very easy.

Let's have a look at the souce code we obtain.

![html](https://raw.githubusercontent.com/nickzylove/spider/master/simulation_login/html.png)

There are a lot of `<input>` fields. These are the identification inforamtion the browser needs to know to login a website. Then we just tell it what it wants.

	selector = etree.HTML(html)
	# the password field may have special name. We should retrieve its name
	password = selector.xpath('//input[@type="password"]/@name')[0]
	vk = selector.xpath('//input[@name="vk"]/@value')[0]
	capId = selector.xpath('//input[@name="capId"]/@value')[0]
	imgUrl = getImg(html)
	buffer = requests.get(imgUrl).content
	# buffer=urllib2.urlopen(imgUrl).read()
	im=Image.open(StringIO.StringIO(buffer))
	im.show()
	captcha_solution= raw_input("Captcha is:")
	data = {
	'mobile':'XXXX', #type in your account
	password:'xxxx',  #type in your password
	'remember':'on',
	'backURL': url,
	'backTitle':u'手机新浪网',
	'tryCount':'',
	'vk':vk,
	'capId': capId,
	'code': captcha_solution,
	'submit':u'登录'
	}
	
Using the above code, we retrive all the information the browser needs to know. The name of password field may not be `"password"` in this website, so we have to retrieve its name. 

The other important issue is that the website needs a captcha. We directly retrieve the captcha image and show to users. Next, users can input the code by themselves. We believe this is a better solution because letting the computer itself to identify the code is what we concern in this blog.

Reading the html source code we can also find a field `<form>` with an attribute `action`. This action is used to redirect to the new link.

	action = selector.xpath('//form[@method="post"]/@action')[0]
	new_url = url_login + action
	
Next, we can login the website with the data we have obtained.

	newhtml = requests.post(new_url,data=data).content
	new_selector = etree.HTML(newhtml)

	content = new_selector.xpath('//span[@class="ctt"]')
	for each in content:
		text = each.xpath('string(.)')
		print text
		
Time to wrap the entire code.

	import re
	import StringIO
	from PIL import Image
	from lxml import etree
	import requests
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
		url = 'http://weibo.cn/xxx' ##change to weibo site of the person			
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
		im = Image.open(StringIO.StringIO(buffer))
		im.show()
		captcha_solution= raw_input("Captcha is:")
		new_url = url_login + action
		data = {
		'mobile':'XXXX', #type in your account
		password:'xxxx',  #type in your password
		'remember':'on',
		'backURL': url,
		'backTitle':u'手机新浪网',
		'tryCount':'',
		'vk':vk,
		'capId': capId,
		'code': captcha_solution,
		'submit':u'登录'
		}

		newhtml = 	requests.post(new_url,data=data).content
		new_selector = etree.HTML(newhtml)

		content = new_selector.xpath('//span[@class="ctt"]')
		for each in content:
			text = each.xpath('string(.)')
			print text
			
A function `def getImg(page)` aimed to retieve the captcha image link is included. And we also import the necessary packages `StringIO` and `Image`.

**P.S.**: All the content above are put in several python scripts in the simulation_login folder.
******************************
We also give a practical example in this blog so that we can see the magic of simulation login. This example is used to send emails reminding the timeline update of the author's weibo.
If you just want to get the update of one person's weibo, you don't have to login actually. That would be very easy job.

No bullshit! See the code.

	class targetweibo(object):
		"""
		a class to spider certain person's weibo
		"""
		#initialization
		def __init__(self):
			self.url = 'http://weibo.cn/xxx' #type in the website address
			self.url_login = 'http://login.weibo.cn/login/'
			self.new_url = self.url_login
			self.user_agent = 'xxx' #type in your user-agent
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
			'mobile':'13732226697',
			password:'901217zy',
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
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

			post_data=urllib.urlencode(data)

			newreq=urllib2.Request(self.url, headers=self.headers)
			newhtml = urllib2.urlopen(newreq,timeout=5).read()
			selector = etree.HTML(newhtml)
			action = selector.xpath('//form[@method="post"]/@action')[0]
			self.jump_url = self.url_login + action

			jumpreq=urllib2.Request(self.jump_url, post_data, self.headers)

			jumphtml = opener.open(jumpreq).read()
			cookie.save(ignore_discard=True, ignore_expires=True)
			return jumphtml

		def getContent(self,html):
			selector = etree.HTML(html)
			link = 'http://weibo.cn'+selector.xpath('//a[@class="nl"]/@href')[4]
			print link
			cookie = cookielib.MozillaCookieJar()
			cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)

			finalreq = urllib2.Request(link,headers=self.headers)
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
			finalhtml=opener.open(finalreq).read()
			final_selector = etree.HTML(finalhtml)
			content = final_selector.xpath('//span[@class="ctt"]')[0]
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

Let's dip into the new class. The login function is achived by `__init__(self)`, `getSource(self`), `getImg(self,page)`, and `getData(self,html)`. They have been explained in detail. 

We add a function `getCookie(self, data)` to save the cookie of the website after login. So we don't have to call the `getData(self,html)` function everytime we want to login. This is useful because the captcha code is changing everytime. We have to type in the code every time if we don't use cookie.

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
		jumphtml = opener.open(jumpreq).read()
		cookie.save(ignore_discard=True, ignore_expires=True)
		return jumphtml
		
A cookieJar is used to help save the cookie. This has been introduced in the basic section. Readers can refer [basic.md](https://github.com/nickzylove/spider/blob/master/basic.md) to know more. 

Next, we can use the cookie to login the website every time we want to get the updates of weibos.

	def getContent(self,html):
		selector = etree.HTML(html)
		link = 'http://weibo.cn'+selector.xpath('//a[@class="nl"]/@href')[4]
		cookie = cookielib.MozillaCookieJar()
		cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)

		finalreq = urllib2.Request(link,headers=self.headers)
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		finalhtml = opener.open(finalreq).read()
		final_selector = etree.HTML(finalhtml)
		#get the first weibo
		content = final_selector.xpath('//span[@class="ctt"]')[0]
		#mail function may fail if link is start with http://
		newcontent = unicode(content.xpath('string(.)')).replace('http://','')
		sendtime = final_selector.xpath('//span[@class="ct"]/text()')[0]
		sendtext = newcontent + sendtime
		return sendtext

The retrieved weibo texts can be saved.

	def tosave(self,text):
		f = open('weibo.txt','a')
		f.write(text+'\n')
		f.close()

It should be better to check whether the weibo content has already existed in the .txt file. We don't want to redundant information.

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
				
After getting the contents we can also send them via email. 

	class mailhelper(object):
		"""
		send an email
		"""
		def __init__(self):

			self.mail_host="smtp.gmail.com"  #server
			self.mail_user="xxxx"    #user name
			self.mail_pass="xxxx"   #email psw
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

We can complete our task with the two new classes now.

	if __name__ == '__main__':
		mailto_list=['xxxx@xx.com'] #mail to list
		helper = targetweibo()
		source = helper.getSource()
		data = helper.getData(source)
		html= helper.getCookie(data)	
		while True:
			content = helper.getContent(html)
			if helper.tocheck(content):
				if mailhelper().send_mail(mailto_list,
				u"target updates his weibo", content):
					print u"successfully sent"

				else:
					print u"sending failed"
				helper.tosave(content)
				print content
			else:
				print u'pass'
			time.sleep(30)

The content retriving and email sending process are repeated every 30 seconds. We only have to get the identification information once and do not have to type in captcha code. The entire code of this practical example can be found in the **simulation_login/weibo_spider.py** script.













