# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BankItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field() #公告名字
    bank = scrapy.Field() #来源银行
    url = scrapy.Field() #链接
    num = scrapy.Field() #编号
    # date = scrapy.Field() #发布时间
    text = scrapy.Field() #文本内容
    links = scrapy.Field() #链接信息