from flask import Blueprint, render_template, request

from module.article import Article

userWrite = Blueprint('userWrite', __name__)

@userWrite.route('/write')
def UserWrite():
    return render_template('write-article.html')

@userWrite.route('/submitArticle', methods=['POST'])
def submitArticle():
    headline = request.form.get('headline')
    content = request.form.get('content')
    type = request.form.get('type')
    credit = request.form.get('credit')
    drafted = request.form.get('drafted')
    checked = request.form.get('checked')
    try:
        Article().add_new_article(headline, content, type, credit, drafted, checked)
        return "submit-pass"
    except:
        return "submit-fail"

