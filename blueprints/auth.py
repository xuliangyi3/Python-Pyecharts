import datetime
import random
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

from blueprints.forms import RegisterForms, LoginForms
from exts import mail, db
from models import EmailCaptchaModel, UserModel

bp = Blueprint("auth", __name__, url_prefix='/auth')


@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('sign-in.html')
    else:
        form = LoginForms(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel.query.filter_by(username=username).first()
            if check_password_hash(user.password,password):
                # cookie相关
                session['user_id'] = user.user_id
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('qa.home'))
        return redirect(url_for('auth.login'))



@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        form = RegisterForms(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(username=username, password=generate_password_hash(password),email=email)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            return render_template('register.html', form=form)


@bp.route('/captcha/email')
def get_email_captcha():
    # /captcha/email/<email>
    # /captcha/email?email=xxx
    email = request.args.get('email')
    captcha = random.randint(1000, 9999)  # 生成验证码的函数

    message = Message(sender='3520202392@qq.com', recipients=[email], subject=f'{datetime.datetime.now()}',
                      body=f'验证码为{captcha}')
    mail.send(message)
    # 使用数据库方式存储email和captcha
    emailcaptcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(emailcaptcha)
    db.session.commit()

    return jsonify({"code": 200, "message": "", "data": None})
