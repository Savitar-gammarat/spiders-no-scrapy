#coding:utf-8
import sys
sys.path.append("..")
from config import BBCConfig as bbc
from logger import Logger
from pipelines import Pipeline
from func import Req,xpath_out
from lxml import etree

class BBC(object):
    url = 'https://www.bbc.com/'

    def first_requests(self):
        selector = etree.HTML(Req(self.url, proxy=True).get_select().text)
        partA = selector.xpath('//div[@class="module__content"]/ul[@class="media-list"]/li')
        partB = selector.xpath('//div[@class="module__content"]/ul[@class="media-list media-list--fixed-height"]/li')

        for part in partA:
            item = dict()
            item['title'] = xpath_out(part.xpath('div/div[@class="media__content"]/h3/a/text()'))
            if item['title'] is not None:
                item['title'] = item['title'].strip()
                item['link'] = xpath_out(part.xpath('div/div[@class="media__content"]/h3/a/@href'))
                yield item
        for part in partB:
            item = dict()
            item['title'] = xpath_out(part.xpath('div/div[@class="media__content"]/h3/a/text()'))
            if item['title'] is not None:
                item['title'] = item['title'].strip()
                item['link'] = xpath_out(part.xpath('div/div[@class="media__content"]/h3/a/@href'))
                yield item

        # for section in sections:
        #     item = dict()
        #     item['title'] = xpath_out(section.xpath('text()'))
        #     item['link'] = xpath_out(section.xpath('@href'))

        #     if item['title'] is not None:
        #         yield item

    # def first_requests(self):
    #     response = Req(url=self.url, proxy=True).get_select()
    #     if response is not None:
    #         selector = etree.HTML(response.content)
    #         partA = selector.cssselect('.nw-c-most-watched div ol li')
    #         partB = selector.cssselect('.nw-c-most-read div div:nth-child(2) ol li')
    #         partA_url = []
    #         partB_url = []

    #         for part in partA:
    #             A = xpath_out(part.xpath('span/div/a/@href'))
    #             if A is not None:
    #                 partA_url.append('https://www.bbc.com' + A)
    #         for part in partB:
    #             B = xpath_out(part.xpath('span/div/a/@href'))
    #             if B is not None:
    #                 partB_url.append('https://www.bbc.com' + B)

    #         urls = dict()
    #         urls['A'] = partA_url
    #         urls['B'] = partB_url
    #         return urls

    # def second_requests(self, urls):
    #     for url in urls['A']:
    #         response = Req(url=url, proxy=True).get_select()
    #         if response is not None:
    #             selector = etree.HTML(response.content)
    #             item = dict()
    #             item['title'] = xpath_out(selector.cssselect('.vxp-media__body h1')).text
    #             item['link'] = response.url
    #             yield item

    #     for url in urls['B']:
    #         response = Req(url=url, proxy=True).get_select()
    #         if response is not None:
    #             selector = etree.HTML(response.content)
    #             item = dict()
    #             item['title'] = xpath_out(selector.xpathselect('.story-body__h1'))
    #             if item['title'] != None:
    #                 item['title'] = item['title'].text
    #                 item['link'] = response.url
    #                 yield item

def run():
    sets = Pipeline(bbc.site_id, bbc.site_name).structure_set()
    Pipeline(bbc.site_id, bbc.site_name).open_spider(sets)

    for item in BBC().first_requests():
        Pipeline(bbc.site_id, bbc.site_name).process_item(item)
        Pipeline(bbc.site_id, bbc.site_name).upload_item(item, sets)

    try:
        Pipeline(bbc.site_id, bbc.site_name).close_spider()
    except:
        Logger().setLogger(bbc.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    # bbc.log_path = "../" + bbc.log_path
    run()