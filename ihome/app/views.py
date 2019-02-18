import os
import re
import uuid

from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_user, login_required, logout_user, LoginManager, current_user

from app.models import db, Area, User, House, Facility

# 获取登录管理对象
login_manage = LoginManager()


@login_manage.user_loader
def load_user(user_id):
    # 定义被login_manage装饰的回调函数
    # 返回的是当前登录系统的用户对象
    # return User.query.filter(User.id == user_id).first()
    return User.query.get(user_id)


# 初始化蓝图对象，蓝图用于模块化管理路由
blue = Blueprint('app', __name__)


# 首页
@blue.route('/index/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        areas = Area.query.all()
        if not current_user.is_anonymous:
            # 如果不是匿名用户，返回自己的房源
            houses = House.query.filter(House.user_id == current_user.id).all()
            return render_template('index.html', areas=areas, houses=houses)
        else:
            # 如果是匿名用户，返回所有房源前三个
            houses = House.query.all()[:3]
            return render_template('index.html', areas=areas, houses=houses)
    if request.method == 'POST':
        pass


# 注册
@blue.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        # 获取表单上传的参数
        mobile = request.form.get('mobile')
        imagecode = request.form.get('imagecode')
        phonecode = request.form.get('phonecode')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        # 验证
        if mobile and password and password2:
            # 手机号格式是否正确
            if not re.match(r'^1[34578]\d{9}$', mobile):
                return render_template('register.html', error_mobile1='手机号格式不正确')
            # 手机号是否已经注册
            phone = User.query.filter(User.phone == mobile).first()
            if phone:
                return render_template('register.html', error_mobile2='手机号已注册')
            # 密码长度不能少于6位
            if len(password) < 6 or len(password2) < 6:
                return render_template('register.html', error_password1='密码长度不能少于6位')
            # 两次密码是否一致
            if password != password2:
                return render_template('register.html', error_password2='两次密码不一致')
            # 添加至数据库
            u = User()
            u.phone = mobile
            u.pwd_hash = generate_password_hash(password)

            db.session.add(u)
            db.session.commit()
            return redirect(url_for('app.login'))
        else:
            # 传递的参数有为空的情况
            return render_template('register.html', error_info='参数不能为空')


# 登录
@blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        # 获取post参数
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        # 检验参数是否填写完成
        if not all([mobile, password]):
            return render_template('login.html', error_info='参数未填写完')
        # 从数据库获取手机号对应用户
        user = User.query.filter_by(phone=mobile).first()
        # 如果存在该用户
        if user:
            # 验证密码是否一致
            if check_password_hash(user.pwd_hash, password):
                # 使用flask-login实现登录操作
                # 向session中存键值对，键为user_id,值为id值
                login_user(user)
                return redirect(url_for('app.my'))
            else:
                return render_template('login.html', error_pwd='密码错误')
        # 如果不存在该用户
        else:
            return render_template('login.html', error_user='该用户未注册')


# 退出
@blue.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('app.index'))


# 详情
@blue.route('/detail/<int:id>/', methods=['GET', 'POST'])
# @blue.route('/detail/', methods=['GET', 'POST'])
def detail(id):
# def detail():
    if request.method == 'GET':
        house = House.query.filter_by(id=id).first()
        return render_template('detail.html', house=house)
    if request.method == 'POST':
        pass


# 我的爱家
@blue.route('/my/', methods=['GET', 'POST'])
@login_required
def my():
    if request.method == 'GET':
        return render_template('my.html')
    if request.method == 'POST':
        pass


