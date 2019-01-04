#coding:utf-8
import sys
sys.path.append("..")
from config import HuanqiuConfig as hq
from logger import Logger
from pipelines import Pipeline

import requests
from lxml import etree
import re


class Huanqiu(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
    }

    def first_requests(self):
        try:
            response = requests.get('http://www.huanqiu.com/', headers=self.headers)
        except:
            Logger().setLogger(hq.log_path, 4, "Failed to get detail_page_urls")
            pass

        selector = etree.HTML(response.content)
        detail_urls = []
        partA = selector.xpath('/html/body/div[2]/div[5]/div/div[1]/div[2]/div[2]/dl//a/@href')
        for part in partA:
            detail_urls.append(part)

        partB = selector.xpath('/html/body/div[2]/div[5]/div/div[1]/div[3]/div[3]/div//a/@href')
        for part in partB:
            detail_urls.append(part)

        return detail_urls

    def second_requests(self, detail_urls):
        for detail_url in detail_urls:
            try:
                response = requests.get(detail_url, headers=self.headers)
            except:
                Logger().setLogger(hq.log_path, 2, "requests detail page failed, url is " + detail_url)
                pass
            selector = etree.HTML(response.content)
            item = dict()
            item['link'] = detail_url
            item['title'] = self.xpath_out(selector.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/h1/text()'))
            if item['title']:
                item['datetime'] = self.xpath_out(selector.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[1]/span[1]/text()'))
                item['intro'] = self.process_intro(self.xpath_out(selector.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/p[1]/text()')))
            else:
                item['title'] = self.xpath_out(selector.xpath('/html/body/div[2]/div[3]/div[1]/div[2]/h1/text()'))
                if item['title']:
                    item['datetime'] = self.xpath_out(selector.xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[1]/span[1]/text()'))
                    item['intro'] = self.process_intro(self.xpath_out(selector.xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[2]/p[1]/text()')))
                else:
                    item['title'] = self.xpath_out(selector.xpath('/html/body/div[4]/div/div[2]/div[1]/h1/text()'))
                    item['datetime'] = self.xpath_out(selector.xpath('//*[@id="time"]/text()'))
                    item['intro'] = self.process_intro(self.xpath_out(selector.xpath('/html/body/div[4]/div/div[2]/div[1]/div/p[1]/text()')))

            yield item

    def process_item(self, item):
        # 对item['datetime']进行格式化处理
        datetime_pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', re.S)
        datetime_patternB = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', re.S)
        if type(item['title']) == str:
            if re.match(datetime_pattern, item['datetime']):
                return item
            elif re.match(datetime_patternB, item['datetime']):
                return item
            else:
                item['datetime'] = None
                return item
        else:
            pass


    def xpath_out(self, list):
        if list == []:
            str = None
        elif list == None:
            str = None
        else:
            str = list[0].encode('utf8').decode('utf8')
        return str

    def process_intro(self, str):
        if not str:
            out = None
        else:
            out = str.replace('\u3000\u3000','')
        if out == '':
            out = None
        return out

def run():
    sets = Pipeline(hq.site_id, hq.site_name).structure_set()
    Pipeline(hq.site_id, hq.site_name).open_spider(sets)

    detail_url = Huanqiu().first_requests()

    for item in Huanqiu().second_requests(detail_url):
        Huanqiu().process_item(item)
        Pipeline(hq.site_id, hq.site_name).process_item(item)
        Pipeline(hq.site_id, hq.site_name).upload_item(item, sets)

    try:
        Pipeline(hq.site_id, hq.site_name).close_spider()
    except:
        Logger().setLogger(hq.log_path, 4, "Failed to close spider,db_session may failed")
        pass


if __name__ == '__main__':
    run()
