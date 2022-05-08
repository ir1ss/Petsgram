from flask import Blueprint, render_template, session

from module.article import Article
from module.comment import Comment
from module.favorite import Favorite
from module.users import Users

userPage = Blueprint('userPage', __name__)

@userPage.route('/userpage')
def gotoUserPage():
    credits = Users().find_user_credit(session.get('userid'))
    articleNum = Article().get_user_article_num(session.get('userid'))
    likeData = Favorite().find_user_like(session.get('userid'))
    print(likeData)
    return render_template('userpage.html', username=session.get('username'), credits=credits, articleNum=articleNum, likeData=likeData, userRole=session.get('role'))

@userPage.route('/userpage/myArticles')
def gotoMyArticles():
    credits = Users().find_user_credit(session.get('userid'))
    articleNum = Article().get_user_article_num(session.get('userid'))
    userArticles = Article().find_by_userid(session.get('userid'))
    return render_template('myArticles.html', username=session.get('username'), credits=credits, articleNum=articleNum, userArticles=userArticles, userRole=session.get('role'))

@userPage.route('/userpage/myDrafts')
def gotoMyDrafts():
    credits = Users().find_user_credit(session.get('userid'))
    articleNum = Article().get_user_article_num(session.get('userid'))
    userDrafts = Article().find_Drafts_by_userid(session.get('userid'))
    return render_template('myDrafts.html', username=session.get('username'), credits=credits, articleNum=articleNum, userDrafts=userDrafts, userRole=session.get('role'))

@userPage.route('/userpage/myCheckings')
def gotoMyCheckings():
    credits = Users().find_user_credit(session.get('userid'))
    articleNum = Article().get_user_article_num(session.get('userid'))
    if session.get('role') == 'user':
        userChecks = Article().find_checkings(session.get('userid'))
    else:
        userChecks = Article().find_checking_list()
    return render_template('myCheckings.html', username=session.get('username'), credits=credits, articleNum=articleNum, userChecks=userChecks, userRole=session.get('role'))

@userPage.route('/userpage/myComments')
def gotoMyComments():
    credits = Users().find_user_credit(session.get('userid'))
    articleNum = Article().get_user_article_num(session.get('userid'))
    userComments = Comment().find_user_comments(session.get('userid'))
    return render_template('myComments.html', username=session.get('username'), credits=credits, articleNum=articleNum, userComments=userComments, userRole=session.get('role'))

@userPage.route('/userpage/myMentioned')
def gotoMyMentioned():
    credits = Users().find_user_credit(session.get('userid'))
    articleNum = Article().get_user_article_num(session.get('userid'))
    mentionedUser = Comment().find_mentioned_user_comment(session.get('userid'))
    return render_template('myMentioned.html', username=session.get('username'), credits=credits, articleNum=articleNum, mentionedUser=mentionedUser, userRole=session.get('role'))

