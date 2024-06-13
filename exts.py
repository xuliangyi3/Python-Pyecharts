import flask_mail
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
mail = flask_mail.Mail()