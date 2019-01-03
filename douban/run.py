#coding:utf-8
import sys
sys.path.append("..")
from config import DoubanConfig as do
from logger import Logger

from douban import Douban
from pipelines import DoubanPipeline

def run():
    sets = DoubanPipeline().structure_set()
    DoubanPipeline().open_spider(sets)

    for item in Douban().first_requests():
        DoubanPipeline().process_item(item)
        DoubanPipeline().upload_item(item, sets)

    try:
        DoubanPipeline().close_spider()
    except:
        Logger().setLogger(do.log_path, 2, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    run()
