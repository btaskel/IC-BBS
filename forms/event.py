from wtforms import StringField, IntegerField
from wtforms.validators import Length

from forms.baseform import BaseForm
from models.event import ReportTypeEnum


class ReportForm(BaseForm):
    """举报验证器"""
    title = StringField(validators=[Length(min=2, max=50, message='举报标题应该在2-50字之间')])
    content = StringField(validators=[Length(min=2, max=800, message='举报内容应该在2-800字之间')])
    report_type = IntegerField(validators=[Length(min=0, max=len(ReportTypeEnum) - 1, message='举报类型选择错误')])


class BulletinForm(BaseForm):
    """公告验证器"""
    title = StringField(validators=[Length(min=2, max=150, message='公告标题应该在2-150字之间')])
    content = StringField(validators=[Length(min=5, max=5000, message='公告内容应该在5-5000字之间')])
