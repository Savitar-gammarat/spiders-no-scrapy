#coding:utf-8
import sys
sys.path.append("..")
from config import SouHuConfig as sh
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
from lxml import etree
import re

class SouHu(object):
    url = 'http://www.sohu.com/'
    # pattern_img = re.compile(r'http://www.sohu.com/picture.*?',re.S)

    def first_requests(self):
        selector = etree.HTML(Req(self.url).get_select().text)
        partA = selector.xpath('//div[@class="focus-news-box"]/div[@class="news"]/p')
        partB = selector.xpath('//div[@class="focus-news-box"]/div[3]/div/ul/li')
        for part in partA:
            item = dict()
            item['title'] = xpath_out(part.xpath('a/@title'))
            item['link'] = xpath_out(part.xpath('a/@href'))
            yield item

        for part in partB:
            item = dict()
            item['title'] = xpath_out(part.xpath('a/@title'))
            item['link'] = xpath_out(part.xpath('a/@href'))
            yield item

        # for section in sections:
        #     item = dict()
        #     item['title'] = xpath_out(section.xpath('text()'))
        #     item['link'] = xpath_out(section.xpath('@href'))

        #     if item['title'] is not None:
        #         yield item

    # def first_requests(self):
    #     response = Req(self.url).get_select()
    #     selector = etree.HTML(response.content)
    #     detail_urls = []
    #     partA = selector.xpath('/html/body/div[4]/div[2]/div[1]/div/div[2]/div/div/div[1]//a/@href')
    #     partB = selector.xpath('/html/body/div[4]/div[2]/div[1]/div/div[2]/div/div/div[2]/div//a/@href')

    #     for part in partA:
    #         print(part)
    #         detail_urls.append(part)

    #     for part in partB:
    #         print(part)
    #         if not re.match(self.pattern_img, part):
    #             detail_urls.append(part)

    #     return detail_urls

    # def second_requests(self, detail_urls):
    #     for detail_url in detail_urls:
    #         response = Req(detail_url).get_select()
    #         selector = etree.HTML(response.text)
    #         item = dict()
    #         item['link'] = detail_url
    #         item['title'] = xpath_out(selector.xpath('//*[@id="article-container"]/div[2]/div[1]/div[1]/div[1]/h1/text()'))
    #         item['datetime'] = xpath_out(selector.xpath('//*[@id="news-time"]/text()'))

    #         if item['title'] != None:
    #            yield item

def run():
    sets = Pipeline(sh.site_id, sh.site_name).structure_set()
    Pipeline(sh.site_id, sh.site_name).open_spider(sets)

    for item in SouHu().first_requests():
        Pipeline(sh.site_id, sh.site_name).process_item(item)
        Pipeline(sh.site_id, sh.site_name).upload_item(item, sets)

    try:
        Pipeline(sh.site_id, sh.site_name).close_spider()
    except:
        Logger().setLogger(sh.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    # sh.log_path = "../" + sh.log_path
    run()
