#coding:utf-8
import sys
sys.path.append("..")
from config import FortuneConfig as fo
from logger import Logger
from pipelines import Pipeline

import requests
from lxml import etree


class Fortune(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
    }
    ip = 'localhost:1080'
    proxies = {
        'http': 'http://' + ip,
        'https': 'https://' + ip
    }

    def first_requests(self):
        try:
            response = requests.get('http://www.fortune.com/',headers=self.headers,proxies=self.proxies)
        except:
            Logger().setLogger(fo.log_path, 4, "Failed to get BBC home web page")
            pass

        selector = etree.HTML(response.text)
        set = []
        partA = selector.xpath('//div[@class="column text-align-left visible-desktop visible-mobile last-column"]/div[@class="column-tout   "]')
        partB = selector.xpath('//div[@class="column large-headline"]/div[@class="column-tout   "]')
        partC = selector.xpath('//div[@class="column column-feed"]/div[@class="column-tout   "]')

        for part in partA:
            item = dict()
            item['title'] = self.xpath_out(part.xpath('div[1]/a/text()')).strip()
            item['link'] = "www.fortune.com/" + self.xpath_out(part.xpath('div[1]/a/@href'))
            if not item['link'] in set:
                set.append(item['link'])
                yield item

        for part in partB:
            item = dict()
            item['title'] = self.xpath_out(part.xpath('div[1]/a/text()')).strip()
            item['link'] = "www.fortune.com/" + self.xpath_out(part.xpath('div[1]/a/@href'))
            item['intro'] = self.xpath_out(part.xpath('div[2]/text()')).strip()
            item['image'] = self.xpath_out(part.xpath('a/div/noscript/div/img/@src'))
            if not item['link'] in set:
                set.append(item['link'])
                yield item


        for part in partC:
            item = dict()
            item['title'] = self.xpath_out(part.xpath('div[1]/a/text()')).strip()
            item['link'] = "www.fortune.com/" + self.xpath_out(part.xpath('div[1]/a/@href'))
            item['image'] = self.xpath_out(part.xpath('a/div/noscript/div/img/@src'))
            if not item['link'] in set:
                set.append(item['link'])
                yield item

    def xpath_out(self, list):
        if list == []:
            str = None
        elif list == None:
            str = None
        else:
            str = list[0].encode('utf8').decode('utf8')
        return str


def run():
    sets = Pipeline(fo.site_id, fo.site_name).structure_set()
    Pipeline(fo.site_id, fo.site_name).open_spider(sets)

    for item in Fortune().first_requests():
        Pipeline(fo.site_id, fo.site_name).process_item(item)
        Pipeline(fo.site_id, fo.site_name).upload_item(item, sets)

    try:
        Pipeline(fo.site_id, fo.site_name).close_spider()
    except:
        Logger().setLogger(fo.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    run()