#coding:utf-8
import sys
sys.path.append("..")
from config import NeteaseConfig as ne
from logger import Logger

from netease import Netease
from pipelines import NeteasePipeline

def run():
    sets = NeteasePipeline().structure_set()
    NeteasePipeline().open_spider(sets)

    detail_url = Netease().first_requests()

    for item in Netease().second_requests(detail_url):
        NeteasePipeline().process_item(item)
        NeteasePipeline().upload_item(item, sets)

    try:
        NeteasePipeline().close_spider()
    except:
        Logger().setLogger(ne.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    run()
