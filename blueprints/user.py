import logging
import os
import random
from datetime import datetime

from flask import Blueprint, request, render_template, url_for, redirect, flash, current_app, session, g, make_response
from flask_mail import Message
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from decorators import login_register
from exts import db, mail, cache
from forms.profile import Signature, Privacy
from forms.users import RegisterForm, LoginForm
from models.users import UserModel, GenderEnum
from utils import restful

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户的首页注册视图函数"""
    if hasattr(g, 'user'):
        logging.debug(f'User {g.user.username} visited the User register')
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
    if hasattr(g, 'user'):
        logging.debug(f'User {g.user.username} visited the User send_email')

    try:
        email = request.args.get('email')
        digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        captcha = ''.join(random.sample(digits, 6))
        body = f'您的验证码为：{captcha}'
        title = str(current_app.config['BBS_NAME'])
        message = Message(subject=title, recipients=[email], body=body)
        mail.send(message)
        cache.set(email, captcha, timeout=240)
        return restful.ok()
    except Exception as e:
        print(e)
        return restful.params_error()


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户的首页登录视图函数"""
    if hasattr(g, 'user'):
        logging.debug(f'User {g.user.username} visited the User login')

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


@bp.get('/profile/<string:user_id>')
def profile(user_id):
    if hasattr(g, 'user'):
        logging.debug(f'User {g.user.username} visited the User profile')

    if request.method == 'GET':
        if not user_id:
            return render_template('front/profile.html', user=g.user, is_mine=True)
        user = UserModel.query.get(user_id)
        if not user:
            return redirect(url_for('status.error_404'))
        is_mine = True if user.email == g.user.email else False
        follow_active = g.user.is_following(user)
        return render_template('front/profile.html', user=user, is_mine=is_mine, follow_active=follow_active)


@bp.route('/profile_edit', methods=['GET', 'POST'])
def profile_edit():
    if request.method == 'GET':
        if hasattr(g, 'user'):
            logging.debug(f'User {g.user.username} visited the User profile_edit')
        gender = GenderEnum
        return render_template('front/profile_edit.html', user=g.user, gender=gender)
    else:
        pass


@bp.route('/profile_edit_delete', methods=['GET', 'POST'])
def profile_edit_delete():
    if request.method == 'GET':
        return render_template('front/profile/profile_edit_delete.html', user=g.user)
    else:
        pass


@bp.route('/profile_edit_binding', methods=['GET', 'POST'])
def profile_edit_binding():
    if request.method == 'GET':
        return render_template('front/profile/profile_edit_binding.html', user=g.user)
    else:
        pass


@bp.route('/profile_edit_privacy', methods=['GET', 'POST'])
def profile_edit_privacy():
    if request.method == 'GET':
        return render_template('front/profile/profile_edit_privacy.html', user=g.user)
    else:
        form = Privacy(request.form)
        if form.validate():
            user = g.user

            location = form.location.data
            phone = form.phone.data
            birthday = form.birthday.data
            home = form.home.data

            user.location = location
            user.phone = phone
            user.birthday = birthday
            user.home = home

            db.session.add(user)
            db.session.commit()
        else:
            for message in form.messages:
                flash(message)
        return redirect(url_for('user.profile_edit_signature'))


@bp.route('/profile_edit_signature', methods=['GET', 'POST'])
def profile_edit_signature():
    if request.method == 'GET':
        return render_template('front/profile/profile_edit_signature.html', user=g.user)
    else:
        form = Signature(request.form)
        if form.validate():
            user = g.user
            signature = form.signature.data
            user.signature = signature
            db.session.add(user)
            db.session.commit()
        else:
            flash('个人签名字数应该在5——1000字以内')
        return redirect(url_for('user.profile_edit_signature'))


@bp.route('/logout')
def logout():
    """退出账户"""
    if hasattr(g, 'user'):
        logging.debug(f'User {g.user.username} visited the User logout')

    if hasattr(g, 'user'):
        session.clear()
    return redirect('/')


