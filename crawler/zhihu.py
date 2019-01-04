#coding:utf-8
import sys
sys.path.append("..")
from config import ZhihuConfig as zh
from logger import Logger
from pipelines import Pipeline

import requests
from lxml import etree

class Zhihu(object):
    name = 'zhihu'
    headers = {
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/hot/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    cookies = {
        '1P_JAR': '2019-01-01-11',
        '__gads': 'ID=c1b7ae0b44cdeeb3:T=1546405453:S=ALNI_Ma4zMry1JckKBAY7AkjlXbU6WRwJA',
        '_xsrf': '528033c1-c407-4ab5-aa75-0830734e3c7f',
        '_zap': '10c352d7-2974-456b-aec1-e89fe25f89b9',
        'a': 'V4Weg0Fqh0sA',
        'capsion_ticket': '"2|1:0|10:1546405405|14:capsion_ticket|44:YzZkMmVmZTk5ZTlkNGMyZThmNjllN2E4YWNjNmI3MmU=|7e99c0e8279e4fa5ccad4dd2fa95b0d00e5e531b864cdfaf858b9b055bddc676"',
        'd_c0': '"AJAiAChQww6PToldl6bxp2jBM2owBEdBSz0=|1546405409"',
        'dk': '2108979_2109816_2108142',
        'id': '22b97fce04ae00ed||t=1546405454|et=730|cs=002213fd48ee5cfd328a775724',
        'q_c1': '57ab6b634b034b66aac04f4583108a0f|1546405410000|1546405410000',
        'syn': '1_f5fd4db4_5c2c4624_5c2c4624_1',
        'tgw_l7_route': '69f52e0ac392bb43ffb22fc18a173ee6',
        'tgw_l7_route': '931b604f0432b1e60014973b6cd4c7bc',
        'tgw_l7_route': '170010e948f1b2a2d4c7f3737c85e98c',
        'tsc': '3_5c2c1ed7_5c2c464d_0_9',
        'tst': 'r',
        'z_c0': '"2|1:0|10:1546405409|4:z_c0|92:Mi4xdnFmTEF3QUFBQUFBb0tLZEcxREREaVlBQUFCZ0FsVk5JWlFaWFFERGZrd2VmVHJCTWVyOUtkS2dRX1FyZllfeENR|cc28e2b32030191a9c3e60a2843d941dcb7a790beb715252aca8cf16f0f4dd70"'
    }

    def first_requests(self):
        response = requests.get('https://www.zhihu.com/hot',headers=self.headers,cookies=self.cookies,allow_redirects=False,timeout=5)
        selector = etree.HTML(response.content)
        sections = selector.xpath('//*[@id="TopstoryContent"]/div/section')

        for section in sections:
            item = dict()
            item['title'] = self.get_out(section.xpath('div[2]/a/h2/text()'))
            item['link'] = self.get_out(section.xpath('div[2]/a/@href'))
            item['intro'] = self.get_out(section.xpath('div[2]/a/p/text()'))
            item['hot'] = float(self.get_out(section.xpath('div[2]/div/text()'))[:-3])
            item['image'] = self.get_out(section.xpath('a/img/@src'))
            if item['title'] is not None:
                yield item
            else:
                Logger().setLogger(zh.log_path, 2, "One item's title is None")
                pass

    def get_out(self, list):
        if list == []:
            str = None
        elif list == None:
            str = None
        else:
            str = list[0]
        return str

def run():
    sets = Pipeline(zh.site_id, zh.site_name).structure_set()

    Pipeline(zh.site_id, zh.site_name).open_spider(sets)

    for item in Zhihu().first_requests():
        Pipeline(zh.site_id, zh.site_name).process_item(item)

        Pipeline(zh.site_id, zh.site_name).upload_item(item, sets)

    try:
        Pipeline(zh.site_id, zh.site_name).close_spider()
    except:
        Logger().setLogger(zh.log_path, 2, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':

    run()