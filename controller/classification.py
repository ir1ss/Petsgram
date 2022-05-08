# 图像识别控制器
from keras import models
from keras.models import load_model
from flask import Blueprint, request, render_template, redirect, url_for, jsonify, session
import tensorflow as tf
from module.article import Article
from module.breeds import Breeds

clsf = Blueprint('clsf', __name__)

@clsf.route('/classification', methods=['POST', 'GET'])
def classification():
    if request.method == 'GET':
        article = Article()
        view, likes, recommend = article.find_most_view_and_like_and_recommend()
        breeds = Breeds()
        breedTypes = breeds.find_all_breed()
        breedNames = []
        for b in breedTypes:
            breedNames.append(b[1].breedName)
        return render_template('classification.html', view=view, likes=likes, userRole=session.get('role'), breedNames=breedNames)
    if request.method == 'POST':
        img_str = request.files.get('file').read()
        x = tf.image.decode_image(img_str, channels=3)
        x = tf.image.resize(x, (512, 512))
        x = x / 255.
        x = tf.reshape(x, (1, 512, 512, 3))
        model = load_model('E:\开发\pythonProject\petsgram_final\model_f.h5')
        preb = model.predict(x)
        maxid = 0
        maxpro = 0
        for i, probabilty in enumerate(preb[0]):
            if probabilty > maxpro:
                maxpro = probabilty
                maxid = i
        print(maxid)
        breeds = Breeds()
        breed_found = breeds.find_by_id(maxid);
        res = Article().find_all_by_headline(breed_found.breedName)
        articles = []
        for i in res:
            tmp = []
            tmp.append(i[0].headline)
            tmp.append(i[0].uploadtime.strftime("%Y-%m-%d"))
            tmp.append(i[0].content)
            tmp.append(i[1].username)
            tmp.append(i[0].articleid)
            articles.append(tmp)
        res = {
            'code': 0,
            'data': {
                    'b_name': breed_found.breedName,
                    'probability': 100,
                    'b_desc' : breed_found.description,
                    'b_infoLink' : '',
                    'b_cover' : breed_found.cover,
                    'article_info' : articles
            }
        }
        return jsonify(res)

