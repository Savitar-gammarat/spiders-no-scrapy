#coding:utf-8
import sys
sys.path.append("..")
from config import DoNewsConfig as dn
from logger import Logger
from pipelines import Pipeline

import requests
from lxml import etree

class DoNews(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
    }

    def first_requests(self):
        try:
            response = requests.get('http://www.donews.com/',headers=self.headers)
        except:
            Logger().setLogger(dn.log_path, 4, "Failed to requests donews home")
            pass

        selector = etree.HTML(response.text)
        partA = selector.xpath('/html/body/div[5]/div[3]/div[2]/dl')
        partB = selector.xpath('/html/body/div[9]/div[2]/div/dl')
        for part in partA:
            item = dict()
            item['link'] = self.xpath_out(part.xpath('dd/h3/a/@href'))
            item['title'] = self.xpath_out(part.xpath('dd/h3/a/text()'))
            item['intro'] = self.xpath_out(part.xpath('dd/p[1]/text()'))
            item['image'] = self.xpath_out(part.xpath('dt/a/img/@src'))
            yield item

        for part in partB:
            item['link'] = self.xpath_out(part.xpath('dd/h3/a/@href'))
            item['title'] = self.xpath_out(part.xpath('dd/h3/a/text()'))
            item['intro'] = self.xpath_out(part.xpath('dd/p[1]/text()'))
            item['image'] = self.xpath_out(part.xpath('dt/a/img/@src'))
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
    sets = Pipeline(dn.site_id, dn.site_name).structure_set()
    Pipeline(dn.site_id, dn.site_name).open_spider(sets)

    for item in DoNews().first_requests():
        Pipeline(dn.site_id, dn.site_name).process_item(item)
        Pipeline(dn.site_id, dn.site_name).upload_item(item, sets)

    try:
        Pipeline(dn.site_id, dn.site_name).close_spider()
    except:
        Logger().setLogger(dn.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    run()