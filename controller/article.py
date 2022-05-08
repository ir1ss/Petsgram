from flask import Blueprint, abort, render_template, request, session
from module.article import Article
from module.comment import Comment
from module.credit import Credit
from module.favorite import Favorite
from module.users import Users

article = Blueprint('article', __name__)

@article.route('/article/<int:articleid>')
def readArticle(articleid):
    try:
        result = Article().find_by_id(articleid)
        if result is None:
            abort(404)
    except:
        abort(500)
    dict = {}
    for k, v in result[0].__dict__.items():
        # 模型类会有个自带属性_sa_instance_state
        if not k.startswith('_sa_instance_state'):
            dict[k] = v
    dict['username'] = result[1]
    payed = Credit().check_payed_article(articleid, session.get('userid'))
    content = dict['content']
    print(content)
    hideButton = False
    if payed == True:
        print('hi')
        hideButton = True
        position = int(len(content))
        dict['content'] = content[0:position]
    else:
        position = int(len(content)/2)
        dict['content'] = content[0:position]
    Article().update_read_count(articleid)
    is_favorite = Favorite().check_favorite(articleid)
    if is_favorite is None:
        is_favorite = False
    view, likes, recommend = Article().find_most_view_and_like_and_recommend()
    print(hideButton)
    # 获取上一篇和下一篇
    prev_and_next = Article().find_prev_and_next_by_id(articleid)
    # 显示评论
    comment_user = Comment().find_limit_with_user(articleid, 0, 50)
    if session.get('role') == 'admin':
        hideButton = True
    return render_template('article-user.html', article=dict, content=content, view=view, likes=likes, position=position, hideButton=hideButton, is_favorite=is_favorite, prev_and_next=prev_and_next, comment_user=comment_user, current_userid=session.get('userid'), userRole=session.get('role'))

@article.route('/readall', methods=['POST'])
def read_all():
    position =  request.form.get('position')
    articleid = request.form.get('articleid')
    article = Article()
    result = article.find_by_id(articleid)
    content = result[0].content[int(position):]
    creditRequire = result[0].credit
    if Users().find_user_credit(session.get('userid')) < creditRequire:
        return 'credit-not-enough'
    # 积分记录更新
    Credit().insert_detail(type="阅读文章", target=articleid, credit=-1*result[0].credit, userid=session.get('userid'))
    Credit().insert_detail(type="作者收获积分", target=articleid, credit=result[0].credit, userid=result[0].userid)
    Users().update_credit(credit=-1*result[0].credit, userid=session.get('userid'))
    Users().update_credit(credit=result[0].credit, userid=result[0].userid)
    return content

@article.route('/checkingArticle/<int:articleid>')
def goCheckArticle(articleid):
    try:
        result = Article().find_checking_by_articleid(articleid)
        if result is None:
            abort(404)
    except:
        abort(500)
    user = Users().find_by_userid(result.userid)
    return render_template('checkingArticle.html', article=result, user=user)

@article.route('/deleteArticle', methods=['POST'])
def deleteArticle():
    articleid = request.form.get('articleid')
    try:
        Article().hide_artilce_by_id(articleid)
        return 'good'
    except:
        return 'fail'

@article.route('/uploadChecking', methods=['POST'])
def uploadChecking():
    articleid = request.form.get('articleid')
    try:
        Article().check_artilce_by_id(articleid)
        return 'good'
    except:
        return 'fail'

@article.route('/recommend', methods=['POST'])
def recommend():
    article = request.form.get('articleid')
    try:
        Article().recommend_by_id(article)
        return "ok"
    except:
        return "fail"

