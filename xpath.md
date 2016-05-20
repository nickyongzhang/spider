<link rel="stylesheet" href="/Users/zhangyong/highlight/styles/default.css">
<script src="/Users/zhangyong/highlight/highlight.pack.js"></script>
<script>hljs.initHighlightingOnLoad();</script>


# Xpath
> XPath is a syntax for defining parts of an XML document. XPath uses path expressions to navigate in XML documents. XPath contains a library of standard functions. XPath is a major element in XSLT. XPath is a W3C recommendation.

we use a python package named ***lxml*** to take advantage of the magic of xpath.

> lxml is the most feature-rich and easy-to-use library for processing XML and HTML in the Python language.

The grammer of xpath is very easy. We can just use some several characters to retrieve information of xml document. Let's see a demo example.


	html0 = '''
	<!DOCTYPE html>
	<html>
	<head lang="en">
    	<meta charset="UTF-8">
    	<title>测试-常规用法</title>
	</head>
	<body>
	<div id="content">
    	<ul id="useful">
        	<li>这是第一条信息</li>
        	<li>这是第二条信息</li>
        	<li>这是第三条信息</li>
    	</ul>
    	<ul id="useless">
        	<li>不需要的信息1</li>
        	<li>不需要的信息2</li>
        	<li>不需要的信息3</li>
    	</ul>

    	<div id="url">
        	<a href="http://jikexueyuan.com">极客学院</a>
        	<a href="http://jikexueyuan.com/course/" 	title="极客学院课程库">点我打开课程库</a>
    	</div>
	</div>

	</body>
	</html>
	'''

The information can be easily obtained with the following rules:

- //         --locate the root directory
- /          --find in the next level
- /text()    --obtain the text content
- /@attr     --obtain the attribute content
- starts-with(@attr, 'xxx') --point to the attribute starting with 'xxx'
- string(.)  --get all strings under a tag

Let us import the ***lxml*** package first. We also define the system's encoding method as 'utf-8'.

	from lxml import etree
	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')

Then we define a selector using **etree**

	selector = etree.HTML(html0)

The text can be directly retrieved.

	content = selector.xpath('//ul[@id="useful"]/li/text())
	for each in content:
		print each

Output

```
这是第一条信息
这是第二条信息
这是第三条信息
```

We can also obtain the attributes.

	link = selector.xpath('//a/@href')
	for each in link:
    	print each
		
	title = selector.xpath('//a/@title')
	print title[0]
	
Output

```
http://jikexueyuan.com
http://jikexueyuan.com/course/
极客学院课程库
```
Let's see some more examples.

	html1 = '''
	<!DOCTYPE html>
	<html>
	<head lang="en">
    	<meta charset="UTF-8">
    	<title></title>
	</head>
	<body>
    	<div id="test-1">需要的内容1</div>
    	<div id="test-2">需要的内容2</div>
    	<div id="testfault">需要的内容3</div>
	</body>
	</html>
	'''
	
	html2 = '''
	<!DOCTYPE html>
	<html>
	<head lang="en">
    	<meta charset="UTF-8">
    	<title></title>
	</head>
	<body>
    	<div id="test3">
        	我左青龙，
        	<span id="tiger">
            	右白虎，
            	<ul>上朱雀，
                	<li>下玄武。</li>
            	</ul>
            	老牛在当中，
        	</span>
        	龙头在胸口。
    	</div>
	</body>
	</html>
	'''

We can use `starts-with(@id,"test")` to point to the `<div>` with id starting with "test":

	selector = etree.HTML(html1)
	content = selector.xpath('//div[starts-with(@id,"test")]/text()')
	for each in content:
    	print each

Output

```
需要的内容1  
需要的内容2  
需要的内容3  
```

Now let's compare the two content-retrieving methods: `string(.)` and `/text()`.

	selector = etree.HTML(html2)
	content_1 = selector.xpath('//div[@id="test3"]/text()')
	for each in content_1:
    	print each

Output

        我左青龙，
        

        龙头在胸口。

The method `/text()` only gives out the text under the direct node. The other non-text nodes are ignored. However, the `string(.)` method can give all the text content in the child and grandchild nodes.

	data = selector.xpath('//div[@id="test3"]')[0]
	info = data.xpath('string(.)')
	content_2 = info.replace('\n','').replace(' ','')
	print content_2

Output

```
我左青龙，右白虎，上朱雀，下玄武。老牛在当中，龙头在胸口。
```

********************************************************
We use a practical example to show the magic of **xpath** below. Before that we show something about the **multiple-processing** method. We compare the time used completing a task with single-processing and multiple-processing methods. 

	from multiprocessing.dummy import Pool as ThreadPool
	import requests
	import time
	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')

	# Define a task
	def getsource(url):
    	html = requests.get(url)

	urls = []

	for i in range(1,21):
    	newpage = 'http://tieba.baidu.com/p/3522395718?pn=' + str(i)
    	urls.append(newpage)

	time1 = time.time()
	for i in urls:
    	getsource(i)
	time2 = time.time()
	print u'单线程耗时：' + str(time2-time1)

	pool = ThreadPool(8)
	time3 = time.time()
	results = pool.map(getsource, urls)
	pool.close()
	pool.join()
	time4 = time.time()
	print u'并行耗时：' + str(time4-time3)

Output

```
单线程耗时：26.4895198345
并行耗时：4.50734210014
```

The method `pool.map()` achieve the looping procedure with multiple-processing method. Now let's have a look at the practical example.

	#import the necessary packages
	from lxml import etree
	from multiprocessing.dummy import Pool as ThreadPool
	import requests
	import json
	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')

	'''重新运行之前请删除content.txt，因为文件操作使用追加方式，会导致内容太多。'''

	#write the content to the file
	def towrite(contentdict):
    	f.writelines(u'回帖时间:' + str(contentdict['topic_reply_time']) + '\n')
    	f.writelines(u'回帖内容:' + unicode(contentdict['topic_reply_content']) + '\n')
    	f.writelines(u'回帖人:' + contentdict['user_name'] + '\n\n')

	#define the spidering task
	def spider(url):
    	html = requests.get(url)
    	selector = etree.HTML(html.text)
    	content_field = selector.xpath('//div[@class="l_post j_l_post l_post_bright  "]')
    	item = {}
    	# print content_field
    	for each in content_field:
        	reply_info = json.loads(each.xpath('@data-field')[0].replace('&quot',''))
        	author = reply_info['author']['user_name']
        	content = each.xpath('div[@class="d_post_content_main"]/div/cc/div')[0]
        	content = content.xpath('string(.)')
        	reply_time = reply_info['content']['date']
        	print(content)
        	print(reply_time)
        	print(author)
        	item['user_name'] = author
        	item['topic_reply_content'] = content
        	item['topic_reply_time'] = reply_time
        	towrite(item)

	if __name__ == '__main__':
    	pool = ThreadPool(4)
    	f = open('content.txt','a')
    	pages = []
    	for i in range(1,21):
        	newpage = 'http://tieba.baidu.com/p/3522395718?pn=' + str(i)
        	pages.append(newpage)

    	# for url in pages:
    	#     spider(url)
    	results = pool.map(spider, pages)
    	pool.close()
    	pool.join()
    	f.close()

The code above uses a multiple-processing procedure to spider the content of one topic of baidutieba.

*******************************************************

**P.S.**: All the content above are put in several python scripts in the xpath folder.










