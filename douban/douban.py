#coding:utf-8
import sys
sys.path.append("..")
from config import DoubanConfig as do
from logger import Logger

import requests
from lxml import etree
import re

class Douban(object):
    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
    }
    hot_pattern = re.compile(r'.*?(\d*)人浏览$',re.S)


    def first_requests(self):
        try:
            explore = requests.get('https://www.douban.com/explore/',headers=self.headers,timeout=5)
        except:
            Logger.setLogger(do.log_path,4,"Failed to requests douban explore")
            pass
        selector = etree.HTML(explore.text)
        gallery = selector.xpath('//*[@id="gallery_main_frame"]/div[@class="item"]')

        for g in gallery:
            item = dict()
            item['link'] = self.get_out(g.xpath('div[@class="bd"]/div/div[@class="title"]/a/@href'))
            item['title'] = self.get_out(g.xpath('div[@class="bd"]/div/div[@class="title"]/a/text()'))
            item['image'] = str(self.get_out(g.xpath('div[@class="bd"]/div[@class="pic"]/a/@style')))[21:-1]
            item['intro'] = self.get_out(g.xpath('div[@class="bd"]/div/p/a/text()'))
            if item['title']:
                    yield item
        try:
            home = requests.get('https://www.douban.com/',headers=self.headers,timeout=5)
        except:
            Logger.setLogger(do.log_path,4,"Failed to requests douban home")
            pass
        selector = etree.HTML(home.text)
        side = selector.xpath('//*[@id="anony-sns"]/div/div[2]/div[2]/ul/div/ul/li')
        for s in side:
            item = dict()
            item['link'] = self.get_out(s.xpath('a/@href'))
            item['title'] = self.get_out(s.xpath('a/text()'))
            item['hot'] = self.get_out(s.xpath('span/text()'))
            if item['hot']:
                item['hot'] = re.match(self.hot_pattern, str(item['hot'])).group(1)

            if item['title']:
                yield item

    def get_out(self, list):
        if list == []:
            str = None
        elif list == None:
            str = None
        else:
            str = list[0]
        return str


Douban().first_requests()