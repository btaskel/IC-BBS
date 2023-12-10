from flask import Blueprint, render_template, g, request
from sqlalchemy import or_

from exts import csrf, db
from forms.chat import ChatForm
from models.message import ChatModel
from utils import restful

bp = Blueprint('chat', __name__, url_prefix='/chat')


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        user = g.user
        messages = db.session.query(ChatModel).filter(
            or_(
                ChatModel.sender_id == user.id,
                ChatModel.receiver_id == user.id
            )
        ).order_by(ChatModel.create_time).all()
        dc = {}
        for message in messages:
            if message.sender_id:
                dc[message.sender_id] = dc.get(message.sender_id, 0) + 1

            if message.receiver_id not in dc:
                dc[message.receiver_id] = dc.get(message.sender_id, 0) + 1


        return render_template('front/chat/index.html', user=user)
    else:
        pass


@bp.post('/post_message')
@csrf.exempt
def post_message():
    form = ChatForm(request.form)
    if form.validate():
        sender_id = form.sender_id.data
        receiver_id = form.receiver_id.data
        content = form.content.data
        chat = ChatModel(content=content, sender_id=sender_id, receiver_id=receiver_id)
        db.session.add(chat)
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error('参数传递错误！')
