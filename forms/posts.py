from wtforms import StringField, IntegerField
from wtforms.validators import Length, ValidationError, NumberRange

from forms.baseform import BaseForm


class CommentForm(BaseForm):
    content = StringField(validators=[Length(min=2, max=2000, message='输入内容应该在2-2000字之间')])


class ListLength(object):
    def __init__(self, min=-1, max=-1):
        self.min = min
        self.max = max

    def __call__(self, form, field):
        if not isinstance(field.data, list):
            raise ValidationError('字段必须是一个列表类型')
        if len(field.data) < self.min or self.max != -1 and len(field.data) > self.max:
            raise ValidationError('列表元素的数量必须在{}-{}之间'.format(self.min, self.max))


class PostForm(BaseForm):
    title = StringField(validators=[Length(min=5, max=100, message='请输入5-50的字符标题')])
    board_id = IntegerField(validators=[NumberRange(min=1, max=255, message='请输入一个有效的板块值')])
    images = StringField(validators=[Length(min=5, max=1000, message='图片URL过长')])
