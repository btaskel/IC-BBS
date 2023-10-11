import random
from datetime import datetime

from flask import Blueprint, request, render_template, url_for, redirect, flash, current_app, session, g
from flask_mail import Message
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.security import check_password_hash

from exts import db, mail, cache
from forms.users import RegisterForm, LoginForm, EditProfileForm
from models.users import UserModel
from utils import restful

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户的首页注册视图函数"""
    if request.method == 'GET':
        return render_template('front/register.html')

    else:
        form = RegisterForm(request.form)
        if form.validate():
            # 验证用户提交表单成功
            email = form.email.data
            username = form.username.data
            password = form.password.data
            captcha = form.captcha.data
            cache_captcha = cache.get(email)
            if not captcha == cache_captcha:
                flash('验证码错误')
                return redirect(url_for('user.register'))
            user = UserModel(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))
        else:
            for message in form.messages:
                flash(message)
            return redirect(url_for('user.register'))


@bp.route('/send_email')
def send_email():
    """发送电子邮件用于验证用户注册和登录"""
    try:
        email = request.args.get('email')
        digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        captcha = ''.join(random.sample(digits, 6))
        body = f'您的验证码为：{captcha}'
        title = str(current_app.config['BBS_NAME'])
        message = Message(subject=title, recipients=[email], body=body)
        mail.send(message)
        cache.set(email, captcha, timeout=240)
        return '邮件发送成功'
    except Exception as e:
        print(e)
        return restful.ok()


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户的首页登录视图函数"""
    if request.method == 'GET':
        return render_template('front/signin.html')

    else:
        form = LoginForm(request.form)
        if form.validate():

            email = form.email.data
            password = form.password.data
            remember = form.remember.data

            user = UserModel.query.filter_by(email=email).first()
            # 数据库hash密码，用户输入源密码; 相同hash值则返回True

            if user and check_password_hash(user._password, password):
                if not user.is_active:
                    flash('用户已被封禁')
                    return redirect(url_for('user.login'))
                session['user_id'] = user.id
                # 记住登录状态
                if remember:
                    session.permanent = True
                user.last_active_time = datetime.now()
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('post.post_list'))

            else:
                flash('账号不存在或密码错误')
                return redirect(url_for('user.login'))

        else:
            for message in form.messages:
                flash(message)
            return redirect(url_for('user.login'))


@bp.route('/test')
def test():
    # s = UserModel(username='test', _password='112233445566', email='11111@hotmail.com')
    # s2 = UserModel(username='test2', _password='112233145566', email='11211@hotmail.com')
    #
    # db.session.add_all([s, s2])
    # db.session.commit()
    s = UserModel.query.filter_by(username='test').first()
    s2 = UserModel.query.filter_by(username='test2').first()

    # 将s的关注列表中增加s2
    s.followed.append(s2)
    db.session.commit()

    # # 让用户 A 取消关注用户 B
    # user_a.followed.remove(user_b)
    # db.session.commit()

    return 'ok'


@bp.route('/profile/<string:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    if request.method == 'GET':
        user = UserModel.query.get(user_id)
        is_mine = False
        if g.user.email == user.email:
            is_mine = True
        return render_template('front/profile.html', user=user, is_mine=is_mine)
    else:
        form = EditProfileForm(CombinedMultiDict([request.form, request.files]))
        if form.validate():
            print(form.username.data)
            print(form.portrait.data)
            print(form.signature.data)
        return redirect(url_for('front.index'))


@bp.route('/logout')
def logout():
    """退出账户"""
    if g.user:
        session.clear()
    return redirect('/')

@bp.post('/upload')
def upload():
    if 'image' not in request.files:
        flash('上传图片格式错误')
        return redirect(url_for(''))
    image = request.files['image']
    if image.filename == '':
        return redirect(url_for(''))
