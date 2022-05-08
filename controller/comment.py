from flask import Blueprint, request, session
from module.article import Article
from module.comment import Comment
from module.credit import Credit
from module.users import Users

comment = Blueprint("comment", __name__)

@comment.route('/comment', methods=['POST'])
def addComment():
    articleid = request.form.get('articleid')
    content = request.form.get('content')
    ipaddress = request.remote_addr
    print(articleid, content, ipaddress)
    # 筛选一下评论
    if len(content) < 5 or len(content) > 1000:
        return "content-invalid"
    print('ss')
    comment = Comment()
    if comment.check_limit_per_5():
        return "add-limit"
    # try:
    print(comment)
    comment.insert_comment(articleid, content, ipaddress)
    Article().update_replycount(articleid)
    if session.get('role') == 'user':
        Credit().insert_detail(type='添加评论', target=articleid, credit=2, userid=session.get('userid'))
        Users().update_credit(2, userid=session.get('userid'))
        return "add-pass"
    else:
        return "admin-add-pass"
    # except:
    #     return "add-fail"

@comment.route('/agree', methods=['POST'])
def addAgree():
    commentid = request.form.get('commentid')
    Comment().update_agree_count(commentid)
    return 'agree-pass'

@comment.route('/disagree', methods=['POST'])
def addDisagree():
    commentid = request.form.get('commentid')
    Comment().update_disagree_count(commentid)
    return 'disagree-pass'

@comment.route('/hideComment', methods=['POST'])
def hideComment():
    commentid = request.form.get('commentid')
    Comment().hide_comment(commentid)
    return "ok"
