from flask import session, request
from sqlalchemy import Table
from common.database import dbconnect
import time

from module.article import Article
from module.users import Users

dbsession, md, DBase = dbconnect()

class Comment(DBase):
    __table__ = Table("comment", md, autoload=True)

    # 统计所有评论的数量
    def get_comment_number(self):
        result = dbsession.query(Comment).count()
        return result

    # 添加一条评论
    def insert_comment(self, articleid, content, ipaddress):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        comment = Comment(userid=session.get('userid'), articleid=articleid, content=content, ipaddress=ipaddress, createtime=now, updatetime=now, agreecount=0, opposecount=0, hidden=0)
        dbsession.add(comment)
        dbsession.commit()

    # 新增回复
    def insert_reply(self, articleid, commentid, content, ipaddress):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        comment = Comment(userid=session.get('userid'), articleid=articleid, content=content, ipaddress=ipaddress, replyid=commentid, createtime=now, updatetime=now, agreecount=0, opposecount=0, hidden=0)
        dbsession.add(comment)
        dbsession.commit()

    # 通过文章id找相应的评论
    def find_by_articleid(self, articleid):
        result = dbsession.query(Comment).filter(Comment.articleid==articleid, Comment.hidden==0, Comment.replyid==0).all()
        return result

    # 限制用户每天只能评论5条
    def check_limit_per_5(self):
        # 当天的起始时间
        start = time.strftime("%Y-%m-%d 00:00:00")
        # 当天的结束时间
        end = time.strftime("%Y-%m-%d 23:59:59")
        result = dbsession.query(Comment).filter(Comment.userid==session.get("userid"), Comment.createtime.between(start, end)).count()
        if result > 5:
            return True
        else:
            return False

    # 更新文章评论量
    def update_replycount(self, articleid):
        row = dbsession.query(Article).filter(Article.articleid==articleid).first()
        row.replycount += 1
        dbsession.commit()

    # 找从start开始count条评论
    def find_limit_with_user(self, articleid, start, count):
        result = dbsession.query(Comment, Users).join(Users, Users.userid == Comment.userid).filter(Comment.articleid==articleid, Comment.hidden==0).order_by(Comment.commentid.desc()).limit(count).offset(start).all()
        return result

    # 增加评论的赞数
    def update_agree_count(self, commentid):
        row = dbsession.query(Comment).filter(Comment.commentid==commentid).first()
        row.agreecount += 1
        dbsession.commit()

    # 增加评论的踩数
    def update_disagree_count(self, commentid):
        row = dbsession.query(Comment).filter(Comment.commentid == commentid).first()
        row.opposecount += 1
        dbsession.commit()

    # 查找用户的评论和对应文章
    def find_user_comments(self, userid):
        res = dbsession.query(Comment, Article).join(Article, Comment.articleid==Article.articleid).filter(Comment.userid==userid).order_by(Comment.createtime.desc()).all()
        return res

    # 查找评论给定用户的评论
    def find_mentioned_user_comment(self, userid):
        res = dbsession.query(Comment, Article, Users).join(Article, Comment.articleid==Article.articleid).filter(Article.userid==userid, Comment.hidden==0).join(Users, Users.userid==Comment.userid).order_by(Comment.createtime.desc()).all()
        return res

    def hide_comment(self, commentid):
        comment = dbsession.query(Comment).filter(Comment.commentid==commentid).first()
        comment.hidden=1
        dbsession.commit()


