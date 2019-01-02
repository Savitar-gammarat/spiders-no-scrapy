#coding:utf-8
import requests
from lxml import etree
import re
import json
import chardet

class Tencent(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
    }
    A_urls = []   #A类详情页面的url列表
    B_urls = []   #B类详情页面的url列表,B类需要通过js获取详情页信息，且B类中又有两类
    pattern_a = re.compile(r'.*?news.qq.com/a.*?',re.S)
    pattern_b = re.compile(r'.*?new.qq.com/omn.*?',re.S)

    def first_requests(self):
        print("first")
        selector = etree.HTML(requests.get("https://www.qq.com/", headers=self.headers).content)
        uls = selector.xpath('//*[@id="tab-news-01"]/ul')
        for ul in uls:
            lis = ul.xpath('li')
            for li in lis:
                hrefs = li.xpath('a/@href')
                for href in hrefs:
                    if re.match(self.pattern_a, href):
                        self.A_urls.append(href)
                    elif re.match(self.pattern_b, href):
                        self.B_urls.append(href)
                    else:
                        pass

    def second_requests(self):
        print("second")
        for url in self.A_urls:
            item = dict()
            selector = etree.HTML(requests.get(url, headers=self.headers).content)
            item['link'] = url
            item['title'] = selector.xpath('//*[@id="Main-Article-QQ"]/div/div[1]/div[1]/div[1]/h1/text()')[0]
            item['image'] = None
            # item['catalog'] = selector.xpath('//*[@id="Main-Article-QQ"]/div/div[1]/div[1]/div[1]/div/div[1]/span[1]/text()')[0]   #新闻类目，可留可去
            item['datetime'] = selector.xpath('//*[@id="Main-Article-QQ"]/div/div[1]/div[1]/div[1]/div/div[1]/span[3]/text()')[0]

            yield item

        for url in self.B_urls:
            response = requests.get(url, headers=self.headers)
            selector = etree.HTML(response.text)
            data = selector.xpath('/html/head/script[5]/text()')
            if data:
                item = dict()
                data = json.loads(data[0].strip()[14:])
                item['link'] = url
                item['title'] = data['title']
                item['datetime'] = data['pubtime']
                item['image'] = None
                yield item
            else:
                self.third_requests(url)

    def third_requests(self, url):
        content_api = 'https://openapi.inews.qq.com/getQQNewsNormalContent'   #腾讯异步请求新闻内容的url
        pattern_id = re.compile(r'.*?/([\s\w]*)$', re.S)
        headers = {
            'referer': url,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
        }
        params = {
            'id': re.match(pattern_id, url).group(1),
            'chlid': 'news_rss',
            'refer': 'mobilewwwqqcom',
            'otype': 'jsonp',
            'ext_data': 'all',
            'srcfrom': 'newsapp',
            'callback': 'getNewsContentOnlyOutput'
        }

        response = requests.get(content_api, headers=headers, params=params)
        data = eval("'" + response.content.decode('ascii') + "'")

        pattern_item = re.compile(r'.*?"title":"(.*?)",.*?"img":{"imgurl":"(.*?)",.*?"pubtime":"(.*?)",.*?$',re.S)
        info = re.match(pattern_item, data).group(1,2,3)
        item = dict()
        item['link'] = url
        item['title'] = info[0]
        item['image'] = info[1].replace("\\","/").replace("//","/")         #最终图片url解码失败，，，，，
        item['datetime'] = info[2]
        if item['title'] is not None:
            yield item
        else:
            print("title为空")
