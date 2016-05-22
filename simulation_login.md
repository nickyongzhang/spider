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

In this case, we want to directly use cookie to 
![cookie](https://raw.githubusercontent.com/nickzylove/spider/master/simulation_login/cookie.png =250x100)

## Direct Crawling

*******************************************************

**P.S.**: All the content above are put in several python scripts in the simulation_login folder.










