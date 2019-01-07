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
        '__gads': 'ID=c1b7ae0b44cdeeb3:T=1546405453:S=ALNI_Ma4zMry1JckKBAY7AkjlXbU6WRwJA',
        '_xsrf': 'JS3T6GXK1wUq3kSYvYFJ1EdpaQzRhe0e',
        '_zap': '10c352d7-2974-456b-aec1-e89fe25f89b9',
        'capsion_ticket': '"2|1:0|10:1546701733|14:capsion_ticket|44:NGFmNjA0NmZkNzQ5NDYzMDg1MGU4NGQ5MjE5Y2YzZDM=|df943ad7863973082166379dec95484fa6e9566031ecb3f5c6005ff7eb1edf48"',
        'd_c0': '"AJAiAChQww6PToldl6bxp2jBM2owBEdBSz0=|1546405409"',
        'q_c1': '57ab6b634b034b66aac04f4583108a0f|1546405410000|1546405410000',
        'tgw_l7_route': '7bacb9af7224ed68945ce419f4dea76d',
        'tgw_l7_route': 'ec452307db92a7f0fdb158e41da8e5d8',
        'tgw_l7_route': 'f2979fdd289e2265b2f12e4f4a478330',
        'tst': 'h',
        'z_c0': '"2|1:0|10:1546701739|4:z_c0|92:Mi4xdnFmTEF3QUFBQUFBa0NJQUtGREREaVlBQUFCZ0FsVk5xeGtlWFFER0F6bXc3cEtNWXNfWTZqdXUyYXRWMkNBODZn|29694964a87f58525a170502516c109e9f43f36662c2d0efcf078ebb247dee1b"'
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
                if item['hot'] >= 150:
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