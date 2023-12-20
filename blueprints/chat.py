import logging
import random

from flask import Blueprint, render_template, g, request, current_app
from flask_mail import Message
from sqlalchemy import or_

from decorators import login_register
from exts import csrf, db, mail
from forms.chat import ChatForm, Email
from models.message import ChatModel
from models.users import UserModel
from utils import restful

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.get('/')
def index():
    return render_template('front/chat/index.html')

@bp.post('/send/<string:user_id>')
@csrf.exempt
@login_register
def send(user_id):
    user = g.user
    recv_user = UserModel.query.get(user_id)
    if not recv_user:
        return restful.params_error('接收的用户不存在！')
    form = Email(request.form)
    if form.validate():
        message = form.message.data
        bbs_name = current_app.config['BBS_NAME']
        title = f'{bbs_name} - 来自{user.username}的消息.'
        try:
            message = Message(subject=title, recipients=[recv_user.email], body=message)
            mail.send(message)
        except Exception as e:
            logging.error(e)
            return restful.server_error('发送邮件时服务器产生错误！')
        return restful.ok()
    else:
        return restful.params_error('字段验证失败')