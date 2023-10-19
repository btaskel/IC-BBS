from datetime import datetime

from exts import db


class AdvertModel(db.Model):
    __tablename__ = 'advert'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text(2000), nullable=False)
    url = db.Column(db.String(255))
    active = db.Column(db.Boolean, nullable=False, default=True)
    create_time = db.Column(db.DateTime, default=datetime.now)

    create_user = db.Column(db.String(100), db.ForeignKey('user.id'))

    user = db.relationship('UserModel', backref='adverts')