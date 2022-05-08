# 交易功能的控制器
from flask import Blueprint, render_template, abort
from module.article import Article

shop = Blueprint('shop', __name__)

@shop.route('/shop')
def goShop():
    return render_template('shop.html')