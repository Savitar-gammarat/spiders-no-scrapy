from sqlalchemy import Table,MetaData,Column,Integer,Float,String,Text,TIMESTAMP,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session,sessionmaker,relationship
from sqlalchemy.schema import ForeignKey
import pymysql
from config import ORM as orm
import datetime

#设置一系列的基本参数
Base = declarative_base()
# DB_CONNECT_STR = "mysql+pymysql://root:@localhost:3306/techurls?charset=utf8"
DB_CONNECT_STR = "mysql+pymysql://" + orm.username + ":" + orm.password + "@" + orm.host + ":" + orm.port + "/" + orm.database + "?charset=utf8"
engine = create_engine(DB_CONNECT_STR,encoding="utf8",convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


#创建news于keyword多对多关系的中间表
news_keyword = Table('news_keyword', Base.metadata,              #news表与keyword表的中间表
    Column('news_id', Integer, ForeignKey('news.id')),
    Column('keyword_id', Integer, ForeignKey('keyword.id'))
)

#news表
class News(Base):
    __tablename__ = 'news'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String(255),nullable=False)
    link = Column(String(255),nullable=False)
    hot = Column(Float,nullable=False)
    image = Column(String(255),nullable=True)
    intro = Column(Text(),nullable=True)
    datetime = Column(TIMESTAMP(),nullable=False,default=datetime.datetime.now)
#创建pass字段用作占位
    pass1 = Column(String(255),nullable=True)
    pass2 = Column(String(255),nullable=True)
    pass3 = Column(String(255),nullable=True)

    site_id = Column(Integer,ForeignKey('site.id'))   #设置与site表的外键
    keywords = relationship('Keyword',secondary=news_keyword)   #与中间表相关联

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.title)   #调试函数


#创建站点site表
class Site(Base):
    __tablename__ = 'site'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer,autoincrement=True,primary_key=True,index=True)
    name = Column(String(25),nullable=False)
    pageviews = Column(Integer,nullable=True)
#创建pass字段用作占位
    pass1 = Column(String(255),nullable=True)
    pass2 = Column(String(255),nullable=True)
    site_news = relationship('News', backref='site')  #创建站点与新闻表之间的一对多关系


#创建关键词keyword表
class Keyword(Base):
    __tablename__ = 'keyword'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    keyword = Column(String(27),nullable=False)
    datetime = Column(TIMESTAMP(),nullable=False,default=datetime.datetime.now)
#创建pass字段用作占位
    pass1 = Column(String(255),nullable=True)
    pass2 = Column(String(255),nullable=True)
    key_news = relationship('News', secondary=news_keyword)  #创建与中间表相关联的字段


#创建全部表的主函数
def main():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    main()
# def main():
#     new_site = Site(
#         id = 1,
#         name = "ZhiHu"
#     )
#     db_session.add(new_site)
#     db_session.commit()
#     db_session.close()
#
# if __name__ == '__main__':
#     main()
