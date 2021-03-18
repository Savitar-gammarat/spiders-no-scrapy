#coding:utf-8
import sys
sys.path.append("..")
from config import ZhihuConfig as zh
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
from lxml import etree

class Zhihu(object):
    url = 'https://www.zhihu.com/hot'
    cookies = {
      '_xsrf': '0c19205a-c20b-43f6-94ad-85911e870a22',
      '_zap': 'cf241d44-8efb-44a5-8088-e8e6a63d13e2',
      'captcha_session_v2': '"2|1:0|10:1616031511|18:captcha_session_v2|88:NkNwT1lGN3pRODJtNGk2QitCMTBHVmo3V1N5Rnl3ekszemVkcGZQMlBteFhUQkkyQnZBcWtSR2Q2Y3gvYStLeg==|baf79a838936951889e11cffbf9c41dc2a08b015237ea3dbc6327c3139dc3dcf"',
      'captcha_ticket_v2': '"2|1:0|10:1616031527|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfdmxZVHBLQjV6YmFJbHRKQUpMT3RPODVpU2huZ181bE5KVXlGWHFwTG1SRGVQMTV0LVY5Wk1ZYkxrRmdoT2Z5dFdpanUuWDdJWWRqWmRsVXJIUUt1Yy5KNjAybjBNbDViS3B2bXVZUEtNY2dtVXVHbG9IWmlHR1B2WUkwUkliS3JxcnBKX0pRZXZJQnJlNnJMQ0xvMkl2NE8wcGJtajg5TEJlOS5mSHNMRUtiYkhqcnkySlQ0WDJmYnBrYVE5R1VYVi5yWndFdTR3TXZ2dS44RUNjbF9sVnc3WVF3VnZMVVNBak0yRVJhWXFmSW9MLXJ3SmRTeHcxRWdNWEw4ZUU1dDU0QnlXZzRzNWJ5UlktbEltV1BGMk1uSENnRkpHQWltQ19QVnZXRnBibGNiNnIySmo2dFVtSFNfVS1BWFl2SUcyeGhLa0dOTFMxUXJFeVBPUGx3WHRsUE82WnQyZzlCWDZELUdhenpyNWJjb0gxME0xdVdqd1I3eVNiaVFNUEI4a3V2d0JRaFVsamEuZzluZG13X09SOW1wUlZQWkFfcGcuSmZTR19EVW11dWlZelEwdG5MOWN4ZE5SaGlfZFFudGp2SG5wSktSdUhDRkFrT2JYd29rMDE5NDRsSTY3dEhUVElfT3NFUExaSUdCWTExYk1EZlFuemo3YjFJMyJ9|b0e9edcb9ccfd5bd8b90348d654032d864a02b75858b23cac7ba6d03924e3bb1"',
      'Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49': '1616031531',
      'Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49': '1615100955,1615101808,1615457275,1616031512',
      'tshl': '',
      'tst': 'h',
      'z_c0': '"2|1:0|10:1616031528|4:z_c0|92:Mi4xdnFmTEF3QUFBQUFBOEZoaEdSMThFaVlBQUFCZ0FsVk5LUDBfWVFBakFOSmt5akFxSlluZ2tENkpsaUVWWm1TNFZB|a72cfc7d08f02bf617f93e9ffaff4f2fdba23698e723ff472c7921daeb57e561"'
    }

    def first_requests(self):
        response = Req(url=self.url,cookies=self.cookies).get_select()
        selector = etree.HTML(response.text)
        sections = selector.xpath('//*[@class="HotList-list"]//section')

        for section in sections:
            item = dict()
            item['title'] = xpath_out(section.xpath('div[2]/a/h2/text()'))
            item['link'] = xpath_out(section.xpath('div[2]/a/@href'))
            item['hot'] = float(xpath_out(section.xpath('div[2]/div/text()'))[:-3])


            if item['title'] is not None:
                if item['hot'] <= 150:
                    item['home'] = False

                yield item
            else:
                Logger().setLogger(zh.log_path, 2, "Item's title is None, item is " + item)
                pass

def run():
    sets = Pipeline(zh.site_id, zh.site_name).structure_set()

    Pipeline(zh.site_id, zh.site_name).open_spider(sets)
    for item in Zhihu().first_requests():
        Pipeline(zh.site_id, zh.site_name).process_item(item)

        Pipeline(zh.site_id, zh.site_name).upload_item(item, sets)

    try:
        Pipeline(zh.site_id, zh.site_name).close_spider()
    except:
        Logger().setLogger(zh.log_path, 2, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    # zh.log_path = "../" + zh.log_path
    run()
