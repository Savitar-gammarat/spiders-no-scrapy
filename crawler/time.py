#coding:utf-8
import sys
sys.path.append("..")
from config import TimeConfig as time
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
from lxml import etree

class Time(object):
    urls = ['https://time.com/section/us/','https://time.com/section/world/','https://time.com/section/business/','https://time.com/section/tech/']
    def first_requests(self):
        for url in self.urls:
            response = Req(url, proxy=True).get_select()
            selector = etree.HTML(response.text)
            partA = selector.xpath('//div[@class="partial hero"]/article')
            partB = selector.xpath('//div[@class="partial marquee"]/article')

            for part in partA:
                item = dict()
                item['title'] = xpath_out(part.xpath('div/h3/a/text()')).strip()
                item['link'] = "https://time.com" + xpath_out(part.xpath('div/h3/a/@href'))
                yield item


            for part in partB:
                item = dict()
                item['title'] = xpath_out(part.xpath('div/h3/a/text()')).strip()
                item['link'] = "https://time.com" + xpath_out(part.xpath('div/h3/a/@href'))
                yield item



def run():
    sets = Pipeline(time.site_id, time.site_name).structure_set()
    Pipeline(time.site_id, time.site_name).open_spider(sets)

    for item in Time().first_requests():
        Pipeline(time.site_id, time.site_name).process_item(item)
        Pipeline(time.site_id, time.site_name).upload_item(item, sets)

    try:
        Pipeline(time.site_id, time.site_name).close_spider()
    except:
        Logger().setLogger(time.log_path, 4, "Failed to close spider,db_session may failed")

if __name__ == '__main__':
    # time.log_path = "../" + time.log_path
    run()
