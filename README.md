# spider

## Overview

This is my learning notes when studying spidering website content. Thanks to [Jikexueyuan](http://www.jikexueyuan.com/path/python/). It is a very good website for programming language learning.

This serie contains both basic and advanced knowledge of spider technology.

## Basics


This section provides basic knowledge for webpage crawler.  There are several methods to login in a website and get the content from a website, like **POST**, **GET**, **Headers**, and **Proxy**. 

### POST
First we need to import some packages

```python

import urllib
import urllib2 
```	

Most websites are dynamic pages needing input information when we visit them. We use **Retuest** before getting response of the website. **Request** gets parameters, like url, data, and others. Url is the address, and data is the information for visiting the website. However, the parameters will not be shown in the link.

```python
	values = {"username":"1016903103@qq.com","password":"XXXX"}  

	data = urllib.urlencode(values)  

	url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"  

	request = urllib2.Request(url,data)
  
	response = urllib2.urlopen(request)
  
	print response.read()
```

The website [CSDN](https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn) is Chinese blog website for writing technology, especially programming staff.

### GET
The url should contain all the parameters when using **GET**. The account and password information we submit will be shown. This is not very safe.

```python
	# The dictionary method is the same as the above code
	values={}
	values['username'] = "1016903103@qq.com"
	values['password']="XXXX"
 
	data = urllib.urlencode(values) 
	url = "http://passport.csdn.net/account/login"
 
	geturl = url + "?"+data
 
	request = urllib2.Request(geturl)
	response = urllib2.urlopen(request)
	print response.read()
```

### Headers
Sometimes the website will refuse the visit from application (python in our case). Then we need use **Headers** to cheat the website that we are visiting through explorer. Opening the web inspecter, we can find the headers containing a lot of information, in which the *user-agent* stands for the identity of visit. We will construct a headers and pass it to **Requst**. Then the server will identify the visiting request is from explorer. There is one more thing called *referer* in the headers which is used to prevent hotlink. Some servers will refuse to respond if finding that the referer is not itself. We can also define the *referer* in the headers just like *user-agent*.

	url = 'http://www.zhihu.com/login'
	
	# the agent below is from using chrome
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  
	
	values = {'username' : 'cqc',  'password' : 'XXXX' }
	  
	headers = { 'User-Agent' : user_agent, 'Referer':'http://www.zhihu.com/articles' } 
	
	data = urllib.urlencode(values)  
	
	request = urllib2.Request(url, data, headers)
	  
	response = urllib2.urlopen(request)  
	
	page = response.read()
	
### Proxy
Some websites will refuse to respond if one IP visits too often in a short time. Then we can use proxy to change IP from time to time. Actually, urllib2 itself will use a enviroment variable http_proxy to set a HTTP Proxy.

	enable_proxy = True

	proxy_handler = urllib2.ProxyHandler({"http" : 'http://some-proxy.com:8080'})
	null_proxy_handler = urllib2.ProxyHandler({})
	
	if enable_proxy:
		opener = urllib2.build_opener(proxy_handler)
	else:
		opener = urllib2.build_opener(null_proxy_handler)
		
	urllib2.install_opener(opener)		
	
### Timeout
`urlopen` can take another parameter called timeout. It will set the waiting time in case some websites are very slow.

	response = urllib2.urlopen('http://www.baidu.com', timeout=10)
	
### URLError
We may come across with error when opening a web page. We can use `try...except...` to detect the reason.

	request = urllib2.Request('http://www.xxx.com')
	try:
		urllib2.urlopen(request)
	except urllib2.URLError, e:
		raise e.reason
	
### HTTPError: 
A subclass of URLError,it will generate a code if error happens

	req = urllib2.Request('http://blog.csdn.net/cqcre')
	try:
    	urllib2.urlopen(req)
	except urllib2.URLError, e:
    	if hasattr(e,"code"):
        	print e.code
    	if hasattr(e,"reason"):
        	print e.reason
	else:
    	print "OK"	

### Cookie
**Cookie** is identification information, e.g. login information.  
**Opener**: a opener is need to get a website. `urlopener` is a special opener but it can open take three parameters, i.e., url, data, and timeout. We can build more general opener.  
**Cookielib**: provides classes to store cookies. It contains CookieJar, FileCookieJar, MozillaCookieJar, LWPCookieJar

#### 1. Save Cookie to a parameter

	import cookielib
	
	#声明一个CookieJar对象实例来保存cookie
	cookie = cookielib.CookieJar()
	
	#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
	handler=urllib2.HTTPCookieProcessor(cookie)
	
	#通过handler来构建opener
	opener = urllib2.build_opener(handler)
	
	#此处的open方法同urllib2的urlopen方法，也可以传入request
	response = opener.open('http://www.baidu.com')
	for item in cookie:
    	print 'Name = '+item.name
    	print 'Value = '+item.value
	
#### 2. Save Cookie to a file

	#设置保存cookie的文件，同级目录下的cookie.txt
	filename = 'cookie.txt'
	
	#声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
	cookie = cookielib.MozillaCookieJar(filename)
	
	#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
	handler = urllib2.HTTPCookieProcessor(cookie)
	
	#通过handler来构建opener
	opener = urllib2.build_opener(handler)
	
	#创建一个请求，原理同urllib2的urlopen
	response = opener.open("http://www.baidu.com")
	
	#保存cookie到文件
	cookie.save(ignore_discard=True, ignore_expires=True)
	
>`ignore_discard`: save even cookies set to be discarded.
`ignore_expires`: save even cookies that have expired.  

The file is overwritten if it already exists.
	
#### 3. Get Cookie from a file

	#创建MozillaCookieJar实例对象
	cookie = cookielib.MozillaCookieJar()
	
	#从文件中读取cookie内容到变量
	cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
	
	#创建请求的request
	req = urllib2.Request("http://www.baidu.com")
	
	#利用urllib2的build_opener方法创建一个opener
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	response = opener.open(req)
	print response.read()	

#### 4. An example
Below is an example of logging in a website

	import urllib
	import urllib2
	import cookielib

	filename = 'cookie.txt'
	#声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
	cookie = cookielib.MozillaCookieJar(filename)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	postdata = urllib.urlencode({
			'stuid':'201200131012',
			'pwd':'23342321'
		})
	#登录教务系统的URL
	loginUrl = 'http://jwxt.sdu.edu.cn:7890/pls/wwwbks/bks_login2.login'
	#模拟登录，并把cookie保存到变量
	result = opener.open(loginUrl,postdata)
	#保存cookie到cookie.txt中
	cookie.save(ignore_discard=True, ignore_expires=True)
	#利用cookie请求访问另一个网址，此网址是成绩查询网址
	gradeUrl = 'http://jwxt.sdu.edu.cn:7890/pls/wwwbks/bkscjcx.curscopre'
	#请求访问成绩查询网址
	result = opener.open(gradeUrl)
	print result.read()
The code can also be found in the file `CookieLogin.py`	
****

### Regular Expressions
	
	import re
	
```	
Identifiers:

\d any number
\D anything but a number
\s space
\S anything but a space
\w any character
\W anything but a character
. any character, except for a newline
\b the white space around words
\. a period

Modifiers: 
{1, 3} we're expecting 1-3 
+ Match 1 or more
? Mathch 0 or 1
* Mathch 0 or more
$ Mathch the end of a string
^ Mathch the beginning of a string
| either or
[] range of "variance" [A-Za-q1-5]
{x} expecting "x" amount

white Space characters:
\n newline
\s space
\t tab
\e escape
\f form feed
\r return

DONT FORGET:
. + * ? [ ] $ ^ ( ) { } | \

```

#### 1. re.compile(string[,flag])
Before we match a pattern, we need to get the pattern. This is what `compile` does.
  
Below are all the match methods. We will introduce one by one.

```python

re.match(pattern, string[, flags])  
re.search(pattern, string[, flags])  
re.split(pattern, string[, maxsplit])  
re.findall(pattern, string[, flags])
re.finditer(pattern, string[, flags])
re.sub(pattern, repl, string[, count])
re.subn(pattern, repl, string[, count])
```

flags is match pattern. We can use '|' to include several pattern case, e.g.`re.I|re.M`


```markdown

* re.I(IGNORECASE): case-insensitive（in bracket is the full spelling;
* re.M(MULTILINE): multiple line mode. This will change the behaviour of `^` and `$`;
* re.S(DOTALL): dot arbitrarily match pattern. This will change the effect of `.`;
* re.L(LOCALE): \w \W \b \B \s \S will be determined by current area setting;
* re.U(UNICODE): \w \W \b \B \s \S \d \D are determined by the character attributes of unicode;
* re.X(VERBOSE): detail mode. Regular expressions can be multiple lines ignoring spaces and can including comments under this mode.	
```
