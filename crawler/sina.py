#coding:utf-8
import sys
sys.path.append("..")
from config import SinaConfig as sina
from logger import Logger
from pipelines import Pipeline

import requests
import datetime
import json
import time
from pprint import pprint


class Sina(object):
    headers = {
        'Host': 'top.news.sina.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
    }
    params = {
        'top_type': 'day',
        'top_cat': 'www_www_all_suda_suda',
        'top_show_num': '10',
        'top_order': 'DESC'
    }

    def first_requests(self):
        self.params['top_time'] = str(datetime.date.today()).replace("-","")
        try:
            response = requests.get('http://top.news.sina.com.cn/ws/GetTopDataList.php',headers=self.headers,params=self.params)
        except:
            Logger().setLogger(sina.log_path, 4, "Failed to get detail_page_urls")
            pass


        data = json.loads(response.content[10:-2].decode('utf8'))['data']
        for news in data:
            item = dict()
            item['title'] = news['title']
            item['link'] = news['url']
            item['datetime'] = time.strptime(news['time'][:-6], '%a, %d %b %Y %H:%M:%S')
            item['datetime'] = time.strftime('%Y-%m-%d %H:%M:%S', item['datetime'])
            item['image'] = news['ext3']

            yield item


def run():

    sets = Pipeline(sina.site_id, sina.site_name).structure_set()
    Pipeline(sina.site_id, sina.site_name).open_spider(sets)

    for item in Sina().first_requests():
        Pipeline(sina.site_id, sina.site_name).process_item(item)
        Pipeline(sina.site_id, sina.site_name).upload_item(item, sets)

    try:
        Pipeline(sina.site_id, sina.site_name).close_spider()
    except:
        Logger().setLogger(sina.log_path, 2, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    # sina.log_path = "../" + sina.log_path
    run()
