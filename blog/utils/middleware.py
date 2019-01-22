
import logging
import re
import time

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin



# 获取logger
from user.models import User

logger = logging.getLogger(__name__)

class LogMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # url到服务器的时候，经过中间件最先执行的方法
        request.init_time = time.time()
        request.init_body = request.body

    def process_response(self, request, response):
        try:
            # 经过中间件，最后执行的方法
            # 计算请求到响应的时间
            count_time = time.time() - request.init_time
            # 获取响应的状态码
            code = response.status_code
            # 获取请求的内容
            req_body = request.init_body
            # 获取想要的内容
            res_body = response.content

            msg = '%s %s %s %s' % (count_time, code, req_body, res_body)
            # 写入日志信息
            logger.info(msg)
        except Exception as e:
            logger.critical('log error, Exception:%s' % e)

        return response


class UserAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 拦截请求之前的函数
        # 对所有请求都进行登录状态的校验
        # 1.给request.user属性赋值，赋值为当前登录系统的用户
        user_id = request.session.get('user_id')
        if user_id:
            # user = User.objects.get(pk=user_id)
            user = User.objects.filter(pk=user_id).first()
            request.user = user
        # 2.登录校验，需区分哪些地址需要做登录校验，哪些地址不需要做登录校验
        # 如果请求的path为去结算的路由：/order/place_order/
        path = request.path
        # if path == '/':
        #     return None
        # 不需要做登录校验的地址
        not_need_check = ['/user/register/', '/user/login/',
                          '/user/index/']
        for check_path in not_need_check:
            if re.match(check_path, path):
                # 当前path路径为不需要做登录校验的路由
                return None
        # path为需要做登录校验的路由时，判断用户是否登录，没有登录则跳转到登录
        if not user_id:
            return HttpResponseRedirect(reverse('user:login'))