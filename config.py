#coding:utf-8
import datetime

class ORM(object):
    #服务器
    username = 'hao'
    password = '991004'
    host = '47.101.196.53'
    port = '3306'
    database = 'techurls'

    # #本机
    # username = 'root'
    # password = ''
    # host = 'localhost'
    # port = '3306'
    # database = 'techurls'

    today = str(datetime.date.today())

class MainConfig(object):
    log_path = "../log/main-" + ORM().today + ".txt"


class PipelineConfig(object):
    log_path = "../log/pipeline-" + ORM().today + ".txt"


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


class PhoenixConfig(object):
    site_id = 6
    site_name = '凤凰网'
    log_path = "../log/phoenix/phoenix-" + ORM().today + ".txt"


class NeteaseConfig(object):
    site_id = 7
    site_name = '网易新闻'
    log_path = "../log/netease/netease-" + ORM().today + ".txt"


class HuanqiuConfig(object):
    site_id = 8
    site_name = '环球网'
    log_path = "../log/huanqiu/huanqiu-" + ORM().today + ".txt"


class XinHuaConfig(object):
    site_id = 9
    site_name = '新华网'
    log_path = "../log/xinhua/xinhua-" + ORM().today + ".txt"


class DoNewsConfig(object):
    site_id = 10
    site_name = 'DoNews'
    log_path = "../log/donews/donews-" + ORM().today + ".txt"


class SouHuConfig(object):
    site_id = 11
    site_name = '搜狐'
    log_path = "../log/souhu/souhu-" + ORM().today + ".txt"


class BBCConfig(object):
    site_id = 12
    site_name = 'BBC'
    log_path = "../log/bbc/bbc-" + ORM().today + ".txt"


class SlashDotConfig(object):
    site_id = 13
    site_name = 'SlashDot'
    log_path = "../log/slashdot/slashdot" + ORM().today + ".txt"


class WiredConfig(object):
    site_id = 14
    site_name = 'Wired'
    log_path = "../log/wired/wired" + ORM().today + ".txt"


class TimeConfig(object):
    site_id = 15
    site_name = 'Time'
    log_path = "../log/time/time" + ORM().today + ".txt"


class NewYorkTimeConfig(object):
    site_id = 16
    site_name = 'New York Times'
    log_path = "../log/newyork/newyork" + ORM().today + ".txt"


class EconomistConfig(object):
    site_id = 17
    site_name = 'The Economist'
    log_path = "../log/economic/economic" + ORM().today + ".txt"


class FortuneConfig(object):
    site_id = 18
    site_name = 'Fortune'
    log_path = "../log/fortune/fortune" + ORM().today + ".txt"