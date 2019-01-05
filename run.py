#coding:utf-8
import sys
sys.path.append("..")
from config import MainConfig as m
from logger import Logger

from crawler import zhihu,tencent,douban,sina,tieba,phoenix,netease,huanqiu,xinhua,donews,souhu,bbc,slashdot,wired,time,newyork

def go(className):
    try:
        className.run()
    except:
        Logger.setLogger(m.log_path, 4,className + " Spider Failed")

def run():
    go(zhihu)
    go(tencent)
    go(douban)
    go(sina)
    go(tieba)
    go(phoenix)
    go(netease)
    go(huanqiu)
    go(xinhua)
    go(donews)
    go(souhu)
    go(bbc)
    go(slashdot)
    go(wired)
    go(time)
    go(newyork)

if __name__ == '__main__':
    run()

