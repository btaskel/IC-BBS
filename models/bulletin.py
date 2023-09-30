from exts import db

class BulletinModel(db.Model):
    """社团模型"""
    __tablename__ = 'bulletin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=True)
    content = db.Column(db.Text(5000), nullable=True)

    user_id = db.Column(db.String(100), db.ForeignKey('user.id'))
    author = db.relationship('UserModel', backref='bulletins')