#coding:utf-8
import sys
sys.path.append("..")
from config import TencentConfig as tc
from logger import Logger

from zhihu import Zhihu
from pipelines import ZhihuPipeline

def run():
    sets = ZhihuPipeline().structure_set()

    ZhihuPipeline().open_spider(sets)

    for item in Zhihu().first_requests():
        ZhihuPipeline().process_item(item)

        ZhihuPipeline().upload_item(item, sets)

    try:
        ZhihuPipeline().close_spider()
    except:
        Logger().setLogger(tc.log_path, 2, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    run()

