# users表模型
import hashlib
from flask import session
from sqlalchemy import Table
from common.database import dbconnect
import time, random

# 把common中定义的数据库连接实例导入
dbsession, md, DBase = dbconnect()

class Users(DBase):
    __table__ = Table('users', md, autoload=True)

    # 查找用户名，判断是否已经注册
    def find_by_username(self, username):
        result = dbsession.query(Users).filter(Users.username==username).all()
        return result

    # 通过邮件找用户
    def find_by_email(self, email):
        result = dbsession.query(Users).filter(Users.email==email).all()
        return result

    # 向数据库中添加注册信息
    def do_register(self, username, password, email, petname, petbreed, city, province):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        # 随机给用户头像
        avatar = str(random.randint(1, 15))
        user = Users(username=username, password=password, role='user', credit=50, email=email, petname=petname, petbreed=petbreed, city=city, province=province, createtime=now, lastlogin=now, avatar='default.jpg')
        dbsession.add(user)
        dbsession.commit()
        return user

    # 修改用户积分
    def update_credit(self, credit, userid):
        user = dbsession.query(Users).filter(Users.userid==userid).one()
        user.credit = int(user.credit) + credit
        dbsession.commit()

    # 判断登录密码是否正确
    def is_password_correct(self, username, password):
        return hashlib.md5(password.encode()).hexdigest() == dbsession.query(Users).filter(Users.username==username).one().password

    # 查找用户的积分
    def find_user_credit(self, userid):
        credit = dbsession.query(Users).filter(Users.userid==userid).one().credit
        return credit

    # 查看是否是今天第一次登录
    def is_first_login_today(self, userid):
        lastLoginTime = dbsession.query(Users.lastlogin).filter(Users.userid==userid).first()
        print(lastLoginTime[0].strftime("%Y-%m-%d"))
        today = time.strftime("%Y-%m-%d")
        print(today)
        return lastLoginTime[0].strftime("%Y-%m-%d") == today

    # 更新登录时间
    def update_login_time(self, userid):
        user = dbsession.query(Users).filter(Users.userid==userid).first()
        user.lastlogin = time.strftime('%Y-%m-%d %H:%M:%S')
        dbsession.commit()

    # 通过用户id查找
    def find_by_userid(self, userid):
        row = dbsession.query(Users).filter(Users.userid==userid).first()
        return row