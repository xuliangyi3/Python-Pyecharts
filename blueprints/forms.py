import wtforms
from wtforms.validators import Email, Length, EqualTo
from models import EmailCaptchaModel, UserModel


class RegisterForms(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误")])
    username = wtforms.StringField(validators=[Length(min=2, max=20, message='用户名格式错误！')])
    password = wtforms.StringField(validators=[Length(min=2, max=20, message='密码格式错误！')])
    password_confirm = wtforms.StringField(validators=[EqualTo('password', message='两次密码输入不一致！')])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError("邮箱或验证码异常")


class LoginForms(wtforms.Form):
    username = wtforms.StringField(validators=[Length(min=2, max=20, message='用户名输入错误！')])
    password = wtforms.StringField(validators=[Length(min=2, max=20, message='密码输入错误！')])
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])

    def validate_email(self, field):
        email = self.email.data
        email_model = UserModel.query.filter_by(email=email).first()
        if not email_model:
            raise wtforms.ValidationError("该邮箱未被注册")