@bp.post('/follow')
@login_register
def follow():
    """
    一个用户关注与取消关注一个用户
    :return: 状态码
    """
    if hasattr(g, 'user'):
        logging.debug(f'User {g.user.username} visited the User follow')
    follow_id = request.form.get('follow')
    user = g.user

    if follow_id:
        follow_user = UserModel.query.get(follow_id)
        if follow_user and follow_user.is_active and user.is_following(follow_user):
            print('un')
            user.unfollow(follow_user)
            db.session.add(user)
            db.session.commit()
            return restful.ok('已经取消关注该用户')

        elif follow_user and follow_user.is_active and not user.is_following(follow_user):
            print('fo')
            user.follow(follow_user)
            db.session.add(user)
            db.session.commit()
            return restful.ok('已关注该用户')
    return restful.params_error('没有查找到该用户，或该用户已被封禁')

    # user_to_unfollow = UserModel.query.get(follow_)
    # if user_to_unfollow and user.is_following(user_to_unfollow):
    #     if user.id != user_to_unfollow.id:
    #
    #         user.unfollow(user_to_unfollow)
    #         db.session.commit()
    #         return restful.ok()
    #     else:
    #         return restful.params_error('用户不存在！')
    #
    # if follow_ and not unfollow_:  # 关注
    #
    #     user_to_follow = UserModel.query.get(follow_)
    #     if user_to_follow and not user.is_following(user_to_follow) and user.id != user_to_follow.id:
    #         user.follow(user_to_follow)
    #         db.session.commit()
    #         return restful.ok()
    #     else:
    #         return restful.params_error('用户不存在！')
    # elif not follow_ and unfollow_:  # 取消关注
    #     user_to_unfollow = UserModel.query.get(unfollow_)
    #     if user_to_unfollow and user.is_following(user_to_unfollow) and user.id != user_to_unfollow.id:
    #
    #         user.unfollow(user_to_unfollow)
    #         db.session.commit()
    #         return restful.ok()
    #     else:
    #         return restful.params_error('用户不存在！')
    # else:
    #     return restful.params_error('无效的操作！')


@bp.post('/unfollow/<string:user_id>')
@login_register
def unfollow(user_id):
    """关注user_id"""
    if hasattr(g, 'user'):
        logging.debug(f'User {g.user.username} visited the User unfollow')

    user = g.user
    user_to_unfollow = UserModel.query.get(user_id)
    if user_to_unfollow is not None:
        user.unfollow(user_to_unfollow)
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error()


@bp.get('/show/<string:filename>')
def show_image(filename):
    if hasattr(g, 'user'):
        logging.debug(f'User {g.user.username} visited the User show_image')

    file_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'upload\\user\\portraits')
    if filename is None or filename == 'default':
        try:
            image_data = open(os.path.join(current_app.config['UPLOAD_FOLDER'], 'upload\\user\\default\\portrait.jpg'),
                              "rb").read()
        except:
            return redirect(url_for('status.error_500'))
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response
    else:
        try:
            image_data = open(os.path.join(file_dir, filename), "rb").read()
        except:
            return redirect(url_for('status.error_500'))

        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response


@bp.post('/upload_portrait')
def upload_portrait():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('user.profile_edit'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('user.profile_edit'))
    try:
        ext = file.filename.split('.')[-1]
    except Exception as e:
        print(e)
        return restful.params_error('文件拓展名不符合规范')

    if ext not in ['jpg', 'jpeg', 'png']:
        return restful.params_error('文件拓展名不符合规范')

    filename = secure_filename(file.filename)
    save_path = os.path.join(current_app.config.get('UPLOAD_FOLDER'), 'upload\\user\\portraits\\', filename)
    file.save(save_path)
    user = UserModel.query.get(g.user.id)
    user.portrait = filename
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('user.profile', user_id=g.user.id))
