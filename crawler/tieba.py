#coding:utf-8
import sys
sys.path.append("..")
from config import TiebaConfig as tb
from logger import Logger
from pipelines import Pipeline

import requests
import json

class Tieba(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
    }

    def first_requests(self):
        try:
            response = requests.get('http://tieba.baidu.com/hottopic/browse/topicList',headers=self.headers,timeout=5)
        except:
            Logger().setLogger(tb.log_path, 4, "Failed to get detail_page_urls")
            pass
        topics = json.loads(response.content.decode('utf8'))['data']['bang_topic']['topic_list']
        for topic in topics:
            item = dict()
            item['intro'] = topic['abstract']
            item['title'] = topic['topic_name']
            item['link'] = topic['topic_url'].replace("&amp;", "&")
            item['image'] = topic['topic_pic']
            item['hot'] = topic['discuss_num']

            item['hot'] = float(round(int(item['hot']) / 10000, 2))
            yield item


def run():
    sets = Pipeline(tb.site_id, tb.site_name).structure_set()
    Pipeline(tb.site_id, tb.site_name).open_spider(sets)

    for item in Tieba().first_requests():
        Pipeline(tb.site_id, tb.site_name).process_item(item)
        Pipeline(tb.site_id, tb.site_name).upload_item(item, sets)

    try:
        Pipeline(tb.site_id, tb.site_name).close_spider()
    except:
        Logger().setLogger(tb.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':

    run()