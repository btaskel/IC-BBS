from datetime import datetime

from shortuuid import uuid

from exts import db

# user_chat_table = db.Table(
#     'user_chat_table',
#     db.Column('user_id', db.String, db.ForeignKey('user.id')),
#     db.Column('chat_id', db.String, db.ForeignKey('chat.id'))
# )
#
#
# class ChatModel(db.Model):
#     __tablename__ = 'chat'
#     id = db.Column(db.String(100), primary_key=True, default=uuid)
#     create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
#     content = db.Column(db.Text(2000), nullable=False)
#
#     user = db.relationship('UserModel', secondary=user_chat_table, backref='chats')

class ChatModel(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.String(100), primary_key=True, default=uuid)
    content = db.Column(db.Text(2000), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    sender_id = db.Column(db.String(100), db.ForeignKey('user.id'))
    receiver_id = db.Column(db.String(100), db.ForeignKey('user.id'))

    sender = db.relationship('UserModel', foreign_keys=[sender_id])
    receiver = db.relationship('UserModel', foreign_keys=[receiver_id])