#coding:utf-8
import sys
sys.path.append("..")
from config import TencentConfig as tc
from logger import Logger

from tencent import Tencent
from pipelines import TencentPipeline

def run():
    sets = TencentPipeline().structure_set()
    TencentPipeline().open_spider(sets)
    Tencent().first_requests()

    for item in Tencent().second_requests():

        TencentPipeline().process_item(item)
        TencentPipeline().upload_item(item, sets)

    try:
        TencentPipeline().close_spider()
    except:
        Logger().setLogger(tc.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    run()

