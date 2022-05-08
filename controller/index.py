# 首页的控制器
from flask import Blueprint, render_template, abort, session
from module.article import Article
import math

index = Blueprint('index', __name__)

# 文章主页的路由
@index.route('/')
def home():
    start = 0
    article = Article()
    result = article.find_limit_with_users(start, 5)
    total = math.ceil(article.get_total_count() / 5)
    view, likes, recommend = article.find_most_view_and_like_and_recommend()
    return render_template('index.html', result=result, total=total, page=1, view=view, likes=likes, recommend=recommend, recommendTotal=len(recommend), userRole=session.get('role'))

# 根据页码访问文章列表的路由
@index.route('/page/<int:page>')
def pageGet(page):
    start = (page-1) * 5
    article = Article()
    result = article.find_limit_with_users(start, 5)
    total = math.ceil(article.get_total_count() / 5)
    view, likes, recommend = article.find_most_view_and_like_and_recommend()
    return render_template('index.html', result=result, total=total, page=page, view=view, likes=likes, recommend=recommend, recommendTotal=len(recommend), userRole=session.get('role'))

# 根据种类访问文章列表的路由
@index.route('/type/<int:type>-<int:page>')
def typeGet(type, page):
    start = (page-1) * 5
    article = Article()
    result = article.find_by_type(type, start, 5)
    total = math.ceil(article.get_total_count_by_type(type) / 5)
    view, likes, recommend = article.find_most_view_and_like_and_recommend()
    return render_template('typeIndex.html', result=result, total=total, page=page, type=type, view=view, likes=likes, recommend=recommend, recommendTotal=len(recommend))

# 搜索
@index.route('/search/<int:page>-<keyword>')
def searchArticle(page, keyword):
    keyword = keyword.strip()
    if keyword is None or keyword == '' or '%' in keyword or len(keyword) > 20:
        abort(404)
    start = (page - 1) * 5
    article = Article()
    result = article.find_by_headline(keyword, start, 5)
    total = math.ceil(article.get_count_by_headline(keyword) / 5)
    view, likes, recommend = article.find_most_view_and_like_and_recommend()
    return render_template('searchResult.html', result=result, page=page, total=total, keyword=keyword, view=view, likes=likes)

