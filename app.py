import pandas
from flask import Flask, render_template, redirect, url_for, session
from sqlalchemy.testing.pickleable import User

import config
from exts import db, mail
from blueprints.auth import bp as bp_auth
from blueprints.qa import bp as bp_qa
from flask_migrate import Migrate
from models import UserModel

app = Flask(__name__)
# 加载数据库配置
app.config.from_object(config)
# 初始化
db.init_app(app)
mail.init_app(app)
# ORM模型数据迁移
migrate = Migrate(app, db)

app.register_blueprint(bp_auth)
app.register_blueprint(bp_qa)
#
# @app.before_request
# def my_before_request():
#     user_id = session.get('user_id')
#     if user_id:
#         user = UserModel.query.get(user_id)
#         setattr(g,)


if __name__ == '__main__':
    app.run(debug=True,port=3389)
