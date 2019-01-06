#coding:utf-8
import sys
sys.path.append("..")
from config import SlashDotConfig as sd
from logger import Logger
from pipelines import Pipeline

import requests
from lxml import etree
from datetime import datetime


class SlashDot(object):
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
            response = requests.get('https://slashdot.org/',headers=self.headers,proxies=self.proxies)
        except:
            Logger.setLogger(sd.log_path,4,"Failed to get SlashDot Home Page")
            pass

        selector = etree.HTML(response.text)
        part = selector.xpath('//div[@id="firehoselist"]/article')
        for article in part:
            item = dict()
            item['title'] = self.xpath_out(article.xpath('header/h2/span[1]/a/text()'))
            item['link'] = self.xpath_out(article.xpath('header/h2/span[1]/a/@href'))
            item['datetime'] = self.xpath_out(article.xpath('header/div[@class="details"]/span[2]/time/text()')).replace("@","")
            item['intro'] = self.xpath_out(article.xpath('div[@class="body"]/div/i/text()'))
            yield item

    def process_item(self,item):
        item['datetime'] = str(datetime.strptime(item['datetime'], 'on %A %B %d, %Y %I:%M%p'))
        return item

    def xpath_out(self, list):
        if list == []:
            str = None
        elif list == None:
            str = None
        else:
            str = list[0].encode('utf8').decode('utf8')
        return str

def run():
    sets = Pipeline(sd.site_id, sd.site_name).structure_set()
    Pipeline(sd.site_id, sd.site_name).open_spider(sets)

    for item in SlashDot().first_requests():
        SlashDot().process_item(item)
        Pipeline(sd.site_id, sd.site_name).process_item(item)
        Pipeline(sd.site_id, sd.site_name).upload_item(item, sets)

    try:
        Pipeline(sd.site_id, sd.site_name).close_spider()
    except:
        Logger().setLogger(sd.log_path, 4, "Failed to close spider,db_session may failed")


if __name__ == '__main__':
    run()
