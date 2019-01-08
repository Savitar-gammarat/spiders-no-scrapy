#coding:utf-8
import sys
sys.path.append("..")
from config import EconomistConfig as ec
from logger import Logger
from pipelines import Pipeline

import requests
from lxml import etree
from datetime import datetime

class Economic(object):
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
            response = requests.get('https://www.economist.com/latest/',headers=self.headers,proxies=self.proxies)
        except:
            Logger().setLogger(ec.log_path, 4, "Failed to get ec home web page")
            pass
        selector = etree.HTML(response.text)
        articles = selector.xpath('//div[@class="teaser-list"]/article')

        for article in articles:
            item = dict()
            item['title'] = self.xpath_out(article.xpath('a/div[2]/h3/span[2]/text()'))
            item['link'] = "https://www.economist.com" + self.xpath_out(article.xpath('a/@href'))
            item['intro'] = self.xpath_out(article.xpath('a/div[2]/div[@class="teaser__text"]/text()'))
            item['datetime'] = self.xpath_out(article.xpath('a/div[2]/div[@class="teaser__datetime"]/time/@datetime'))
            item['image'] = self.xpath_out(article.xpath('a/div[1]/div/noscript/div/img/@src'))
            item['datetime'] = str(datetime.strptime(item['datetime'], '%Y-%m-%dT%H:%M:%SZ'))
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
    sets = Pipeline(ec.site_id, ec.site_name).structure_set()
    Pipeline(ec.site_id, ec.site_name).open_spider(sets)

    for item in Economic().first_requests():
        Pipeline(ec.site_id, ec.site_name).process_item(item)
        Pipeline(ec.site_id, ec.site_name).upload_item(item, sets)

    try:
        Pipeline(ec.site_id, ec.site_name).close_spider()
    except:
        Logger().setLogger(ec.log_path, 4, "Failed to close spider,db_session may failed")

if __name__ == '__main__':
    # ec.log_path = "../" + ec.log_path
    run()
