#coding:utf-8
import sys
sys.path.append("..")
from config import PhoenixConfig as ph
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
from lxml import etree
import re

class Phoenix(object):
    url = 'https://www.ifeng.com/'
    detail_patternA = re.compile(r'https?://news.ifeng.com/[ac]/.*?',re.S)
    detail_patternB = re.compile(r'heep://v.ifeng.com/.*?',re.S)

    detail_page_pattern = re.compile(r'.*?"docData":(.*?}})};.*?',re.S)

    def first_requests(self):
        response = Req(self.url).get_select()
        selector = etree.HTML(response.text)
        partA = selector.xpath('//div[@class="left_box-7d48CK7i"]/div[@class="hot_box-1yXFLW7e"]/div[@class="news_list-1dYUdgWQ"]//a')
        partB = selector.xpath('//div[@class="center_box-2F8qYPeE"]/div[@class="tabBodyItemActive-H7rMJtKB"]/div[@class="news_list-1dYUdgWQ"]//a')

        for part in partA:
            item = dict()
            item['title'] = xpath_out(part.xpath('text()'))
            item['link'] = xpath_out(part.xpath('@href'))
            yield item

        for part in partB:
            item = dict()
            item['title'] = xpath_out(part.xpath('text()'))
            item['link'] = xpath_out(part.xpath('@href'))
            yield item

    # def first_requests(self):
    #     response = Req(self.url).get_select()
    #     selector = etree.HTML(response.content)
    #     containers = selector.xpath('//*[@id="headLineDefault"]/ul/ul')

    #     for container in containers:
    #         headlines = container.xpath('li/h1/a')
    #         for headline in headlines:
    #             item = dict()
    #             item['link'] = xpath_out(headline.xpath('@href'))
    #             item['title'] = xpath_out(headline.xpath('text()'))
    #             yield item

    #         news = container.xpath('li/a')
    #         for new in news:
    #             if re.match(self.detail_patternA, xpath_out(new.xpath('@href'))) or re.match(self.detail_patternB, xpath_out(new.xpath('@href'))):
    #                 item = dict()
    #                 item['link'] = xpath_out(new.xpath('@href'))
    #                 item['title'] = xpath_out(new.xpath('text()'))
    #                 yield item

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
