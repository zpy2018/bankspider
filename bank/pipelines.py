# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .sql import Sql


class BankPipeline(object):
    def process_item(self, item, spider):
        # print('/n/n/n/n/n/n/n/n/n/n开始保存%s /n/n/n/n/n/n/n/n/n/n/n/n/n'% item['url'])
        num = item['num']
        name = item['name']
        url = item['url']
        bank = item['bank']
        links = item['links']
        ret = Sql.select(num)
        if ret[0] == 1:
            print('已经存在')
            return item
        f = open('web/files/' + item['num'] + '.txt', 'w', encoding='utf-8')
        f.write(item['text'])
        f.close()
        Sql.insert(num, name, url, bank, links)
        return item


        # print(item['links'])
        # return item
