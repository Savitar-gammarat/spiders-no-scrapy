#coding:utf-8
import datetime

class ORM(object):
    # #服务器
    # username = 'hao'
    # password = '991004'
    # host = '47.101.196.53'
    # port = '3306'
    # database = 'techurls'

    #本机
    username = 'root'
    password = ''
    host = 'localhost'
    port = '3306'
    database = 'techurls'


    today = str(datetime.date.today())

class ZhihuConfig(object):
    site_id = 1
    site_name = '知乎'
    log_path = "../log/zhihu/zhihu-" + ORM().today + ".txt"

class TencentConfig(object):
    site_id = 2
    site_name = '腾讯'
    log_path = "../log/tencent/tencent-" + ORM().today + ".txt"

class DoubanConfig(object):
    site_id = 3
    site_name = '豆瓣'
    log_path = "../log/douban/douban-" + ORM().today + ".txt"

class SinaConfig(object):
    site_id = 4
    site_name = '新浪'
    log_path = "../log/sina/sina-" + ORM().today + ".txt"

class TiebaConfig(object):
    site_id = 5
    site_name = '百度贴吧'
    log_path = "../log/tieba/tieba-" + ORM().today + ".txt"
