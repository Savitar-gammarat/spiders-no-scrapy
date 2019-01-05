#coding:utf-8
import sys
sys.path.append("..")
from config import WiredConfig as wd
from logger import Logger
from pipelines import Pipeline

import requests
from lxml import etree

class Wired(object):
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
            response = requests.get('https://www.wired.com/most-recent/',headers=self.headers,proxies=self.proxies)
        except:
            Logger().setLogger(wd.log_path, 4, "Failed to get BBC home web page")
            pass

        selector = etree.HTML(response.content)
        part = selector.xpath('//div[@class="archive-listing-component"]/div[1]/ul/li')
        for article in part:
            item=dict()
            item['link'] = "www.wired.com" + self.xpath_out(article.xpath('div[@class="archive-item-component__info"]/a/@href')).encode('utf8').decode('utf8')
            item['title'] = self.xpath_out(article.xpath('div[@class="archive-item-component__info"]/a/h2/text()'))
            item['intro'] = self.xpath_out(article.xpath('div[@class="archive-item-component__info"]/a/p/text()'))
            item['image'] = self.xpath_out(article.xpath('a/div/div/div/div/img/@src'))
            yield item

    def xpath_out(self, list):
        if list == []:
            str = None
        elif list == None:
            str = None
        else:
            str = list[0]
        return str

def run():
    sets = Pipeline(wd.site_id, wd.site_name).structure_set()
    Pipeline(wd.site_id, wd.site_name).open_spider(sets)

    for item in Wired().first_requests():
        Pipeline(wd.site_id, wd.site_name).process_item(item)
        Pipeline(wd.site_id, wd.site_name).upload_item(item, sets)

    try:
        Pipeline(wd.site_id, wd.site_name).close_spider()
    except:
        Logger().setLogger(wd.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    run()