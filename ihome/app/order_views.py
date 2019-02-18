from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import current_user, login_required

from app.models import Area, House, Facility, HouseImage, Order

# 初始化订单蓝图对象，蓝图用于模块化管理路由
order_blue = Blueprint('order', __name__)


# 房屋预定(前端渲染页面)
@order_blue.route('/booking/', methods=['GET'])
@login_required
def booking():
    return render_template('booking.html')


# 房屋预定(后端)
@order_blue.route('/booking/<int:id>/', methods=['GET'])
def my_booking(id):
    # 查询房屋信息
    house = House.query.filter_by(id=id).first()
    # 返回指定id的简略的house参数
    return jsonify({'code': 200, 'house': house.to_dict()})


# 创建订单
@order_blue.route('/order/', methods=['POST'])
def create_order():
    # 房子id
    house_id = request.form.get('house_id')
    # request.form.get('begin_date')得到字符串 得进行转换
    # 入住时间
    begin_date = datetime.strptime(request.form.get('begin_date'), '%Y-%m-%d')
    # 离店时间
    end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
    # 总时间
    days = (end_date - begin_date).days + 1
    # 获取相应房子id对应的房子对象
    house = House.query.get(house_id)
    # 房间价格
    price = house.price
    # 总价格
    amount = price * days
    # 创建订单对象并添加数据至数据库
    order = Order()
    order.user_id = current_user.id
    order.house_id = house_id
    order.begin_date = begin_date
    order.end_date = end_date
    order.days = days
    order.house_price = price
    order.amount = amount
    order.add_update()
    return jsonify({'code': 200})


# 修改订单
@order_blue.route('/order/', methods=['PATCH'])
def update_order():
    # 获取参数
    comment = request.form.get('comment')
    order_id = request.form.get('order_id')
    # 获取参数2
    status = request.form.get('status')
    reject_reason = request.form.get('reject_reason')
    # 添加到数据库
    order = Order.query.filter_by(id=order_id).first()
    # 传评价
    if comment:
        order.comment = comment
        order.add_update()
        return jsonify({'code': 200})
    # 传拒单和接单
    if status:
        order.status = status
        order.add_update()
        return jsonify({'code': 200})


# 我的订单(前端页面)
@order_blue.route('/orders/', methods=['GET'])
def orders():
    return render_template('orders.html')


# 我的订单(接口信息)
@order_blue.route('/my_orders/', methods=['GET'])
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    orders_list = [order.to_dict() for order in orders]
    return jsonify({'code': 200, 'orders_list': orders_list})


# 客户订单(前端页面)
@order_blue.route('/lorders/', methods=['GET'])
def lorders():
    return render_template('lorders.html')


# 客户订单(接口信息)
@order_blue.route('/my_lorders/', methods=['GET'])
def my_lorders():
    houses = House.query.filter_by(user_id=current_user.id).all()
    houses_ids = [house.id for house in houses]

    orders = Order.query.filter(Order.house_id.in_(houses_ids))
    orders_list = [order.to_dict() for order in orders]
    return jsonify({'code': 200, 'houses_list': orders_list})