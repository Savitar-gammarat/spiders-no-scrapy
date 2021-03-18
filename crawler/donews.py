#coding:utf-8
import sys
sys.path.append("..")
from config import DoNewsConfig as dn
from logger import Logger
from pipelines import Pipeline
from func import Req,xpath_out
from lxml import etree


class DoNews(object):
    url = 'https://www.donews.com/newsflash/index'

    def first_requests(self):
        response = Req(self.url).get_select()

        if response is not None:
            selector = etree.HTML(response.text)
            parts = selector.xpath('//div[@id="newloadmore"]/div')

            for part in parts:
                item = dict()
                item['link'] = xpath_out(part.xpath('a/@href'))
                item['title'] = xpath_out(part.xpath('a/div[1]/text()'))
                yield item


def run():
    sets = Pipeline(dn.site_id, dn.site_name).structure_set()
    Pipeline(dn.site_id, dn.site_name).open_spider(sets)

    for item in DoNews().first_requests():
        print(item)
        Pipeline(dn.site_id, dn.site_name).process_item(item)
        Pipeline(dn.site_id, dn.site_name).upload_item(item, sets)

    try:
        Pipeline(dn.site_id, dn.site_name).close_spider()
    except:
        Logger().setLogger(dn.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    # dn.log_path = "../" + dn.log_path
    run()
