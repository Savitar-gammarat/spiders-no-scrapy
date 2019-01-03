#coding:utf-8
import sys
sys.path.append("..")
from config import DoubanConfig as do
from logger import Logger

from sina import Sina
from pipelines import SinaPipeline

def run():
    sets = SinaPipeline().structure_set()
    SinaPipeline().open_spider(sets)

    for item in Sina().first_requests():
        SinaPipeline().process_item(item)
        SinaPipeline().upload_item(item, sets)

    try:
        SinaPipeline().close_spider()
    except:
        Logger().setLogger(do.log_path, 2, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    run()
