<link rel="stylesheet" href="/Users/zhangyong/highlight/styles/default.css">
<script src="/Users/zhangyong/highlight/highlight.pack.js"></script>
<script>hljs.initHighlightingOnLoad();</script>


# spider

## Overview

This is my learning notes when studying spidering website content. Thanks to [Jikexueyuan](http://www.jikexueyuan.com/path/python/). It is a very good website for programming language learning.

This serie contains both basic and advanced knowledge of spider technology.

## Basics


This section provides basic knowledge for webpage crawler.  There are several methods to login in a website and get the content from a website, like **POST**, **GET**, **Headers**, and **Proxy**. 

### POST
First we need to import some packages


	import urllib
	import urllib2 
	

Most websites are dynamic pages needing input information when we visit them. We use **Retuest** before getting response of the website. **Request** gets parameters, like url, data, and others. Url is the address, and data is the information for visiting the website. However, the parameters will not be shown in the link.

	values=
	{"username":"1016903103@qq.com","password":"XXXX"}  

	data = urllib.urlencode(values)  

	url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"  

	request = urllib2.Request(url,data)
  
	response = urllib2.urlopen(request)
  
	print response.read()
	
The website [CSDN](https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn) is Chinese blog website for writing technology, especially programming staff.

### GET
The url should contain all the parameters when using **GET**. The account and password information we submit will be shown. This is not very safe.

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
*********************************************************

## Regular Expressions
	
	import re
	
```	
*** Identifiers:
\d any number
\D anything but a number
\s space
\S anything but a space
\w any character
\W anything but a character
. any character, except for a newline
\b the white space around words
\. a period
*** Modifiers: 
{1, 3} we're expecting 1-3 
+ Match 1 or more
? Mathch 0 or 1
* Mathch 0 or more
$ Mathch the end of a string
^ Mathch the beginning of a string
| either or
[] range of "variance" [A-Za-q1-5]
{x} expecting "x" amount
*** white Space characters:
\n newline
\s space
\t tab
\e escape
\f form feed
\r return
DONT FORGET:
. + * ? [ ] $ ^ ( ) { } | \
```

### 1. re.compile(string[,flag])
Before we match a pattern, we need to get the pattern. This is what `compile` does.
  
Below are all the match methods. We will introduce one by one.

	re.match(pattern, string[, flags])  
	re.search(pattern, string[, flags])  
	re.split(pattern, string[, maxsplit])  
	re.findall(pattern, string[, flags])
	re.finditer(pattern, string[, flags])
	re.sub(pattern, repl, string[, count])
	re.subn(pattern, repl, string[, count])

flags is match pattern. We can use '|' to include several pattern case, e.g.`re.I|re.M`

	* re.I(IGNORECASE): case-insensitive（in bracket is the full spelling;
	* re.M(MULTILINE): multiple line mode. This will change the behaviour of `^` and `$`;
	* re.S(DOTALL): dot arbitrarily match pattern. This will change the effect of `.`;
	* re.L(LOCALE): \w \W \b \B \s \S will be determined by current area setting;
	* re.U(UNICODE): \w \W \b \B \s \S \d \D are determined by the character attributes of unicode;
	* re.X(VERBOSE): detail mode. Regular expressions can be multiple lines ignoring spaces and can including comments under this mode.	

### 2. re.match
We need to compile the regExp into a pattern first. The 'r' in front of 'hello' stands for raw string.

	pattern = re.compile(r'hello')
 
Then we can use `re.match` to match texts. If no matches return, None will be returned.

	result1 = re.match(pattern,'hello')
	result2 = re.match(pattern,'helloo world!')
	result3 = re.match(pattern,'helo world!')
	result4 = re.match(pattern,'hello world!')
 
If the first match is successful,

	if result1:
    # get the match result using group()
    	print result1.group()
	else:
    	print '1st match fail！'
 
If the second is successful,

	if result2:
    	print result2.group()
	else:
    	print '2nd match fail！'
    	
Similarly for the third,

	if result3:
    	print result3.group()
	else:
    	print '3rd match fail！'

and the fourth,
 
	if result4:
    	print result4.group()
	else:
    	print '4th match fail！'
    	
There is a `result.groupt()`. What is it? `re.match()` contain a lot of attributes and methods, like the following:

```
Attributes
1.string: 匹配时使用的文本。
2.re: 匹配时使用的Pattern对象。
3.pos: 文本中正则表达式开始搜索的索引。值与Pattern.match()和Pattern.search()方法的同名参数相同。
4.endpos: 文本中正则表达式结束搜索的索引。值与Pattern.match()和Pattern.search()方法的同名参数相同。
5.lastindex: 最后一个被捕获的分组在文本中的索引。如果没有被捕获的分组，将为None。
6.lastgroup: 最后一个被捕获的分组的别名。如果这个分组没有别名或者没有被捕获的分组，将为None。
Methods:
1.group([group1, …]):
获得一个或多个分组截获的字符串；指定多个参数时将以元组形式返回。group1可以使用编号也可以使用别名；编号0代表整个匹配的子串；不填写参数时，返回group(0)；没有截获字符串的组返回None；截获了多次的组返回最后一次截获的子串。
2.groups([default]):
以元组形式返回全部分组截获的字符串。相当于调用group(1,2,…last)。default表示没有截获字符串的组以这个值替代，默认为None。
3.groupdict([default]):
返回以有别名的组的别名为键、以该组截获的子串为值的字典，没有别名的组不包含在内。default含义同上。
4.start([group]):
返回指定的组截获的子串在string中的起始索引（子串第一个字符的索引）。group默认值为0。
5.end([group]):
返回指定的组截获的子串在string中的结束索引（子串最后一个字符的索引+1）。group默认值为0。
6.span([group]):
返回(start(group), end(group))。
7.expand(template):
将匹配到的分组代入template中然后返回。template中可以使用\id或\g、\g引用分组，但不能使用编号0。\id与\g是等价的；但\10将被认为是第10个分组，如果你想表达\1之后是字符’0’，只能使用\g0。
```

Let's go inside with an example:

	# -*- coding: utf-8 -*-
	#一个简单的match实例

	import re
	# 匹配如下内容：单词+空格+单词+任意字符
	m = re.match(r'(\w+) (\w+)(.*?)', 'hello world!')

	print "m.string:", m.string
	print "m.re:", m.re
	print "m.pos:", m.pos
	print "m.endpos:", m.endpos
	print "m.lastindex:", m.lastindex
	print "m.lastgroup:", m.lastgroup
	print "m.group():", m.group()
	print "m.group(1,2):", m.group(1, 2)
	print "m.groups():", m.groups()
	print "m.groupdict():", m.groupdict()
	print "m.start(2):", m.start(2)
	print "m.end(2):", m.end(2)
	print "m.span(2):", m.span(2)
	print r"m.expand(r'\2 \1\3'):", m.expand(r'\2 \1\3')

The output should be:

```
\# m.string: hello world!
\# m.re: <_sre.SRE_Pattern object at 0x108f93250>
\# m.pos: 0
\# m.endpos: 12
\# m.lastindex: 3
\# m.lastgroup: sign
\# m.group(1,2): ('hello', 'world')
\# m.groups(): ('hello', 'world', '!')
\# m.groupdict(): {'sign': '!'}
\# m.start(2): 6
\# m.end(2): 11
\# m.span(2): (6, 11)
\# m.expand(r'\2 \1\3'): world hello!  
```

### 3. re.search
The `re.search()` method is very similar with `re.match()`. The difference is that `re.match()` check whether **re** matches at the beginning of a string while the `re.search()` scan the whole string. `re.match()` will return None if **re** cannot match at 0 position.

First, compile again,

	pattern = re.compile(r'world')
	
Then we can use `re.search()` to match texts. If no matches return, None will be returned. The example below will fail using `re.match()`

	match = re.search(pattern,'hello world!')
	if match:
    	print match.group()

The output will be:

	world

### 4. re.split(pattern, string[, maxsplit])
Use the matched substring to split the stringbefore. The parameter **maxsplit** determine the maximum split times.

	pattern = re.compile(r'\d+')
	print re.split(pattern,'one1two2three3four4')

Output:

	['one', 'two', 'three', 'four', '']

### 5. re.findall(pattern, string[, flags])
Return a list of all the matched substrings

	pattern = re.compile(r'\d+')
	print re.findall(pattern,'one1two2three3four4')

Output

	['1', '2', '3', '4']

### 6. re.finditer(pattern, string[, flags])
Return an iterator accessing the matched substrings one by one in order.

	pattern = re.compile(r'\d+')
	for m in re.finditer(pattern,'one1two2three3four4'):
    	print m.group(),

Output

	1 2 3 4

### 7. re.sub(pattern, repl, string[, count])
Substitute repl for every matched substring.  
If repl is a string, we can use `\id` or `\g`, `\g` to quote groups, starting from index 1.  
If repl is a method, it only receives a parameter (match objec), and return a string for substitution (Now quoting groups in the returned string).  
`count` is used as the maximum subsititution timies. All are replaced when appointing no values to `count`

	pattern = re.compile(r'(\w+) (\w+)')
	s = 'i say, hello world!'

	print re.sub(pattern,r'\2 \1', s)

	def func(m):
    	return m.group(1).title() + ' ' + m.group(2).title()

	print re.sub(pattern,func, s)

Output:

```
say i, world hello!
I Say, Hello World!
```

### 8. re.subn(pattern, repl, string[, count])
Return (sub(repl, string[, count]), count)

	import re

	pattern = re.compile(r'(\w+) (\w+)')
	s = 'i say, hello world!'

	print re.subn(pattern,r'\2 \1', s)

	def func(m):
    	return m.group(1).title() + ' ' + m.group(2).title()

	print re.subn(pattern,func, s)

Output

```
('say i, world hello!', 2)
('I Say, Hello World!', 2)
```

****************************************************

## BeautifulSoup
BeautifulSoup replace the HTML document style with a tree structure. Every node of the tree is a python object. These objects can can be catogorized into four classes:

- Tag
- NavigableString
- BeautifulSoup
- Comment

### Tag
We can use the tags to easily get acess the content. It is much easier than using RegExp. However, soup tag can only find the first which meet the demand.

Let's see one examples:

	from bs4 import BeautifulSoup

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

	soup = BeautifulSoup(html) 
	print soup.title
	print soup.head
	print soup.a
	
Output

	<title>The Dormouse's story</title>
	<head><title>The Dormouse's story</title></head>
	<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>

**Tag** has two attributes: name and attrs

	print soup.name
	print soup.head.name
	print soup.p.attrs

Output

	[document]
	head
	{'class': ['title'], 'name': 'dromouse'}
	
The attrs of p tag are printed out above. It's a dictionary.	We can also get acess the single attribute.

	print soup.p['class']
	print soup.p.get('class')
	

Output

	['title']
	['title']

We can even change or delete the attribute:

	soup.p['class']="newClass"
	print soup.p
	del soup.p['class']
	print soup.p
	
Output

	<p class="newClass" name="dromouse"><b>The Dormouse's story</b></p>
	<p name="dromouse"><b>The Dormouse's story</b></p>
	
### NavigableString
This is used to get the content of a tag

	print soup.p.string
	
Output

	The Dormouse's story
	
### BeautifulSoup
This object contains the entire content of a document. We can regard it as a special **Tag**, and get its type, name, and attributes.

	print type(soup.name)
	print soup.name 
	print soup.attrs 

	
	<type 'unicode'>	
	[document]	
	{} /空字典	
	
### Comment
**Comment** can be thought of as a special **NavigableString** Object. Its output will not include comment symbols.

	print soup.a
	print soup.a.string
	print type(soup.a.string)

Output

	<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>
	Elsie      /the comment symbols are excluded
	<class 'bs4.element.Comment'>

### Attibutes of the tags
Now we want to know how to go through the BeautifulSoup tree the get content of the document.

#### 1. .children
`tag.contents` can output the child node of the tag with a list.

	print soup.head.contents
	
Output

	[<title>The Dormouse's story</title>]

`tag.children` gives out a generator object. We can get the child nodes by iterating the generator.

	print soup.head.children
	for child in  soup.body.children:
    	print child
    	
Ouptut

	<listiterator object at 0x7f71457f5710>

	<p class="title" name="dromouse"><b>The Dormouse's story</b></p>

	<p class="story">Once upon a time there were three little sisters; and their names were
	<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
	<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
	<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
	and they lived at the bottom of a well.</p>

	<p class="story">...</p>

#### 2. .descendants
`tag.contents` and `tag.children` only contain the direct child nodes. `tag.descentdants` can recurrently retrieve all the children nodes, direct or indirect.

	for child in soup.descendants:
    	print child

Output

	<html><head><title>The Dormouse's story</title></head>
	<body>
	<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
	<p class="story">Once upon a time there were three little sisters; and their names were
	<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
	<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
	<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
	and they lived at the bottom of a well.</p>
	<p class="story">...</p>
	</body></html>
	<head><title>The Dormouse's story</title></head>
	<title>The Dormouse's story</title>
	The Dormouse's story

	<body>
	<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
	<p class="story">Once upon a time there were three little sisters; and their names were
	<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
	<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
	<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
	and they lived at the bottom of a well.</p>
	<p class="story">...</p>
	</body>

	<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
	<b>The Dormouse's story</b>
	The Dormouse's story

	<p class="story">Once upon a time there were three little sisters; and their names were
	<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
	<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
	<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
	and they lived at the bottom of a well.</p>
	Once upon a time there were three little sisters; and their names were

	<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>
	 Elsie 
	,

	<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	Lacie
	 and

	<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
	Tillie
	;
	and they lived at the bottom of a well.

	<p class="story">...</p>
	...

All the nodes are printed out. Start from the most outside html tag, and next head tag, and so on and so forth.

#### 3. .string
If a tag does not contain any other tags. The content will be returned by `tag.string`. However, if tag contains child nodes. `tag.string` will return None.

	print soup.head.string
	print soup.title.string
	print soup.html.string
	
Output

	The Dormouse's story
	The Dormouse's story
	None

#### 4. .strings
`tag.strings` can get contents of multiple nodes. 

	for string in soup.strings:
    	print(repr(string))

Output

```
u"The Dormouse's story"
u'\n\n'
u"The Dormouse's story"
u'\n\n'
u'Once upon a time there were three little sisters; and their names were\n'
u'Elsie'
u',\n'
u'Lacie'
u' and\n'
u'Tillie'
u';\nand they lived at the bottom of a well.'u'\n\n'
u'...'
u'\n'
```

We can use .strippled_strings to exclude the spaces and blank lines.

	for string in soup.stripped_strings:
    	print(repr(string))

Output

```
u"The Dormouse's story"
u"The Dormouse's story"
u'Once upon a time there were three little sisters; and their names were'
u'Elsie'
u','
u'Lacie'
u'and'
u'Tillie'
u';\nand they lived at the bottom of a well.'
# u'...'
```

#### 5. .parent

	p = soup.p
	print p.parent.name

	content = soup.head.title.string
	print content.parent.name

Output
	
	body
	title

#### 6. .parents
It's a generator, can be iterated

	content = soup.head.title.string
	for parent in  content.parents:
    	print parent.name

Output

```
title
head
html
[document]
```

#### 7. .next_sibling & .previous_sibling
The sibling nodes are nodes at the samle level with the current node. `tag.next_sibling` and `tag.previous_sibling` acess the next and previous nodes respectively.

>tag.next_sibling and tag.previous_sibling usually return strings or spaces in real documents. As the spaces and blank lines are also regarded as nodes, we may get '\n' or '\n\n'

	print soup.p.next_sibling
	# this will return blank
	print soup.p.previous_sibling
	# this wil also return blank because there is '\n' infront of the first <p>
	print soup.p.next_sibling.next_sibling
	
Output

	<p class="story">Once upon a time there were three little sisters; and their names were
	<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
	<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
	<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
	and they lived at the bottom of a well.</p>

#### 8. .next_siblings & .previous_siblings
These are generators, can be iterated:

	for sibling in soup.a.next_siblings:
    	print(repr(sibling))

Output

	u',\n'
	<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	u' and\n'
	<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
	u';\nand they lived at the bottom of a well.'
	None

#### 9. .next_element & previous_element
They are different from `.next_sibling` and `.previous_sibling` that the next element can be located at other levels.

	print soup.head
	print soup.head.next_element
	print soup.head.next_sibling

Output

	<head><title>The Dormouse's story</title></head>
	print soup.head.next_element
	#next node is title
	<title>The Dormouse's story</title>
	#next sibling node is blank

#### 10. .next_elements & previous_elements
Iterators

	for element in last_a_tag.next_elements:
    	print(repr(element))

Output

	u'Tillie'
	u';\nand they lived at the bottom of a well.'
	u'\n\n'
	<p class="story">...</p>
	u'...'
	u'\n'
	None

### Methods of the tags
Search the document tree

#### 1.find_all(name , attrs , recursive , text , **kwargs )
**A. name**: find all the tags with the name and return a list. String object will be ignored.

***a. string***
This is the simplest filter

	print soup.find_all('b')
	print soup.find_all('a')

Output

	[<b>The Dormouse's story</b>]
	[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

***b. regualr expressions***
BeautifulSoup will use `re.match()` to filter content.

	import re
	for tag in soup.find_all(re.compile("^b")):
    	print(tag.name)
    	
Output

	body
	b

The above example find the tags starting with 'b'

***c. list***
BeautifulSoup will return any content match any element in the list.

	soup.find_all(["a", "b"])

Output

	[<b>The Dormouse's story</b>,
	<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
	<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
	<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

***d. True***
Return all the tag except the string nodes

	for tag in soup.find_all(True):
    	print(tag.name)

Output

```
html
head
title
body
p
b
p
a
a
a
p
```

***e.method***
We can even define a method which can take only one parameter. If the method returns True, there is matched content. Otherwise, return False.

	def has_class_but_no_id(tag):
    	return tag.has_attr('class') and not tag.has_attr('id')
	soup.find_all(has_class_but_no_id)

Output

	[<p class="title"><b>The Dormouse's story</b></p>,
	<p class="story">Once upon a time there were...</p>,
	<p class="story">...</p>]

**B. keywords**
If the keyword is not a default parameter in the `findall`, it will be regarded as attributes of tag when searching. 

BeautifulSoup will search every tag with the attribute *'id'* if the keyword is *'id'*

	print soup.find_all(id='link2')
	print soup.find_all(href=re.compile("elsie"))
	soup.find_all(href=re.compile("elsie"), id='link1')

Output

	[<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]	
	[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
	[<a class="sister" href="http://example.com/elsie" id="link1">three</a>]

If we want to use the attribute *'class'* to search, we will confront some troubles because *'class'* is a keyword of python. We can do like this

	print soup.find_all("a", class_="sister")

Output

	[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
	 <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
	 <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

Some tag attributes cannot be used like data-* in html5.
We can use *attrs* of `find_all()` to define a dictionary.

	data_soup.find_all(attrs={"data-foo": "value"})

Output

	[<div data-foo="value">foo!</div>]

**C. text**
It is similar as **name**

	soup.find_all(text="Elsie")
	soup.find_all(text=["Tillie", "Elsie", "Lacie"])
	soup.find_all(text=re.compile("Dormouse"))

Output

	[u'Elsie']
	[u'Elsie', u'Lacie', u'Tillie']
	[u"The Dormouse's story", u"The Dormouse's story"]

**D. limit**
`find_all()` will return all the results which may result
in a slow speed. We can use *limit* to limit the number
returned.

	soup.find_all("a", limit=2)

Output

	[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
	 <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]

There are three 'a' tags but return only two.

**E. recursive** 
`find_all()` will search all the childnodes, direct or indirect,
of current tag. If we only want the direct child nodes, we 
can use `recursive=False`

	soup.html.find_all("title")
	# [<title>The Dormouse's story</title>]

	soup.html.find_all("title", recursive=False)
	# []


#### 2. find( name , attrs , recursive , text , **kwargs )
It is the same as `find_all()` except that `find_all()` will 
return a list while `find()` return the result directly.

#### 3. find_parents() & find_parent()
`find_all()` and `find()` search the children and grandchiledre 
of the current tag. `find_parents()` and `find_parent()` 
search the parent and parents nodes with the same search methods.

#### 4. find_next_siblings() & find_next_sibling()
The two methods analyze the sibling nodes of curent tag using `.next_siblings` attibute. The former return all the next sibling nodes which match the filter conditions while the latter only return the closet next sibling 
node.

#### 5. find_previous_siblings() & find_previous_sibling()
Similar to 4 but using `.previous_siblings` attribute

#### 6. find_all_next() & find_next()
Use `.next_elments` attribute

#### 7. find_all_previous() & find_previous()
Use `.previous_elments` attibute

The parameters of (2-7) are the same as (1).

*********************************************************

## CCS 
When we use CCS, the **tag** name does not need any modifications, **id** name has '#' in front of it, class name has '.' in front. We can use similar methods to filter elements. The method is `soup.select()` which returns a list.

### Tag name

	print soup.select('title') 
	print soup.select('a')

Output

	[<title>The Dormouse's story</title>]
	[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

### Class name

	print soup.select('.sister')
	
Output

	[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

### id name

	print soup.select('#link1')

Output

	[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]

### Combination

	print soup.select('p #link1')
	print soup.select("head > title")

Output

	[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
	[<title>The Dormouse's story</title>]


### Attributes

	print soup.select('a[href="http://example.com/elsie"]')
	print soup.select('p a[href="http://example.com/elsie"]')
	
Output

	[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
	[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
















