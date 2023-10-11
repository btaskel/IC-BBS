from datetime import datetime
from enum import Enum

from shortuuid import uuid

from exts import db


class PermissionEnum(Enum):
    """权限表：这里增加"""
    BOARD = '板块'
    POST = '帖子'
    COMMENT = '评论'
    FRONT_USER = '前台用户'
    CMS_USER = '后台用户'


role_permission_table = db.Table(
    'role_permission_table',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)


class PermissionModel(db.Model):
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Enum(PermissionEnum), nullable=False, unique=True)


class RoleModel(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    desc = db.Column(db.String(70), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    permissions = db.relationship('PermissionModel', secondary=role_permission_table,
                                  backref='roles')  # secondary= 设置多对多中间表


followers = db.Table(
    'followers',
    db.Column('follower_id', db.String(100), db.ForeignKey('user.id')),
    db.Column('followed_id', db.String(100), db.ForeignKey('user.id'))
)


class GenderEnum(Enum):
    male = '男'
    female = '女'
    Female_cross_male = '女跨男'
    male_to_female = '男跨女'
    LGBT = 'LGBT'
    other = '其他性别'
    none = '未填写'


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(100), primary_key=True, default=uuid)
    username = db.Column(db.String(20), nullable=False)
    _password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    email_active = db.Column(db.Boolean, nullable=False, default=False)

    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    create_time_active = db.Column(db.Boolean, nullable=False, default=True)

    signature = db.Column(db.Text(1000), default='什么都没有写唷~ (￣▽￣)')
    signature_active = db.Column(db.Boolean, nullable=False, default=True)

    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.none)
    gender_active = db.Column(db.Boolean, nullable=False, default=True)

    phone = db.Column(db.Integer, default='--未填写--')
    phone_active = db.Column(db.Boolean, nullable=False, default=True)

    location = db.Column(db.String(200), default='火星~')
    location_active = db.Column(db.Boolean, default=True)

    birthday = db.Column(db.String(7), default='--未填写--')
    birthday_active = db.Column(db.Boolean, nullable=False, default=True)

    home = db.Column(db.String(255), default='--未填写--')
    home_active = db.Column(db.Boolean, nullable=False, default=True)

    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_staff = db.Column(db.Boolean, nullable=False, default=False)
    report = db.Column(db.Boolean, default=True)
    portrait = db.Column(db.String(255), default='media/upload/user/default/portrait.jpg', nullable=False)

    # # 关注者
    followed = db.relationship(
        'UserModel', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    role = db.relationship('RoleModel', backref='users')
    # role = db.relationship('RoleModel', backref='users')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def has_permission(self, permission):
        for perm in self.role.permissions:
            if perm.name == permission:
                return True
        return False

# following_id', db.String(100), db.ForeignKey('user.id')),
#     db.Column('followers_id


# user_follow_table = Table(
#     'user_follow_table',
#     db.Column('following_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('followers_id', db.Integer, db.ForeignKey('user.id'))
# )
