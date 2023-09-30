from wtforms import StringField, IntegerField
from wtforms.validators import Length, InputRequired

from .baseform import BaseForm


class WorkForm(BaseForm):
    title = StringField(validators=[Length(min=3, max=30, message='工单标题应该在3-30个字符之间')])
    content = StringField(validators=[Length(min=10, max=3000, message='工单内容应该在10-3000个字符之间')])
    level = IntegerField(validators=[InputRequired(message='请输入板块的id')])