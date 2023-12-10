from wtforms import StringField
from wtforms.validators import Length

from .baseform import BaseForm

class ChatForm(BaseForm):
    content = StringField(validators=[Length(min=1, max=2000, message='输入的字符应该在1-2000个以内')])
    sender_id = StringField(validators=[Length(min=36, max=36, message='发送方id长度错误')])
    receiver_id = StringField(validators=[Length(min=36, max=36, message='接收方id长度错误')])