#coding:utf-8
import sys
sys.path.append("..")
from config import BBCConfig as bbc
from logger import Logger
from pipelines import Pipeline

import requests
from lxml import etree


class BBC(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
    }
    ip = 'localhost:1080'
    proxies = {
        'http': 'http://' + ip,
        'https': 'https://' + ip
    }

    def first_requests(self):
        try:
            response = requests.get('https://www.bbc.com/news',headers=self.headers,proxies=self.proxies)
        except:
            Logger().setLogger(bbc.log_path, 4, "Failed to get BBC home web page")
            pass

        selector = etree.HTML(response.content)
        partA = selector.cssselect('.nw-c-most-watched div ol li')
        partB = selector.cssselect('.nw-c-most-read div div:nth-child(2) ol li')

        partA_url = []
        partB_url = []
        for part in partA:
            partA_url.append(self.xpath_out(part.xpath('span/div/a/@href')))
        for part in partB:
            partB_url.append(self.xpath_out(part.xpath('span/div/a/@href')))

        urls = dict()
        urls['A'] = partA_url
        urls['B'] = partB_url
        return urls

    def second_requests(self, urls):
        for url in urls['A']:
            try:
                response = requests.get('https://www.bbc.com' + url,headers=self.headers,proxies=self.proxies)
            except:
                Logger().setLogger(bbc.log_path, 4, "Failed to get BBC A class detail web page")
                pass
            selector = etree.HTML(response.content)

            item = dict()
            item['title'] = self.xpath_out(selector.cssselect('.vxp-media__body h1')).text
            item['link'] = url
            item['image'] = self.xpath_out(selector.cssselect('.vxp-media__player img')).get('src')
            yield item


        for url in urls['B']:
            try:
                response = requests.get('https://www.bbc.com' + url,headers=self.headers,proxies=self.proxies)
            except:
                Logger().setLogger(bbc.log_path, 2, "Failed to get BBC B class detail web page")
                pass
            selector = etree.HTML(response.content)

            item = dict()
            item['title'] = self.xpath_out(selector.cssselect('.story-body__h1'))
            if item['title'] != None:
                item['title'] = item['title'].text
                item['link'] = url
                item['intro'] = self.xpath_out(selector.cssselect('.story-body__introduction')).text
                yield item


    def xpath_out(self, list):
        if list == []:
            str = None
        elif list == None:
            str = None
        else:
            str = list[0]
        return str


def run():
    sets = Pipeline(bbc.site_id, bbc.site_name).structure_set()
    Pipeline(bbc.site_id, bbc.site_name).open_spider(sets)
    urls = BBC().first_requests()

    for item in BBC().second_requests(urls):
        Pipeline(bbc.site_id, bbc.site_name).process_item(item)
        Pipeline(bbc.site_id, bbc.site_name).upload_item(item, sets)

    try:
        Pipeline(bbc.site_id, bbc.site_name).close_spider()
    except:
        Logger().setLogger(bbc.log_path, 4, "Failed to close spider,db_session may failed")
        pass


if __name__ == '__main__':
    run()