# 修改
@blue.route('/profile/', methods=['GET', 'POST', 'PUT'])
@login_required
def profile():
    if request.method == 'GET':
        return render_template('profile.html')
    if request.method == 'POST':
        # 从数据库获取用户
        user = User.query.filter(User.id == current_user.id).first()

        # 获取图片参数
        icon = request.files.get('avatar')
        if icon:
            # 获取项目的根路径
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # 获取媒体文件的路径
            STATIC_DIR = os.path.join(BASE_DIR, 'static')
            MEDIA_DIR = os.path.join(STATIC_DIR, 'media')
            # 随机生成图片的名称
            filename = str(uuid.uuid4())
            a = icon.mimetype.split('/')[-1:][0]
            name1 = filename + '.' + a
            # 拼接图片的地址
            path = os.path.join(MEDIA_DIR, name1)
            # 保存
            icon.save(path)
            # 修改用户的头像avatar字段
            user.avatar = name1
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('app.my'))

        # 获取用户名参数
        name = request.form.get('name')
        if name:
            if user.name == name:
                return render_template('profile.html', error_name='用户名已存在')
            user.name = name
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('app.my'))
        else:
            return render_template('profile.html', error_info='请输入参数')


# 我的订单
@blue.route('/orders/', methods=['GET', 'POST'])
@login_required
def orders():
    if request.method == 'GET':
        return render_template('orders.html')
    if request.method == 'POST':
        pass


# 实名认证
@blue.route('/auth/', methods=['GET', 'POST'])
@login_required
def auth():
    if request.method == 'GET':
        return render_template('auth.html')
    if request.method == 'POST':
        # 获取参数
        real_name = request.form.get('real_name')
        id_card = request.form.get('id_card')
        # 验证参数有效性
        if not all([real_name, id_card]):
            return render_template('auth.html', error_info='信息填写不完整，请补全信息')
        # 验证身份证合法
        if not re.match(r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$',
                        id_card):
            return render_template('auth.html', error_id='身份证不合法')
        # 修改数据库对象
        user = User.query.filter(User.id == current_user.id).first()
        user.id_name = real_name
        user.id_card = id_card
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('app.my'))


# 我的房源
@blue.route('/myhouse/', methods=['GET', 'POST'])
@login_required
def myhouse():
    if request.method == 'GET':
        houses = House.query.filter(House.user_id == current_user.id).all()
        return render_template('myhouse.html', houses=houses)
    if request.method == 'POST':
        pass


# 客户订单
@blue.route('/lorders/', methods=['GET', 'POST'])
@login_required
def lorders():
    if request.method == 'GET':
        return render_template('lorders.html')
    if request.method == 'POST':
        pass


# 发布新房源
@blue.route('/newhouse/', methods=['GET', 'POST'])
@login_required
def newhouse():
    if request.method == 'GET':
        areas = Area.query.all()
        facilities = Facility.query.all()
        return render_template('newhouse.html', facilities=facilities, areas=areas)
    if request.method == 'POST':
        # 获取参数
        title = request.form.get('title')
        price = request.form.get('price')
        area_id = request.form.get('area_id')
        address = request.form.get('address')
        room_count = request.form.get('room_count')
        acreage = request.form.get('acreage')
        unit = request.form.get('unit')
        capacity = request.form.get('capacity')
        beds = request.form.get('beds')
        deposit = request.form.get('deposit')
        min_days = request.form.get('min_days')
        max_days = request.form.get('max_days')
        if not all([title, price, area_id, address, room_count, acreage, unit, capacity,
                    beds, deposit, min_days, max_days]):
            return render_template('newhouse.html', error_info='请将全部信息填写完整后再提交')
        if current_user:
            house = House()
            house.user_id = current_user.id
            house.title = title
            house.price = int(price)
            house.area_id = int(area_id)
            house.address = address
            house.room_count = int(room_count)
            house.acreage = int(acreage)
            house.unit = unit
            house.capacity = int(capacity)
            house.beds = beds
            house.deposit = int(deposit)
            house.min_days = int(min_days)
            house.max_days = int(max_days)
            # 添加至数据库
            db.session.add(house)
            db.session.commit()
            return redirect(url_for('app.myhouse'))


# 预订
@blue.route('/booking/<int:id>/', methods=['GET', 'POST'])
def booking(id):
    if request.method == 'GET':
        house = House.query.filter_by(id=id).first()
        return render_template('booking.html', house=house)
    if request.method == 'POST':
        pass


# 搜索
@blue.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        areas = Area.query.all()
        houses = House.query.all()
        return render_template('search.html', areas=areas, houses=houses)
    if request.method == 'POST':
        pass
