from datetime import datetime, timedelta
from enum import Enum

from exts import db


class ReportTypeEnum(Enum):
    """举报类型枚举"""
    illegal = "违法违禁"
    pornography = "色情"
    vulgar = "低俗"
    gambling_fraud = "赌博诈骗"
    bloody_violence = "血腥暴力"
    name_calling = "人身攻击"
    warfare = "引战"
    political_rumors = "涉政谣言"
    false = "虚假不实信息"
    other = "有其它问题"


class WorkTypeEnum(Enum):
    """
    工单优先级枚举
    """
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class ReportModel(db.Model):
    """举报模型"""
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text(500), nullable=False)
    report_type = db.Column(db.Enum(ReportTypeEnum), nullable=False)
    active = db.Column(db.Boolean, nullable=True)

    create_time = db.Column(db.DateTime, default=datetime.now())

    user = db.relationship('UserModel', backref='reports')
    report_user_id = db.Column(db.String(100), db.ForeignKey('user.id'))

    post = db.relationship('PostModel', backref='post_reports')
    report_post_id = db.Column(db.Integer, db.ForeignKey('post.id'))


class WorkModel(db.Model):
    """工单模型"""
    __tablename__ = 'work'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text(2000), nullable=False)

    create_time = db.Column(db.DateTime, default=datetime.now())
    end_time = db.Column(db.DateTime, default=datetime.now() + timedelta(days=14))
    active = db.Column(db.Boolean, default=True, nullable=False)
    finish = db.Column(db.Boolean, default=False, nullable=False)
    timeout = db.Column(db.Boolean, default=False, nullable=False)

    level = db.Column(db.Enum(WorkTypeEnum), nullable=False)

    user = db.relationship('UserModel', backref='works')
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'))



