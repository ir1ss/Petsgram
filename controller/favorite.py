from flask import Blueprint, request
from module.favorite import Favorite

favorite = Blueprint('favorite', __name__)

# 添加收藏
@favorite.route('/like', methods=['POST'])
def add_favorite():
    articleid = request.form.get('articleid')
    try:
        Favorite().insert_favorite(articleid)
        return 'favorite-pass'
    except:
        return 'favorite-fail'

# 取消收藏
@favorite.route('/canclelike', methods=['POST'])
def cancel_favorite():
    articleid = request.form.get('articleid')
    try:
        Favorite().cancel_favorite(articleid)
        return 'cancel-pass'
    except:
        return 'cancel-fail'


