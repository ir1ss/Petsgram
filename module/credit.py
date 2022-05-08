# credit表模型
import time
from flask import session
from sqlalchemy import Table
from common.database import dbconnect

# 把common中定义的数据库连接实例导入
dbsession, md, DBase = dbconnect()

class Credit(DBase):
    __table__ = Table('credit', md, autoload=True)

    # 积分变化详细记录
    def insert_detail(self, type, target, credit, userid):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        credit = Credit(userid=userid, category=type, target=target, credit=credit, createTime=now, updateTime=now)
        dbsession.add(credit)
        dbsession.commit()

    # 判断用户之前是否已经在articleid号文章上消耗过积分
    def check_payed_article(self, articleid, userid):
        result = dbsession.query(Credit).filter(Credit.userid==userid, Credit.target==articleid, Credit.category=="阅读文章").count()
        return result == 1