from django import forms
from django.contrib.auth.hashers import check_password

from user.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20,
                               min_length=5,
                               required=True,
                               error_messages={
                                   'required': '用户名必填',
                                   'max_length': '用户名不能超过20字符',
                                   'min_length': '用户名不能短于5字符'
                               })
    password = forms.CharField(max_length=20,
                               min_length=8,
                               required=True,
                               error_messages={
                                   'required': '密码必填',
                                   'max_length': '密码不能超过20字符',
                                   'min_length': '密码不能短于8字符'
                               })
    password2 = forms.CharField(max_length=20,
                                min_length=8,
                                required=True,
                                error_messages={
                                    'required': '密码必填',
                                    'max_length': '密码不能超过20字符',
                                    'min_length': '密码不能短于8字符'
                                })

    def clean_user_name(self):
        # 校验注册的账号是否已经存在
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).first()
        if user:
            raise forms.ValidationError('该账号已存在，请更换账号再注册')
        return self.cleaned_data['username']

    def clean(self):
        # 检验密码是否一致
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError({'password2': '两次密码不一致'})
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20,
                               min_length=5,
                               required=True,
                               error_messages={
                                   'required': '用户名必填',
                                   'max_length': '用户名不能超过20字符',
                                   'min_length': '用户名不能短于5字符'
                               })
    password = forms.CharField(max_length=20,
                               min_length=8,
                               required=True,
                               error_messages={
                                   'required': '密码必填',
                                   'max_length': '密码不能超过20字符',
                                   'min_length': '密码不能短于8字符'
                               })

    def clean(self):
        # 校验注用户名是否已经注册
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError({'username': '该账号没有注册,请去注册'})
        # 校验密码
        password = self.cleaned_data.get('password')
        if not check_password(password, user.password):
            raise forms.ValidationError({'password': '密码错误'})
        return self.cleaned_data
