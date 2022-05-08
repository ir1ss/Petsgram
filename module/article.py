# article表模型
import random
import time

from flask import session
from sqlalchemy import Table
from common.database import dbconnect
from module.users import Users

# 把common/database.py中定义的数据库连接实例导入
dbsession, md, DBase = dbconnect()

class Article(DBase):
    __table__ = Table('article', md, autoload=True)

    # 查询所有文章
    def find_all(self):
        result = dbsession.query(Article).all()
        return result

    # 根据id找文章
    def find_by_id(self, articleid):
        row = dbsession.query(Article, Users.username).join(Users, Users.userid==Article.userid).filter(Article.articleid == articleid, Article.hidden==0, Article.checked==1, Article.drafted==0).first()
        return row

    # 设置分页的limit和offset，同时对users和article做连接查询
    def find_limit_with_users(self, start, count):
        result = dbsession.query(Article, Users).join(Users, Users.userid == Article.userid).filter(Article.hidden==0, Article.drafted==0, Article.checked==1).order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    # 统计文章总数量
    def get_total_count(self):
        count = dbsession.query(Article).filter(Article.hidden==0, Article.drafted==0, Article.checked==1).count()
        return count

    # 统计特定种类文章的总数量
    def get_total_count_by_type(self, type):
        count = dbsession.query(Article).filter(Article.hidden==0, Article.drafted==0, Article.checked==1, Article.type==type).count()
        return count

    # 按种类查询文章
    def find_by_type(self, type, start, count):
        result = dbsession.query(Article, Users).join(Users, Users.userid == Article.userid).filter(Article.hidden==0, Article.drafted==0, Article.checked==1, Article.type==type).limit(count).offset(start).all()
        return result

    # 查询文章
    def find_by_headline(self, headline, start, count):
        result = dbsession.query(Article, Users).join(Users, Users.userid == Article.userid).filter(Article.hidden==0, Article.drafted==0, Article.checked==1, Article.headline.like('%' + headline + '%')).order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    # 查询文章数量
    def get_count_by_headline(self, headline):
        count = dbsession.query(Article, Users).join(Users, Users.userid == Article.userid).filter(Article.hidden==0, Article.drafted==0, Article.checked==1, Article.headline.like('%' + headline + '%')).count()
        return count

    # 查找最多阅读的文章
    def find_most_view(self):
        result = dbsession.query(Article.articleid, Article.headline).filter(Article.hidden==0, Article.drafted==0, Article.checked==1).order_by(Article.readcount.desc()).limit(9).all()
        return result;

    # 查找最多收藏的文章
    def find_most_likes(self):
        result = dbsession.query(Article.articleid, Article.headline).filter(Article.hidden==0, Article.drafted==0, Article.checked==1).order_by(Article.likes.desc()).limit(9).all()
        return result;

    # 查找推荐文章
    def find_recommend(self):
        result = dbsession.query(Article.articleid, Article.headline, Article.thumbnail, Article.content).filter(Article.hidden == 0, Article.drafted == 0,Article.checked == 1, Article.recommend==1).order_by(Article.articleid.desc()).limit(5).all()
        return result;

    # 打包查询最多阅读、最多收藏和推荐文章
    def find_most_view_and_like_and_recommend(self):
        view = self.find_most_view()
        likes = self.find_most_likes()
        recommend = self.find_recommend()
        return view, likes, recommend

    # 更新阅读次数
    def update_read_count(self, articleid):
        article = dbsession.query(Article).filter(Article.articleid==articleid).one()
        article.readcount += 1
        dbsession.commit()

    # 根据文章id找标题
    def find_headline_by_id(self, articleid):
        row = dbsession.query(Article.headline).filter(Article.articleid==articleid, Article.hidden==0, Article.checked==1, Article.drafted==0).first()
        return row

    # 通过id找上一篇和下一篇
    def find_prev_and_next_by_id(self, articleid):
        dict = {}
        next = dbsession.query(Article).filter(Article.hidden==0, Article.checked==1, Article.drafted==0, Article.articleid<articleid).order_by(Article.articleid.desc()).first()
        prev = dbsession.query(Article).filter(Article.hidden==0, Article.checked==1, Article.drafted==0, Article.articleid>articleid).first()
        if prev is None:
            prev_id = articleid
        else:
            prev_id = prev.articleid
        if next is None:
            next_id = articleid
        else:
            next_id = next.articleid
        prev_headline = self.find_headline_by_id(prev_id)
        next_headline = self.find_headline_by_id(next_id)
        dict['prev_id'] = prev_id
        dict['next_id'] = next_id
        dict['prev_headline'] = prev_headline[0]
        dict['next_headline'] = next_headline[0]
        return dict

    # 更新回复
    def update_replycount(self, articleid):
        row = dbsession.query(Article).filter(Article.articleid==articleid).first()
        row.replycount += 1
        dbsession.commit()

    # 新添文章
    def add_new_article(self, headline, content, type, credit, drafted, checked):
        userid = session.get('userid')
        thumbnail = str(random.randint(0,9)) + '.jpg'
        readcount = 0
        likes = 0
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        hidden = 0
        recommend = 0
        replycount = 0
        article = Article(userid=userid, type=type, headline=headline, content=content, thumbnail=thumbnail, credit=credit, readcount=readcount, likes=likes, uploadtime=now, hidden=hidden, drafted=drafted, checked=checked, recommend=recommend, replycount=replycount)
        dbsession.add(article)
        dbsession.commit()

    # 查找所有文章的数量，不限条件
    def get_all_count(self):
        result = dbsession.query(Article).count()
        return result

    # 查找给定用户发表文章的数量
    def get_user_article_num(self, userid):
        result = dbsession.query(Article).filter(Article.userid==userid, Article.hidden == 0, Article.drafted == 0).count()
        return result

    # 查找给定用户的文章
    def find_by_userid(self, userid):
        result = dbsession.query(Article).filter(Article.userid==userid, Article.hidden==0, Article.drafted==0, Article.checked==1).order_by(Article.uploadtime.desc()).all()
        return result

    # 查找用户的草稿
    def find_Drafts_by_userid(self, userid):
        result = dbsession.query(Article).filter(Article.userid==userid, Article.hidden==0, Article.drafted==1, Article.checked==1).order_by(Article.uploadtime.desc()).all()
        return result

    # 查找用户正在审核的文章
    def find_checkings(self, userid):
        result = dbsession.query(Article).filter(Article.userid==userid, Article.hidden==0, Article.drafted==0, Article.checked==0).order_by(Article.uploadtime.desc()).all()
        return result

    # 查找所有待审核的文章
    def find_checking_list(self):
        result = dbsession.query(Article).filter(Article.hidden==0, Article.drafted==0, Article.checked==0).all()
        return result

    # 通过id查找待审核的文章
    def find_checking_by_articleid(self, articleid):
        row = dbsession.query(Article).filter(Article.articleid==articleid, Article.hidden==0, Article.drafted==0, Article.checked==0).first()
        return row

    # 隐藏文章
    def hide_artilce_by_id(self, articleid):
        row = dbsession.query(Article).filter(Article.articleid==articleid).first()
        row.hidden = 1
        dbsession.commit()

    def check_artilce_by_id(self, articleid):
        row = dbsession.query(Article).filter(Article.articleid==articleid).first()
        row.checked = 1
        row.uploadtime = time.strftime('%Y-%m-%d %H:%M:%S')
        dbsession.commit()

    def recommend_by_id(self, articleid):
        row = dbsession.query(Article).filter(Article.articleid==articleid).first()
        row.recommend = 1
        dbsession.commit()

    def find_all_by_headline(self, headline):
        print(headline)
        result = dbsession.query(Article, Users).join(Users, Users.userid == Article.userid).filter(Article.hidden==0, Article.drafted==0, Article.checked==1, Article.headline.like('%' + headline + '%')).order_by(Article.likes.desc()).all()
        return result

