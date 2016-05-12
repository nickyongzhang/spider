# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
__author__ = Zhang Yong

Using Scrapy to get web page content

#we first need to start a scrapy project
scrapy startproject douban

#scrapy 文件结构
item.py: 定义需要抓取并需要后期处理的数据
settings.py: 配置scrapy，从而修改user-agent,设定爬取时间间隔，设置代理，配置各种中间件等等
piplines.py: 存放执行后期数据处理的功能，从而使得数据的爬取和处理分开
"""

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from douban.items import DoubanItem


class Douban(CrawlSpider):
    name = "douban"
    redis_key = 'douban:start_urls'
    start_urls = ['http://movie.douban.com/top250']

    url = 'http://movie.douban.com/top250'

    def parse(self,response):
        # print response.body
        # print response.url
        item = DoubanItem()
        selector = Selector(response)
        Movies = selector.xpath('//div[@class="info"]')
        for eachMovie in Movies:
            # different from xpath of lxml which use .content()
            title = eachMovie.xpath('div[@class="hd"]/a/span/text()').extract()
            fullTitle = ''
            for each in title:
                fullTitle += each
            movieInfo = eachMovie.xpath('div[@class="bd"]/p/text()').extract()
            star = eachMovie.xpath('div[@class="bd"]/div[@class="star"]/span/em/text()').extract()
            quote = eachMovie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            #quote may be empty
            if quote:
                quote = quote=quote[0]
            else:
                quote = ''
            item['title']=fullTitle
            item['movieInfo']=';'.join(movieInfo)
            item['star'] = star
            item['quote'] = quote
            yield item
        nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()
        if nextLink:
            nextLink = nextLink[0]
            print nextLink
            yield Request(self.url + nextLink, callback=self.parse)
