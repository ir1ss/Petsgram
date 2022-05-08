from flask import Blueprint, make_response, session, request, render_template, redirect
from common.utility import ImageCode, gen_email_code, send_email
from module.credit import Credit
from module.users import Users
# python中的正则表达式模块↓
import re
# python中实现md5加密的模块↓
import hashlib

user = Blueprint('user', __name__)

@user.route('/vcode', methods=['POST', 'GET'])
def vcode():
    code, bstring = ImageCode().get_code()
    response = make_response(bstring)
    response.headers['Content-Type'] = 'image/jpeg'
    session['vcode'] = code.lower()
    print(session.get('vcode'))
    return response

@user.route('/ecode', methods=['POST'])
def ecode():
    email = request.form.get('email')
    # 后台也需校验，因为用户可能直接访问接口
    if not re.match('.+@.+\..+', email):
        return 'email-invalid'
    code = gen_email_code()
    try:
        send_email(email, code)
        session['ecode'] = code
        return 'send-pass'
    except:
        return 'send-fail'

@user.route('/user', methods=['POST'])
def doRegister():
    user = Users()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    email = request.form.get('email').strip()
    petname = request.form.get('petname').strip()
    petbreed = request.form.get('petbreed').strip()
    city = request.form.get('city').strip()
    province = request.form.get('province').strip()
    ecode = request.form.get('ecode').strip()
    # 校验数据
    if session.get('ecode') != ecode:
        return 'ecode-error'
    elif not re.match('.+@.+\..+', email) or len(password) < 5:
        return 'up-invalid'
    # 验证是否已经注册
    elif len(user.find_by_username(username)) > 0:
        return 'username-used'
    elif len(user.find_by_email(email)) > 0:
        return 'email-used'
    else:
        # # 密码使用md5加密
        password = hashlib.md5(password.encode()).hexdigest()
        # # 保存信息至数据库
        result = user.do_register(username, password, email, petname, petbreed, city, province)
        # # 保存session
        session['islogin'] = 'true'
        session['userid'] = result.userid
        session['username'] = username
        session['password'] = password
        session['email'] = email
        session['petname'] = petname
        session['petbreed'] = petbreed
        session['city'] = city
        session['province'] = province
        session['role'] = result.role
        # 更新积分记录
        Credit().insert_detail(type='用户注册', target=0, credit=50, userid=session.get('userid'))
        return 'reg-pass'

@user.route('/userLogin', methods=['POST'])
def doLogin():
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    vcode = request.form.get('vcode').strip().lower()
    print(vcode)
    if vcode != session.get('vcode'):
        return 'vcode-error'
    elif len(Users().find_by_username(username)) == 0:
        return 'no-such-user'
    elif Users().is_password_correct(username, password) == False:
        return 'wrong-password'
    else:
        session['username'] = username
        session['islogin'] = 'true'
        session['userid'] = Users().find_by_username(username)[0].userid
        if username == 'admin':
            session['role'] = 'admin'
        else:
            session['role'] = 'user'
        Users().update_login_time(session.get('userid'))
        print(username)
        if not Users().is_first_login_today(session.get('userid')) and session.get('role') != 'admin':
            Users().update_credit(5)
            return "login-success-and-add-credit"
        else:
            return 'login-success'

@user.route('/logout')
def logout():
    session['islogin'] = 'false'
    return redirect('/')

