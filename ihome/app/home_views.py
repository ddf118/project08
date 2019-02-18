import os
import uuid

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import current_user, login_required

from app.models import Area, House, Facility, HouseImage

# 初始化房屋蓝图对象，蓝图用于模块化管理路由
home_blue = Blueprint('home', __name__)


# 判断是不是匿名用户
@home_blue.route('/is_user/', methods=['GET'])
def is_user():
    if not current_user.is_anonymous:
        return jsonify({'code': 1001, 'msg': '已登录用户'})
    else:
        return jsonify({'code': 1002, 'msg': '匿名用户'})


# 用户所有房子信息
@home_blue.route('/home_info/', methods=['GET'])
def home_info():
    # 房子对象的列表
    houses = House.query.filter(House.user_id == current_user.id).all()
    # 对象的列表转换成值的字典的列表
    simple_houses = []
    full_houses = []
    for house in houses:
        simple_houses.append(house.to_dict())
        full_houses.append(house.to_full_dict())
    return jsonify({'code': 200, 'simple_houses': simple_houses, 'full_houses': full_houses})


# 区域信息
@home_blue.route('/area_info/', methods=['GET'])
def area_info():
    # 区域对象的列表
    areas = Area.query.all()
    # 对象的列表转换成值的字典的列表
    areas_list = []
    for area in areas:
        areas_list.append(area.to_dict())
    return jsonify({'code': 200, 'areas_list': areas_list})


# 配套设施信息
@home_blue.route('/facility_info/', methods=['GET'])
def facility_info():
    # 配套设施对象的列表
    facilities = Facility.query.all()
    # 对象的列表转换成值的字典的列表
    facilities_list = []
    for facility in facilities:
        facilities_list.append(facility.to_dict())
    return jsonify({'code': 200, 'facilities_list': facilities_list})


# 首页(前端)
@home_blue.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


# 首页需用数据信息
@home_blue.route('/my_index/', methods=['GET'])
def my_index():
    areas = Area.query.all()
    areas_list = [area.to_dict() for area in areas]
    houses = House.query.all()[:5]
    houses_list = [house.to_dict() for house in houses]
    return jsonify({'code': 200, 'areas_list': areas_list, 'houses_list': houses_list})


# 我的房源
@home_blue.route('/myhouse/', methods=['GET'])
@login_required
def myhouse():
    return render_template('myhouse.html')


# 发布新房源(前端)
@home_blue.route('/newhouse/', methods=['GET'])
@login_required
def newhouse():
    return render_template('newhouse.html')


# 发布新房源信息
@home_blue.route('/newhouse/newhouse_info/', methods=['POST'])
@login_required
def newhouse_info():
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

    facilities = request.form.getlist('facility')
    if not all([title, price, area_id, address, room_count, acreage, unit, capacity,
                beds, deposit, min_days, max_days, facilities]):
        return jsonify({'code': 1001, 'msg': '请将全部信息填写完整后再提交'})
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
        for facility_id in facilities:
            facility = Facility.query.get(facility_id)
            # 多对多关联
            house.facilities.append(facility)
        # 添加至数据库
        house.add_update()
        return jsonify({'code': 200, 'house_id': house.id})


# 发布新房源图片
@home_blue.route('/newhouse/newhouse_picture/', methods=['POST'])
@login_required
def newhouse_picture():
    # 创建房屋图片
    house_id = request.form.get('house_id')
    image = request.files.get('house_image')
    if image:
        # 获取项目的根路径
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 获取媒体文件的路径
        STATIC_DIR = os.path.join(BASE_DIR, 'static')
        MEDIA_DIR = os.path.join(STATIC_DIR, 'media')
        # 随机生成图片的名称
        filename = str(uuid.uuid4())
        a = image.mimetype.split('/')[-1:][0]
        name1 = filename + '.' + a
        # 拼接图片的地址
        save_url = os.path.join(MEDIA_DIR, name1)
        # 本地保存图片
        image.save(save_url)
        # 保存房屋和图片信息
        house_image = HouseImage()
        house_image.house_id = house_id
        # image_url = os.path.join('media', name1)
        image_url = '/static/media/' + name1
        house_image.url = image_url
        house_image.add_update()
        # 创建房屋首图
        house = House.query.get(house_id)
        if not house.index_image_url:
            house.index_image_url = image_url
            house.add_update()
        return jsonify({'code': 200, 'image_url': image_url})
    else:
        return jsonify({'code': 1001, 'msg': '请认真上传图片！'})


# 房屋详情(前端渲染页面)
@home_blue.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


# 房屋详情(后端)
@home_blue.route('/detail/<int:id>/', methods=['GET'])
def my_detail(id):
    # 查询房屋信息
    house = House.query.filter_by(id=id).first()
    # 返回指定id详细的house参数
    return jsonify({'code': 200, 'house': house.to_full_dict()})


# 搜索页面(前端)
@home_blue.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')


# 搜索页面(后端)
@home_blue.route('/my_search/', methods=['GET'])
def my_search():
    # {aid: "8", sd: "2019-02-22", ed: "2019-02-28", sk: "new", p: 1}
    aid = request.args.get('aid')
    houses = House.query.filter(House.area_id == aid).all()
    houses_list = [house.to_dict() for house in houses]
    return jsonify({'code': 200, 'houses_list': houses_list})

