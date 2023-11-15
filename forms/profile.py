from wtforms import StringField, IntegerField
from wtforms.validators import Length

from forms.baseform import BaseForm

class Signature(BaseForm):
    signature = StringField(validators=[Length(min=5, max=1000, message='个人签名应该在5-1000字以内')])

class Privacy(BaseForm):
    phone = IntegerField(validators=[Length(min=11, max=11, message='个人手机号应该为11位')])
    location = StringField(validators=[Length(max=100, message='个人未知应该在100字以内')])
    birthday = StringField(validators=[Length(max=50, message='个人生日应该在50字以内')])
    home = StringField(validators=[Length(max=100, message='家属性应该在100字以内')])