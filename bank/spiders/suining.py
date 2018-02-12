# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
from bs4 import BeautifulSoup
from bank.items import BankItem


class SuiningSpider(scrapy.Spider):
    name = 'suining'
    allowed_domains = ['www.snccb.com']
    start_urls = ['http://www.snccb.com']

    def start_requests(self):
        for i in range(5):
            dic = {'id': i}
            url = 'http://www.snccb.com/list.php?tid=133&TotalResult=194&PageNo=' + str(i + 1)
            yield Request(url, self.parse, meta=dic)

    def parse(self, response):
        item ={}
        soup = BeautifulSoup(response.text)
        count = 0
        for info in soup.find_all('div', class_='tt'):
            item['name'] = str(info.a.string)
            item['url'] = self.start_urls[0] + info.a.attrs['href']
            item['bank'] = '遂宁银行'
            item['num'] = 'sn' + str(count + response.meta['id'] * 10)
            count += 1
            yield Request(item['url'], self.get_info, meta=item)

    def get_info(self, response):
        item = BankItem()
        soup = BeautifulSoup(response.text)
        infos = soup.find('div', class_='articledetail')
        item['name'] = response.meta['name']
        item['url'] = response.meta['url']
        item['bank'] = response.meta['bank']
        item['num'] = response.meta['num']
        item['links'] = ''
        item['text'] = infos.text
        return item
