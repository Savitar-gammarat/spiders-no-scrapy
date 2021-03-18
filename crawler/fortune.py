#coding:utf-8
import sys
sys.path.append("..")
from config import FortuneConfig as fo
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
from lxml import etree


class Fortune(object):
    url = 'http://www.fortune.com/'

    def first_requests(self):

        response = Req(self.url, proxy=True).get_select()
        selector = etree.HTML(response.text)
        set = []
        partA = selector.xpath('//div[@class="grid__wrapper--41aq_ grid__featureThreeGrid--1FMOs"]/ul[@class="grid__list--2G2Hx"]/li')
        partB = selector.xpath('//ul[@class="theLatest__list--3Cuet"]/li')
        partC = selector.xpath('//div[@class="grid__wrapper--41aq_"]/ul[@class="grid__list--2G2Hx"]/li')

        for part in partA:
            item = dict()
            item['title'] = xpath_out(part.xpath('div/a[2]/div/text()')).strip()
            item['link'] = xpath_out(part.xpath('div/a[2]/@href'))
            if not item['link'] in set:
                set.append(item['link'])
                yield item

        for part in partB:
            item = dict()
            item['title'] = xpath_out(part.xpath('div/a/div/text()')).strip()
            item['link'] = xpath_out(part.xpath('div/a/@href'))
            if not item['link'] in set:
                set.append(item['link'])
                yield item


        for part in partC:
            item = dict()
            item['title'] = xpath_out(part.xpath('div/a[2]/div/text()')).strip()
            item['link'] = xpath_out(part.xpath('div/a[2]/@href'))
            if not item['link'] in set:
                set.append(item['link'])
                yield item


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
    # fo.log_path = "../" + fo.log_path
    run()
