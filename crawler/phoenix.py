#coding:utf-8
import sys
sys.path.append("..")
from config import PhoenixConfig as ph
from logger import Logger
from pipelines import Pipeline

import requests
from lxml import etree
import re

class Phoenix(object):
    headers = {
        'Host': 'www.ifeng.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
    }
    detail_headers = {
        'Host': 'news.ifeng.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
    }
    detail_patternA = re.compile(r'https?://news.ifeng.com/[ac]/.*?',re.S)
    detail_patternB = re.compile(r'heep://v.ifeng.com/.*?',re.S)

    detail_page_pattern = re.compile(r'.*?"docData":(.*?}})};.*?',re.S)

    def first_requests(self):
        try:
            response = requests.get('https://www.ifeng.com/',headers=self.headers,timeout=5)
        except:
            Logger().setLogger(ph.log_path, 4, "Failed to get detail_page_urls")
            pass
        selector = etree.HTML(response.content)
        containers = selector.xpath('//*[@id="headLineDefault"]/ul/ul')

        for container in containers:
            headlines = container.xpath('li/h1/a')
            for headline in headlines:
                item = dict()
                item['link'] = headline.xpath('@href')[0]
                item['title'] = headline.xpath('text()')[0]
                yield item

            news = container.xpath('li/a')
            for new in news:
                if re.match(self.detail_patternA, new.xpath('@href')[0]) or re.match(self.detail_patternB, new.xpath('@href')[0]):
                    item = dict()
                    item['link'] = new.xpath('@href')[0]
                    item['title'] = new.xpath('text()')[0]
                    yield item

def run():
    sets = Pipeline(ph.site_id, ph.site_name).structure_set()
    Pipeline(ph.site_id, ph.site_name).open_spider(sets)

    for item in Phoenix().first_requests():
        Pipeline(ph.site_id, ph.site_name).process_item(item)
        Pipeline(ph.site_id, ph.site_name).upload_item(item, sets)

    try:
        Pipeline(ph.site_id, ph.site_name).close_spider()
    except:
        Logger().setLogger(ph.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    # ph.log_path = "../" + ph.log_path
    run()
