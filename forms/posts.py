from wtforms import StringField, IntegerField
from wtforms.validators import Length,InputRequired

from forms.baseform import BaseForm


class CommentForm(BaseForm):
    content = StringField(validators=[Length(min=2, max=2000, message='输入内容应该在2-2000字之间')])


class PostForm(BaseForm):
    title = StringField(validators=[Length(min=5, max=50, message='请输入5-50的字符标题')])
    content = StringField(validators=[Length(min=5, max=3000, message='请输入5-3000的字符内容')])
    board_id = IntegerField(validators=[InputRequired(message='请输入正确的板块id')])
