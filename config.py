SECRET_KEY = 'dgsgff;fhlflsfdh'

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'flaskProjectDemo'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = DB_URI

MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = '3520202392@qq.com'
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = '3520202392@qq.com'
