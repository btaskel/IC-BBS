from datetime import datetime

from exts import db


class AdvertModel(db.Model):
    __tablename__ = 'advert'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    create_time = db.Column(db.DateTime, default=datetime.now)

    create_user = db.Column(db.String(100), db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    user = db.relationship('UserModel', backref='adverts')
    post = db.relationship('PostModel', backref='advert')
