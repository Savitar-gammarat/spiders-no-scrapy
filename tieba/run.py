#coding:utf-8
import sys
sys.path.append("..")
from config import DoubanConfig as do
from logger import Logger

from tieba import Tieba
from pipelines import TiebaPipeline

def run():
    sets = TiebaPipeline().structure_set()
    TiebaPipeline().open_spider(sets)

    for item in Tieba().first_requests():
        TiebaPipeline().process_item(item)
        TiebaPipeline().upload_item(item, sets)

    try:
        TiebaPipeline().close_spider()
    except:
        Logger().setLogger(do.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    run()
