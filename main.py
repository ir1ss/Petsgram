from flask import Flask, render_template, request, redirect, url_for, session, make_response, abort
import os
from flask_sqlalchemy import SQLAlchemy
import pymysql
import flask
pymysql.install_as_MySQLdb()

app = Flask(__name__, template_folder='template', static_url_path='/', static_folder='resource')
app.config['SECRET_KEY'] = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/petsgram?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 100
db = SQLAlchemy(app)

# @app.route('/index')
# def index2():
#     return render_template('index.html')
#
# @app.route('/articlebase')
# def articlebase():
#     return render_template('article-base.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error-404.html')

@app.errorhandler(500)
def server_error(e):
    return render_template('error-500.html')

@app.before_request
def before():
    url = request.path
    # 拦截器白名单
    pass_list = ['/user', '/login', '/logout', '/register', '/ecode', '/vcode', '/userLogin']
    if url in pass_list or url.endswith('.js') or url.endswith('.jpg') or url.endswith('.png') or url.endswith('.css'):
        pass
    elif session.get('islogin') is None or session.get('islogin') == 'false':
        return render_template('login.html')
    # elif session.get('islogin') is None:
    #     username = request.cookies.get('username')
    #     password = request.cookies.get('password')
    #     print(username)
    #     if username != None and password != None:
    #         user = Users()
    #         result = user.find_by_username(username)
    #         if len(result) == 1 and result[0].password == password:
    #             session['islogin'] = 'true'
    #             session['userid'] = result[0].userid
    #             session['username'] = username
    #             session['nickname'] = result[0].nickname
    #             session['role'] = result[0].role

def mytruncate(s, length, end='...'):
    count = 0
    new = ''
    for c in s:
        new += c
        if ord(c) <= 128:
            count += 0.5
        else:
            count += 1
        if count > length:
            break
    return new + end

app.jinja_env.filters.update(mytruncate=mytruncate)

@app.context_processor
def gettype():
    type = {
        '1': '养宠日志',
        '2': '喂养经验',
        '3': '驯养经验',
        '4': '宠物杂谈',
        '5': '讨论与提问'
    }
    return dict(article_type = type)

if __name__ == '__main__':
    from controller.index import *
    app.register_blueprint(index)
    from controller.article import *
    app.register_blueprint(article)
    from controller.classification import *
    app.register_blueprint(clsf)
    from controller.user import *
    app.register_blueprint(user)
    from controller.comment import *
    app.register_blueprint(comment)
    from controller.favorite import *
    app.register_blueprint(favorite)
    from controller.shop import *
    app.register_blueprint(shop)
    from controller.userPage import *
    app.register_blueprint(userPage)
    from controller.writeArticles import *
    app.register_blueprint(userWrite)
    from controller.notificaton import *
    app.register_blueprint(notificationControl)
    app.run(debug=True)

