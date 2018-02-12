# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
from bs4 import BeautifulSoup
from bank.items import BankItem


class ZigongSpider(scrapy.Spider):
    name = 'zigong'
    allowed_domains = ['www.zgbank.com.cn']
    start_urls = ['http://www.zgbank.com.cn/']

    def start_requests(self):
        for i in range(5):
            dic = {'id': i}
            url = 'http://www.zgbank.com.cn/list.php?fid-42-page-' + str(i + 1) + '.htm'
            yield Request(url, self.parse, meta=dic)

    def parse(self, response):
        item = {}
        count = 0
        for info in re.findall('<span style="float:left;">.*?</a> ', response.text):
            dic = BeautifulSoup(info).a.attrs
            item['name'] = dic['title']
            item['url'] = self.start_urls[0] + dic['href']
            item['bank'] = '自贡银行'
            item['num'] = 'zg' + str(count + response.meta['id'] * 16)
            count += 1
            # print('/n/n/n/n/n/n/n/n/n/n开始抓取%s /n/n/n/n/n/n/n/n/n/n/n/n/n'% item['url'])
            yield Request(item['url'], self.get_info, meta=item)

    def get_info(self, response):
        item = BankItem()
        item['name'] = response.meta['name']
        item['url'] = response.meta['url']
        item['bank'] = response.meta['bank']
        item['num'] = response.meta['num']

        soup = BeautifulSoup(re.findall('<span id="post1">.*?</span>', response.text.replace('\n', ''))[0])
        if len(soup.text.replace('\n', '')) < 5:
            text = 'pic'
            links = soup.img.attrs['src']
        else:
            text = ''
            for word in re.findall('<P.*?</FONT></P>', response.text):
                text += (BeautifulSoup(word).text + '\n')
            links = '_just_a_split_'.join([str(x) for x in soup.find_all('a')])
        item['text'] = text
        item['links'] = links
        # print('/n/n/n/n/n/n/n/n/n/n处理结束，等待保存%s /n/n/n/n/n/n/n/n/n/n/n/n/n'% item['url'])
        return item






