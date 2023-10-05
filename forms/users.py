from flask_wtf.file import FileAllowed
from wtforms import StringField, ValidationError, BooleanField, FileField
# EqualTo验证两个字符串是否相同
from wtforms.validators import Email, Length, EqualTo

from exts import cache
from models.users import UserModel
from .baseform import BaseForm


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确格式的邮箱.")])
    password = StringField(validators=[Length(min=6, max=20, message='密码格式错误.')])
    remember = BooleanField()


class RegisterForm(BaseForm):
    username = StringField(validators=[Length(min=2, max=20, message='用户名应在2-20个字符之间')])
    email = StringField(validators=[Email(message='请输入正确格式的邮箱，例如：xxxxx@qq.com')])
    password = StringField(validators=[Length(min=6, max=20, message='密码应在8-20个字符之间')])
    repassword = StringField(validators=[EqualTo('password', message='两次输入的密码不一致！')])
    captcha = StringField(validators=[Length(min=6, max=6, message='验证码应是六位数')])

    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise ValidationError(message='邮箱已经存在')

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        cache_captcha = cache.get(email)
        if not cache_captcha or captcha != cache_captcha:
            raise ValidationError(message='验证码错误')


class EditProfileForm(BaseForm):
    username = StringField(validators=[Length(min=2, max=20, message='用户名应在2-20个字符之间')])
    portrait = FileField(validators=[FileAllowed(['jpg', 'png', 'jpeg'], message='上传的图片类型错误, 只能为jpg, png或jpeg.')])
    signature = StringField(validators=[Length(min=2, max=1000, message='签名应该在2-1000个字符之间')])

