from datetime import datetime

from exts import db

class advert:
    __tablename__ = 'advert'
    name = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text(2000), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    create_time = db.Column(db.DateTime, default=datetime.now)

