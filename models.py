from exts import db


class UserModel(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(20), nullable=False)


class EmailCaptchaModel(db.Model):
    __tablename__ = 'captcha'
    captcha_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    captcha = db.Column(db.String(20), unique=True, nullable=False)
