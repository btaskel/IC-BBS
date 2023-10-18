from datetime import datetime

from shortuuid import uuid

from exts import db


class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    create_time = db.Column(db.DateTime, default=datetime.now)


class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(4000), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    views = db.Column(db.Integer, default=0)
    reports = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)

    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    author_id = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)

    images = db.relationship('PostImages', backref='post')
    board = db.relationship('BoardModel', backref='posts')
    author = db.relationship('UserModel', backref='posts')


class PostImages(db.Model):
    __tablename__ = 'postImages'
    id = db.Column(db.String(100), primary_key=True, default=uuid)
    name = db.Column(db.String(255), nullable=False, default=uuid)
    path = db.Column(db.String(255), nullable=False, default='.\\media\\local\\404.png')

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))


class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(800), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)

    post = db.relationship('PostModel', backref='comments')
    author = db.relationship('UserModel', backref='comments')
