# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: 
Zhang Yong

spider the website baidutieba

"""
import urllib
import urllib2
import re

#Define a class to process tags
class Tool:
    #remove img tag and long spaces
    removeImg = re.compile('<img.*?>| {7}|')
    #remove link tag
    removeAddr = re.compile('<a.*?>|</a>')
    #replace all the line-changing tags with '\n'
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #replace <td> with \t
    replaceTD= re.compile('<td>')
    #replace the beginning of paragraph with \n and two spaces
    replacePara = re.compile('<p.*?>')
    #replace all the line-changing identifiers with '\n'
    replaceBR = re.compile('<br><br>|<br>')
    #remove other tags
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        return x.strip()

#define a new spider class
class BDTB:

    #initialization
    def __init__(self,baseUrl,seeTS,floorTag):
        #base url
        self.baseURL = baseUrl
        #sometimes we only want to see the infor of thread starter
        self.seeTS = '?see_lz='+str(seeTS)
        #we use a class object to delete the tags we don't want
        self.tool = Tool()
        #file name
        self.file = None
        #floor number
        self.floor = 1
        #defaulted file title
        self.defaultTitle = u"baidutieba"
        #whether write floor separator
        self.floorTag = floorTag

    #get source code of current page
    def getPage(self,pageNum):
        try:
            url = self.baseURL+ self.seeTS + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')

        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"Connection failed, the reason is",e.reason
                return None

    #get title of the thread
    def getTitle(self,page):
        pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    #get the number of pages of the thread
    def getPageNum(self,page):
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    #get every post content
    def getContent(self,page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            #exculude the unwanted tags
            content = "\n"+self.tool.replace(item)+"\n"
            contents.append(content.encode('utf-8'))
        return contents
   
    # define the file title
    def setFileTitle(self,title):
        if title is not None:
            self.file = open(title + ".txt","w+")
        else:
            self.file = open(self.defaultTitle + ".txt","w+")

    def writeData(self,contents):
        #write the posts into a file
        for item in contents:
            if self.floorTag == '1':
                #separate floors
                floorLine = "\n" + str(self.floor) + u"----------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print "URL is not effective any more"
            return
        try:
            print "The thread has " + str(pageNum) + "pages"
            for i in range(1,int(pageNum)+1):
                print "Loading Page " + str(i)
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        
        except IOError,e:
            print "Loading error，the reason is " + e.message
        finally:
            print "Loading successful"

print u"Enter the thread number"
baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
seeTS = raw_input("Whether to read messages of thread starter? '1' for yes and '0' for no\n")
floorTag = raw_input("Whether to separate floor messages? '1' for yes and '0' for no\n")
bdtb = BDTB(baseURL,seeTS,floorTag)
bdtb.start() 