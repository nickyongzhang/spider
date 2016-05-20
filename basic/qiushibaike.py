# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: 
Zhang Yong

spider the website qiushibaike

"""
import urllib
import urllib2
import re
import thread
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#we define a new class named QSBK
class QSBK:

    #initialization
    def __init__(self):
        self.pageIndex = 1
        self.stories = []
        #control parameter
        self.enable = False

    #get the source code of one page
    def getPage(self,pageIndex):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'
        headers = { 'User-Agent' : user_agent }
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url,headers = headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode

        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"Connection failed, the reason is",e.reason
                return None

    #get the needed information
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "Loading Failed"
            return None
        pattern = re.compile('<div.*?class="author.*?>.*?<h2>(.*?)</h2>.*?<div.*?class="content">(.*?)</div>.*?<div class="stats.*?class="number">(.*?)</i>',re.S)
        items = re.findall(pattern,pageCode)
        #a list to store information
        pageStories = []
        for item in items:
            #item[0] is the author，item[1] is the information，item[2] is number of likes
            pageStories.append([item[0].encode('utf-8').strip(),item[1].encode('utf-8').strip(),item[2].encode('utf-8').strip()])
        return pageStories

    #load the page and save the retrieved information
    def loadPage(self):
        #We control there are two pages' stories stored in the global variable
        if self.enable == True:
            if len(self.stories) < 2:
                #get the stories of current page
                pageStories = self.getPageItems(self.pageIndex)

                if pageStories:
                    self.stories.append(pageStories)
                    #update page index
                    self.pageIndex += 1

    #type return to get one more story and type Q to quit
    def getOneStory(self,pageStories,page):
        #run through the stories on one page
        for story in pageStories:
            #readers can input a command 
            input = raw_input()
            #when the program receive a return command, it will determine by itself whether to load a new page's stories
            self.loadPage()
            #quit when receiving Q
            if input == "Q":
                self.enable = False
                return
            print u"Page:%d\tauthor:%s\ncontent:%s\nlikes:%s\n" %(page, story[0],story[1],story[2])

    #start method
    def start(self):
        print u"正在读取糗事百科,按回车查看新段子，Q退出"
        #define a control parameter
        self.enable = True
        #load the first page
        self.loadPage()
        #control the page number of the url
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                #get stories of one page
                pageStories = self.stories[0]
                #update page numbers read
                nowPage += 1
                #delete the stories read from global variable
                del self.stories[0]
                #output the storeis
                self.getOneStory(pageStories,nowPage)

spider = QSBK()
spider.start() 