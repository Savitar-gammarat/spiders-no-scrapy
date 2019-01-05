#coding:utf-8
import sys
sys.path.append("..")
from config import NewYorkTimeConfig as nyk
from logger import Logger
from pipelines import Pipeline

import requests
from lxml import etree

class NewYork(object):
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
            response = requests.get('https://www.nytimes.com/trending/',headers=self.headers,proxies=self.proxies)
        except:
            Logger.setLogger(nyk.log_path,4,"Failed to get SlashDot Home Page")
            pass
        selector = etree.HTML(response.text)
        partA = selector.xpath('//main[@id="site-content"]/div/div[2]/div[2]/div[1]/div/article')
        partB = selector.xpath('//main[@id="site-content"]/div/div[2]/div[2]/div[1]/div/ul/li')

        for part in partA:
            item = dict()
            item['title'] = self.xpath_out(part.xpath('a[2]/div/h2/text()'))
            item['link'] = self.xpath_out(part.xpath('a[2]/@href'))
            item['image'] = self.xpath_out(part.xpath('a[1]/figure/img/@src'))
            item['intro'] = self.xpath_out(part.xpath('a[2]/div/span/text()'))
            yield item

        for part in partB:
            item = dict()
            item['title'] = self.xpath_out(part.xpath('a/div/h1/text()'))
            item['link'] = self.xpath_out(part.xpath('a/@href'))
            item['image'] = self.xpath_out(part.xpath('a/img/@src'))
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
    sets = Pipeline(nyk.site_id, nyk.site_name).structure_set()
    Pipeline(nyk.site_id, nyk.site_name).open_spider(sets)

    for item in NewYork().first_requests():
        Pipeline(nyk.site_id, nyk.site_name).process_item(item)
        Pipeline(nyk.site_id, nyk.site_name).upload_item(item, sets)

    try:
        Pipeline(nyk.site_id, nyk.site_name).close_spider()
    except:
        Logger().setLogger(nyk.log_path, 4, "Failed to close spider,db_session may failed")

if __name__ == '__main__':
    run()