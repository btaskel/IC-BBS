from wtforms import StringField
from wtforms.validators import Length, URL

from forms.baseform import BaseForm


class AdvertForm(BaseForm):
    title = StringField(validators=[Length(min=5, max=100, message='请输入5-50的字符标题')])
    content = StringField(validators=[Length(min=5, max=1000, message='请输入5-1000之间的字符内容')])
    url = StringField('URL', [URL(message='这不是一个有效的跳转链接')])