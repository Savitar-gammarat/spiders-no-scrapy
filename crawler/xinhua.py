#coding:utf-8
import sys
sys.path.append("..")
from config import XinHuaConfig as xh
from logger import Logger
from pipelines import Pipeline

import requests
from lxml import etree
import datetime
import re


class Xinhua(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
    }
    today = str(datetime.date.today()).replace('-','')
    re_title = re.compile(r'.{4,}',re.S)

    def first_requests(self):
        url = 'http://www.news.cn/cover' + self.today + 'a/index.htm'
        try:
            response = requests.get(url, headers=self.headers)
        except:
            Logger().setLogger(xh.log_path, 4, "Failed to requests Xinhua home")
            pass
        if response.status_code == 404:
            url = 'http://www.news.cn/cover' + str(datetime.date.today() - datetime.timedelta(days=1)).replace('-','') + 'a/index.htm'
            response = requests.get(url, headers=self.headers)

        selector = etree.HTML(response.content)
        hrefs = selector.xpath('//*[@id="headLine"]/div[5]/div[3]//a')
        url_set = []
        for href in hrefs:
            if not href in url_set:
                url_set.append(href)  #去重操作

                item = dict()
                item['title'] = self.xpath_out(href.xpath('text()'))
                item['link'] = self.xpath_out(href.xpath('@href'))

                if item['title'] != None:
                    if re.match(self.re_title, item['title']):
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
    sets = Pipeline(xh.site_id, xh.site_name).structure_set()
    Pipeline(xh.site_id, xh.site_name).open_spider(sets)

    for item in Xinhua().first_requests():
        Pipeline(xh.site_id, xh.site_name).process_item(item)
        Pipeline(xh.site_id, xh.site_name).upload_item(item, sets)

    try:
        Pipeline(xh.site_id, xh.site_name).close_spider()
    except:
        Logger().setLogger(xh.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    run()