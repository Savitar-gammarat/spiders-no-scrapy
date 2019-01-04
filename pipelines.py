#coding:utf-8
import sys
sys.path.append("..")
import alchemy as db
from config import PipelineConfig as ne
from logger import Logger

import jieba


class Pipeline(object):

    column_set = ["title", "link", "hot", "image", "intro", "datetime", "site_id", "jieba"]  # 对进入pipelines的item进行格式化处理的column名

    def __init__(self, site_id, site_name):

        self.site_id = site_id
        self.site_name = site_name



    def orm_sort(self, dict):
        set_out = []
        for i in dict:
            set_out.append(i[0])
        set_out = set(set_out)

        return set_out

    def structure_set(self):
        container = dict()
        try:
            container['site_set'] = db.db_session.query(db.Site).filter(db.Site.id == self.site_id).all()
            container['key_set'] = self.orm_sort(db.db_session.query(db.Keyword.keyword).all())
            container['news_set'] = self.orm_sort(db.db_session.query(db.News.link).filter(db.News.site_id == self.site_id).all())
            container['set_notsql'] = {}

            return container
        except:
            print("Structure sets failed")
            Logger().setLogger(ne.log_path, 2, "Pipelines, Failed to structure set")
            pass

    def open_spider(self, structure):
        try:
            if structure['site_set']:  # 判断该站点是否已经建立在site表内，如未建立则创建之，id须从settings内提前设置正确
                pass
                # self.site_id = db.db_session.query(db.Site.id).filter(db.Site.name == self.site_name).first()[0]
            else:
                new_site = db.Site(  # 创建新的site对象，并尝试插入到site表
                    id=self.site_id,
                    name=self.site_name
                )
                try:
                    db.db_session.add(new_site)
                    db.db_session.commit()
                    print("成功插入site信息")
                except:
                    print("Failed to insert site")
                    pass
            print("Succeed open spider")
        except:
            print("Open spider failed")
            Logger().setLogger(ne.log_path, 3, "Failed to open spider(site info may not be inserted")
            pass

    def organ_item(self, key, item):
        if key in item.keys():
            pass
        else:
            item[key] = None
        return item

    def process_item(self, item):

        item['site_id'] = self.site_id
        # item['hot'] = float(round(int(item['hot'])/10000,2))

        try:   #尝试对title进行中文分词操作
            item['jieba'] = list(jieba.cut_for_search(item['title']))
            print("jieba Succeed")
        except:
            Logger().setLogger(ne.log_path, 2,"Pipelines, Failed to process item,So no jieba or site_id,may cause error,url is")
            item['jieba'] = None


        for column in self.column_set:
            self.organ_item(column, item)

        return item

    def upload_item(self, item, structure):

        try:
            if item['jieba'] is None:   #如果item['jieba']为空则表示jieba分词失败
                print("JieBa failed so no item['jieba']")
                pass
            else:
                key_list = []
                for i in item['jieba']:  #遍历item['jieba']内的每个词项
                    if i is None:
                        pass
                    elif i in structure['key_set']:  #如果该词汇已经存在于set内则查询到对象并添加到key_list内

                        if i in structure['set_notsql'].keys():    #获取存在于set但不存在于数据库内的词汇orm对象
                            key_list.append(structure['set_notsql'][i])
                        else:   #获取存在于set与数据库内的词汇orm对象
                            x = db.db_session.query(db.Keyword).filter(db.Keyword.keyword == i).first()   #注意此处应为db.Keyword以获取对象！！！是ORM对象！
                            key_list.append(x)

                    else:  #如果该词不存在于set内则创建SQLAlchemy对象并插入之，在添加到key_list与set_notsql内

                        new_keyword = db.Keyword(
                            keyword = i
                        )
                        try:
                            db.db_session.add(new_keyword)
                        except Exception:
                            print("Failed to insert keyword")

                        #对变量进行更新
                        structure['key_set'].add(i)
                        structure['set_notsql'][i] = new_keyword

                        #插入到该item下收集所有对应keyword的列表
                        key_list.append(new_keyword)

            print("Succeed add keywords")

            if item['title'] is not None:  #判断如果item['title']不为空则执行插入操作
                if item['link'] in structure['news_set']:  #如果该link已经存在于数据表内则尝试对热度hot进行更新操作
                    pass
                else:      #创建SQLAlchemy中news对象并尝试插入到表
                    self.insert_new(item, key_list)
            print("Upload Succeed")
        except:
            Logger().setLogger(ne.log_path, 2, "Pipelines, Failed to upload item,url is" + item['link'])
            pass

    def insert_new(self, item, key_list):
        new_news = db.News(
            link=item['link'],
            title=item['title'],
            hot=item['hot'],
            image=item['image'],
            intro=item['intro'],
            site_id=item['site_id'],
            datetime=item['datetime']
        )
        new_news.keywords = key_list  # 建立每个news和与他相关的keyword的关系
        try:
            db.db_session.add(new_news)
        except Exception:
            Logger().setLogger(ne.log_path, 4, "Failed to insert new news,url is " + item['link'])
            pass

    def close_spider(self):
        try:
            db.db_session.commit()
            db.db_session.close()
            print("Spider Finished")
        except:
            print("Close spider failed")
            Logger().setLogger(ne.log_path, 4, "Failed to commit or close db_session")