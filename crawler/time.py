#coding:utf-8
import sys
sys.path.append("..")
from config import TimeConfig as time
from logger import Logger
from pipelines import Pipeline

import requests
from lxml import etree

class Time(object):
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
            response = requests.get('http://time.com/',headers=self.headers,proxies=self.proxies)
        except:
            Logger.setLogger(time.log_path,4,"Failed to get SlashDot Home Page")
            pass
        selector = etree.HTML(response.text)
        partA = selector.xpath('//div[@class="column text-align-left visible-desktop visible-mobile last-column"]/div[@class="column-tout  "]')
        partB = selector.xpath('//div[@class="column text-align-left visible-desktop"]/div[@class="column-tout  "]')

        for part in partA:
            item = dict()
            item['title'] = self.xpath_out(part.xpath('div[@class="column-tout-info "]/div/div/a/text()')).strip()
            item['link'] = "time.com" + self.xpath_out(part.xpath('div[@class="column-tout-info "]/div/div/a/@href'))
            yield item

        for part in partB:
            item = dict()
            item['title'] = self.xpath_out(part.xpath('div[@class="column-tout-info "]/div/div[1]/a/text()')).strip()
            item['link'] = "time.com" + self.xpath_out(part.xpath('div[@class="column-tout-info "]/div/div[1]/a/@href'))
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
