# favorite表模型
import time
from flask import session
from sqlalchemy import Table
from common.database import dbconnect
from module.article import Article
from module.users import Users

# 把common/database.py中定义的数据库连接实例导入
dbsession, md, DBase = dbconnect()

class Favorite(DBase):
    __table__ = Table('favorite', md, autoload=True)

    # 插入文章收藏数据
    def insert_favorite(self, articleid):
        row = dbsession.query(Favorite).filter(Favorite.articleid==articleid, Favorite.userid==session.get('userid')).first()
        article = dbsession.query(Article).filter(Article.articleid==articleid).first()
        article.likes += 1
        if row is not None:
            row.canceled = 0
        else:
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            favoriteid = dbsession.query(Favorite).count() + 1
            favorite = Favorite(favoriteid=favoriteid, articleid=articleid, userid=session.get('userid'), canceled=0, createtime=now, updatetime=now)
            dbsession.add(favorite)
        dbsession.commit()

    # 取消收藏
    def cancel_favorite(self, articleid):
        row = dbsession.query(Favorite).filter(Favorite.articleid==articleid, Favorite.userid==session.get('userid')).first()
        article = dbsession.query(Article).filter(Article.articleid==articleid).first()
        article.likes -= 1
        print(row)
        row.canceled = 1
        dbsession.commit()

    # 判断是否收藏
    def check_favorite(self, articleid):
        row = dbsession.query(Favorite).filter(Favorite.articleid==articleid, Favorite.userid==session.get('userid')).first()
        if row is None:
            return False
        elif row.canceled == 1:
            return False
        else:
            return True

    def find_user_like(self, userid):
        result = dbsession.query(Favorite, Article, Users).join(Article, Article.articleid==Favorite.articleid).join(Users, Users.userid==Article.userid).filter(Favorite.userid==userid, Favorite.canceled==0, Article.hidden==0, Article.drafted==0, Article.checked==1).order_by(Favorite.createtime.desc()).all()
        return result

