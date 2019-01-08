#coding:utf-8
import sys
sys.path.append("..")
from config import NeteaseConfig as ne
from logger import Logger
from pipelines import Pipeline

import requests
from lxml import etree
import re

class Netease(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
    }

    def first_requests(self):
        try:
            response = requests.get('http://news.163.com/rank/', headers=self.headers)
        except:
            Logger().setLogger(ne.log_path, 4, "Failed to get detail_page_urls")
            pass
        print(response)
        selector = etree.HTML(response.text)
        detail_url = []
        partA = selector.cssselect('body > div.area.areabg1 > div:nth-child(2) > div > div.tabContents.active > table > tr')
        try:
            partA.pop(0)
            for part in partA:
                item = dict()
                item['link'] = part.xpath('td[1]/a/@href')[0]
                item['title'] = part.xpath('td[1]/a/text()')[0]
                item['hot'] = part.xpath('td[2]/text()')[0]
                detail_url.append(item)

            partB = selector.cssselect('body > div.area.areabg1 > div:nth-child(6) > div > div:nth-child(3) > table > tr')
            partB.pop(0)
            for part in partB:
                item = dict()
                item['link'] = part.xpath('td[1]/a/@href')[0]
                item['title'] = part.xpath('td[1]/a/text()')[0]
                item['hot'] = part.xpath('td[2]/text()')[0]
                detail_url.append(item)
        except:
            Logger().setLogger(ne.log_path, 2, "Failed to get detail_page_url from home")
            pass

        return detail_url

    def second_requests(self, detail_url):
        code_pattern = re.compile(r'.*?(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?',re.S)
        for detail in detail_url:
            try:
                response = requests.get(detail['link'], headers=self.headers)
            except:
                Logger().setLogger(ne.log_path, 2, "Failed to get detail_page, url is " + detail['link'])
                pass
            selector = etree.HTML(response.content)
            detail['datetime'] = selector.xpath('//*[@id="epContentLeft"]/div[1]/text()')
            if detail['datetime'] == []:
                detail['datetime'] = None
            elif detail['datetime'] == None:
                pass
            else:
                detail['datetime'] = re.findall(code_pattern, str(detail['datetime'][0]))[0]

            yield detail

    def process_item(self,item):
        item['hot'] = float(round(int(item['hot']) / 10000, 2))
        return item


def run():
    sets = Pipeline(ne.site_id, ne.site_name).structure_set()
    Pipeline(ne.site_id, ne.site_name).open_spider(sets)

    detail_url = Netease().first_requests()

    for item in Netease().second_requests(detail_url):
        Netease().process_item(item)
        Pipeline(ne.site_id, ne.site_name).process_item(item)
        Pipeline(ne.site_id, ne.site_name).upload_item(item, sets)

    try:
        Pipeline(ne.site_id, ne.site_name).close_spider()
    except:
        Logger().setLogger(ne.log_path, 4, "Failed to close spider,db_session may failed")
        pass


if __name__ == '__main__':
    # ne.log_path = "../" + ne.log_path
    run()
