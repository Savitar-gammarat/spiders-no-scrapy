#coding:utf-8
import sys
sys.path.append("..")
from config import SouHuConfig as sh
from logger import Logger
from pipelines import Pipeline

import requests
from lxml import etree
import re

class SouHu(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
    }
    pattern_img = re.compile(r'http://www.sohu.com/picture.*?',re.S)

    def first_requests(self):
        try:
            response = requests.get('http://www.sohu.com/',headers=self.headers)
        except:
            Logger().setLogger(sh.log_path, 4, "Failed to requests Souhu home")
            pass

        selector = etree.HTML(response.content)
        detail_urls = []
        partA = selector.xpath('/html/body/div[4]/div[2]/div[1]/div/div[2]/div/div/div[1]//a/@href')
        partB = selector.xpath('/html/body/div[4]/div[2]/div[1]/div/div[2]/div/div/div[2]/div//a/@href')

        for part in partA:
            detail_urls.append(part)

        for part in partB:
            if not re.match(self.pattern_img, part):
                detail_urls.append(part)

        return detail_urls

    def second_requests(self, detail_urls):
        for detail_url in detail_urls:
            try:
                response = requests.get(detail_url,headers=self.headers)
            except:
                Logger().setLogger(sh.log_path, 2, "Failed to requests Souhu detail page,url is " + detail_url)
                pass

            selector = etree.HTML(response.text)
            item = dict()
            item['link'] = detail_url
            item['title'] = self.xpath_out(selector.xpath('//*[@id="article-container"]/div[2]/div[1]/div[1]/div[1]/h1/text()'))
            item['datetime'] = self.xpath_out(selector.xpath('//*[@id="news-time"]/text()'))
            item['intro'] = self.xpath_out(selector.xpath('//*[@id="mp-editor"]/p[2]/text()'))

            if item['title'] != None:
               yield item

    def xpath_out(self, list):
        if list == []:
            str = None
        elif list == None:
            str = None
        else:
            str = list[0].encode('utf8').decode('utf8').strip()
        return str

def run():
    sets = Pipeline(sh.site_id, sh.site_name).structure_set()
    Pipeline(sh.site_id, sh.site_name).open_spider(sets)
    detail_urls = SouHu().first_requests()

    for item in SouHu().second_requests(detail_urls):
        Pipeline(sh.site_id, sh.site_name).process_item(item)
        Pipeline(sh.site_id, sh.site_name).upload_item(item, sets)

    try:
        Pipeline(sh.site_id, sh.site_name).close_spider()
    except:
        Logger().setLogger(sh.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    run()