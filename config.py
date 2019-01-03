#coding:utf-8
class ORM(object):
    username = 'root'
    password = ''
    host = 'localhost'
    port = '3306'
    database = 'techurls'

class ZhihuConfig(object):
    site_id = 1
    site_name = 'Zhihu'
    log_path = "../log/zhihu.txt"

class TencentConfig(object):
    site_id = 2
    site_name = 'Tencent'
    log_path = "../log/tencent.txt"
