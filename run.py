#coding:utf-8
import sys
sys.path.append("..")
from config import MainConfig as m
from logger import Logger

from crawler import zhihu,tencent,douban,sina,tieba,phoenix,netease

def go(className):
    try:
        className.run()
    except:
        Logger.setLogger(m.log_path, 4,className + " Spider Failed")


if __name__ == '__main__':

    def run():
        go(zhihu)
        go(tencent)
        go(douban)
        go(sina)
        go(tieba)
        go(phoenix)
        go(netease)

    run()


        # try:
        #     zhihu.run()
        # except:
        #     Logger.setLogger(m.log_path, 4, "Zhihu Spider Failed")
        #
        # try:
        #     tencent.run()
        # except:
        #     Logger.setLogger(m.log_path, 4, "Tencent Spider Failed")
        #
        # try:
        #     douban.run()
        # except:
        #     Logger.setLogger(m.log_path,4,"Douban Spider Failed")
        #
        # try:
        #     sina.run()
        # except:
        #     Logger.setLogger(m.log_path, 4, "Sina Spider Failed")
        #
        # try:
        #     tieba.run()
        # except:
        #     Logger.setLogger(m.log_path, 4, "Tieba Spider Failed")
        #
        # try:
        #     phoenix.run()
        # except:
        #     Logger.setLogger(m.log_path, 4, "Phoenix Spider Failed")
        #
        # try:
        #     netease.run()
        # except:
        #     Logger.setLogger(m.log_path,4,"Netease Spider Failed")

