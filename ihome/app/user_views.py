import os
import random
import re
import uuid

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

from flask_login import login_user, LoginManager, logout_user, login_required, current_user

from app.models import User, House

# 初始化用户蓝图对象，蓝图用于模块化管理路由
user_blue = Blueprint('user', __name__)

# 获取登录管理对象
login_manage = LoginManager()


# 定义被login_manage装饰的回调函数
@login_manage.user_loader
def load_user(user_id):
    # 返回的是当前登录系统的用户对象
    # return User.query.filter(User.id == user_id).first()
    return User.query.get(user_id)


# 前端注册(暂无前端所以要写)
@user_blue.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


# 后端注册
@user_blue.route('/register/', methods=['POST'])
def my_register():
    # 获取参数
    mobile = request.form.get('mobile')
    imagecode = request.form.get('imagecode')
    passwd = request.form.get('passwd')
    passwd2 = request.form.get('passwd2')
    # 1.验证参数是否都填写了
    if not all([mobile, imagecode, passwd, passwd2]):
        return jsonify({'code': 1001, 'msg': '请填写完整参数'})
    # 2. 验证手机号正确
    if not re.match('^1[3456789]\d{9}$', mobile):
        return jsonify({'code': 1002, 'msg': '手机号不正确'})
    # 3. 验证图片验证码
    if session['img_code'] != imagecode:
        return jsonify({'code': 1003, 'msg': '验证码不正确'})
    # 4. 密码和确认密码是否一致
    if passwd != passwd2:
        return jsonify({'code': 1004, 'msg': '密码不一致'})
    # 验证手机号是否被注册
    user = User.query.filter(User.phone == mobile).first()
    if user:
        return jsonify({'code': 1005, 'msg': '手机号已被注册，请重新注册'})
    # 创建注册信息
    u = User()
    u.phone = mobile
    u.name = mobile
    u.password = passwd
    u.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})
    #     # 密码长度不能少于6位
    #     if len(password) < 6 or len(password2) < 6:
    #         return render_template('register.html', error_password1='密码长度不能少于6位')


# 获取验证码
@user_blue.route('/code/', methods=['GET'])
def get_code():
    # 方式1：后端生成图片，并返回验证码图片的地址(不推荐)
    # 方式2：后端只生成随机参数，返回给页面，在页面中生成图片(前端做)
    s = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    code = ''
    for i in range(4):
        code += random.choice(s)
    session['img_code'] = code
    return jsonify({'code': 200, 'msg': '请求成功', 'data': code})


# 前端登录(暂无前端所以要写)
@user_blue.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


# 后端登录
@user_blue.route('/my_login/', methods=['GET'])
def my_login():
    # 获取参数
    mobile = request.args.get('mobile')
    passwd = request.args.get('passwd')
    # 1.验证参数是否都填写了
    if not all([mobile, passwd]):
        return jsonify({'code': 1001, 'msg': '请填写完整参数'})
    # 从数据库获取手机号对应用户
    user = User.query.filter_by(phone=mobile).first()
    # 如果存在该用户
    if user:
        # 验证密码是否一致
        if user.check_pwd(passwd):
            # 使用flask-login实现登录操作
            # 向session中存键值对，键为user_id,值为id值
            login_user(user)
            return jsonify({'code': 200, 'msg': '请求成功'})
        else:
            return jsonify({'code': 1003, 'msg': '密码错误'})
    # 如果不存在该用户
    else:
        return jsonify({'code': 1002, 'msg': '该用户未注册'})


# 退出登录
@user_blue.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))


# 个人中心
@user_blue.route('/my/', methods=['GET'])
@login_required
def my():
    return render_template('my.html')


# 个人信息
@user_blue.route('/user_info/', methods=['GET'])
@login_required
def user_info():
    info = User.query.filter_by(id=current_user.id).first()
    return jsonify({'code': 200, 'info': info.to_basic_dict()})


# 修改(前端)
@user_blue.route('/profile/', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html')


# 修改用户名
@user_blue.route('/profile/user_profile/', methods=['PATCH'])
@login_required
def user_profile():
    # 从数据库获取用户
    user = User.query.filter(User.id == current_user.id).first()
    # 从数据库获取所有用户名
    users = User.query.all()
    names = []
    for ddf in users:
        names.append(ddf.name)

    # 获取用户名参数
    name = request.form.get('name')
    if name:
        if name in names:
            return jsonify({'code': 1002, 'msg': '该用户名已存在！'})
        user.name = name
        user.add_update()
        return jsonify({'code': 200, 'msg': '成功修改用户！'})
    else:
        return jsonify({'code': 1001, 'msg': '请填写用户名'})


# 修改图片
@user_blue.route('/profile/picture_profile/', methods=['PATCH'])
@login_required
def picture_profile():
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
        user.add_update()
        return jsonify({'code': 200, 'msg': '成功修改图片！', 'ddf': current_user.avatar})
    else:
        return jsonify({'code': 1001, 'msg': '请填写图片'})


# 实名认证(前端)
@user_blue.route('/auth/', methods=['GET'])
@login_required
def auth():
    return render_template('auth.html')


# 实名认证(后端)
@user_blue.route('/auth/', methods=['PATCH'])
@login_required
def my_auth():
    # 获取参数
    real_name = request.form.get('real_name')
    id_card = request.form.get('id_card')
    # 验证参数有效性
    if not all([real_name, id_card]):
        return jsonify({'code': 1001, 'msg': '信息填写不完整，请补全信息！'})
    # 验证身份证合法
    if not re.match('^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$',
                    id_card):
        return jsonify({'code': 1002, 'msg': '身份证不合法！'})
    # 验证名字合法否 [\u4e00-\u9fa5]
    if not re.match('^[\u4e00-\u9fa5]{2,6}$', real_name):
        return jsonify({'code': 1003, 'msg': '名字必须中文并且大于两个字小于六个字！'})
    # 验证身份证是否已经存在，身份证号唯一
    # 从数据库获取所有用户名
    users = User.query.all()
    id_cards = []
    for ddf in users:
        id_cards.append(ddf.id_card)
    if id_card in id_cards:
        return jsonify({'code': 1004, 'msg': '身份证已存在！'})
    # 修改数据库对象
    user = User.query.filter(User.id == current_user.id).first()
    user.id_name = real_name
    user.id_card = id_card
    user.add_update()
    return jsonify({'code': 200, 'msg': '保存成功！'})



