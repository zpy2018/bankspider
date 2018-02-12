# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
from bs4 import BeautifulSoup
from bank.items import BankItem
import json


class ChengduSpider(scrapy.Spider):
    name = 'chengdu'
    allowed_domains = ['www.cdrcb.com']
    start_urls = ['http://www.cdrcb.com/news']

    def start_requests(self):
        for i in range(5):
            dic = {'id': i}
            url = 'http://www.cdrcb.com/news/newsTable.php'
            data = {
                'type': '1',
                'index': str(i),
                'total': '10',
                'count': '0' if i == 0 else '54'
            }
            yield scrapy.FormRequest(url, formdata=data, callback=self.parse, meta=dic)

    def parse(self, response):
        item = {}
        dic = json.loads(response.text)
        soup = BeautifulSoup(dic['str'])
        count = 0
        for info in soup.find_all('tr'):
            item['name'] = str(info.a.string)
            item['url'] = self.start_urls[0] + info.a.attrs['href'][1:]
            item['bank'] = '成都农商银行'
            item['num'] = 'cd' + str(count + response.meta['id'] * 10)
            count += 1
            yield Request(item['url'], self.get_info, meta=item)

    def get_info(self, response):
        item = BankItem()
        soup = BeautifulSoup(response.text)
        *infos, = soup.find_all('div', 'maincontentd')[0].children
        item['name'] = response.meta['name']
        item['url'] = response.meta['url']
        item['bank'] = response.meta['bank']
        item['num'] = response.meta['num']
        loc = infos[4].text.find('：')
        # item['date'] = infos[4].text[loc + 1:]
        item['text'] = infos[5].text
        links = [str(x) for x in infos[5].find_all('a')]
        item['links'] = '_just_a_split_'.join(links)
        return item




