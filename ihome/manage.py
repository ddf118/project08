from flask import Flask, url_for, render_template
from flask_script import Manager

from app.models import db
from app.order_views import order_blue
from app.user_views import user_blue, login_manage
from app.home_views import home_blue
from app.views import blue

app = Flask(__name__)
# 注册蓝图对象
app.register_blueprint(blueprint=blue, url_prefix='/app')
# 注册用户蓝图对象
app.register_blueprint(blueprint=user_blue, url_prefix='/user')
# 注册房子蓝图对象
app.register_blueprint(blueprint=home_blue, url_prefix='/home')
# 注册订单蓝图对象
app.register_blueprint(blueprint=order_blue, url_prefix='/order')


# 首页/地址
@app.route('/')
def index():
    return render_template('index.html')


# 设置加密的复杂程度,存在客户端
app.secret_key = '123456'
# 配置及初始化数据库
# mysql+pymysql://root:123456@120.77.174.68:3306/ihome
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@120.77.174.68:3306/ihome'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 初始化flask-login
login_manage.init_app(app)

# 设置登陆视图，用于未授权操作的跳转：# 校验失败，则跳转到登录管理对象.login_view定义的视图函数
login_manage.login_view = 'user.login'
# 设置快闪消息，用于提示用户：
login_manage.login_message = u'请先登录后在进行操作'
# 管理flask应用对象app
manage = Manager(app)

if __name__ == '__main__':
    manage.run()
