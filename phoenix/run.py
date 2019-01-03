#coding:utf-8
import sys
sys.path.append("..")
from config import DoubanConfig as do
from logger import Logger

from phoenix import Phoenix
from pipelines import PhoenixPipeline

def run():
    sets = PhoenixPipeline().structure_set()
    PhoenixPipeline().open_spider(sets)

    for item in Phoenix().first_requests():
        PhoenixPipeline().process_item(item)
        PhoenixPipeline().upload_item(item, sets)

    try:
        PhoenixPipeline().close_spider()
    except:
        Logger().setLogger(do.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    run()
