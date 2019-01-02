import sys
sys.path.append("..")
import alchemy as db
from config import TencentConfig as tc
import jieba


class TencentPipeline(object):
    site_id = tc.site_id
    site_name = tc.site_name


    def __init__(self):
        self.set_notsql = {}  # 重点，此dict用来暂时存储本次爬取过程中存在于set，但不存在于mysql的keyword以及其所对应的SQLAlchemy对象
        try:
            self.site_set = db.db_session.query(db.Site.id).filter(db.Site.name == self.site_name).all()
            self.key_set = set(db.db_session.query(db.Keyword.keyword).all())
            self.news_set = set(db.db_session.query(db.News.title).all())

        except Exception:
            print("Failed to instruct set")
            pass


    def open_spider(self):
        print("open")

        if self.site_set:  # 判断该站点是否已经建立在site表内，如未建立则创建之，id须从settings内提前设置正确
            self.site_id = db.db_session.query(db.Site.id).filter(db.Site.name == self.site_name).first()[0]
        else:
            print(self.site_set)
            new_site = db.Site(  # 创建新的site对象，并尝试插入到site表
                id=self.site_id,
                name=self.site_name
            )
            try:
                db.db_session.add(new_site)
                db.db_session.flush()  # 插入到site表后进行“刷新”操作
                db.db_session.commit()
                print("成功插入site信息")
            except Exception:
                print("Failed to insert site")
                pass

    def process_item(self, item):
        print("process")
        item['site_id'] = self.site_id
        try:   #尝试对title进行中文分词操作
            item['jieba'] = list(jieba.cut_for_search(item['title']))
        except:
            print("JieBa failed")
            item['jieba'] = None
        return item

    def upload_item(self, item):
        print("upload")
        if item['jieba'] is None:   #如果item['jieba']为空则表示jieba分词失败
            print("JieBa failed so no item['jieba']")
            pass
        else:
            key_list = []
            for i in item['jieba']:  #遍历item['jieba']内的每个词项
                if i is None:
                    pass
                elif i in self.key_set:  #如果该词汇已经存在于数据库内则查询到对象并添加到key_list内

                    if i in self.set_notsql.keys():
                        key_list.append(self.set_notsql[i])
                    else:
                        x = db.db_session.query(db.Keyword.keyword).filter(db.Keyword.keyword == i).first()
                        key_list.append(x)

                else:  #如果该词不存在于数据库内则创建SQLAlchemy对象并插入之，在添加到key_list内
                    new_keyword = db.Keyword(
                        keyword = i
                    )
                    try:
                        db.db_session.add(new_keyword)
                    except Exception:
                        print("Failed to insert keyword")

                    #对全局变量进行更新
                    self.key_set.add(i)
                    self.set_notsql[i] = new_keyword

                    #插入到该item下收集所有对应keyword的列表
                    key_list.append(new_keyword)


        if item['title'] is not None:  #判断如果item['title']不为空再进行插入操作
            if item['title'] in self.news_set:  #如果该title已经存在于数据表内则略过不再插入
                try:
                    exist_news = db.db_session.query(db.News).filter(db.News.title == item['title']).first()
                    if exist_news.site_id == self.site_id:
                        pass
                    else:
                        self.insert_new(item, key_list)
                    # exist_news.hot = item['hot']
                except Exception:
                    print("Failed to Update exist news' hot")
            else:      #创建SQLAlchemy中news对象并尝试插入到表
                self.insert_new(item, key_list)

    def insert_new(self, item, key_list):
        new_news = db.News(
            title=item['title'],
            link=item['link'],
            site_id=item['site_id'],
            image=item['image']
        )
        new_news.keywords = key_list  # 建立每个news和与他相关的keyword的关系
        try:
            db.db_session.add(new_news)
        except Exception:
            print("Failed to insert new news")

    def close_spider(self):
        print("close")
        try:
            db.db_session.commit()
            db.db_session.close()
        except Exception:
            print("Failed to commit or close db_session")
