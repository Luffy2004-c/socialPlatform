from django.core.validators import RegexValidator
from myapp.models import User
from django import forms
from .ui_form import BootstrapForm
from common.encrypt import encrypt


class RegisterModelForm(BootstrapForm, forms.ModelForm):  # 用户注册表单
    password = forms.CharField(
        label="密码",
        min_length=8,
        max_length=128,
        error_messages={"min_length": "密码最少为8位", "max_length": "密码最多为128位"},
        widget=forms.PasswordInput,
    )
    password_confirm = forms.CharField(label="确定密码", widget=forms.PasswordInput)
    code = forms.CharField(label="验证码", required=False)

    class Meta:
        model = User
        fields = ["username", "password", "password_confirm"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        exists = User.objects.filter(username=username).exists()
        if exists:
            raise forms.ValidationError("用户名已存在")
        return username

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return encrypt(pwd)

    def clean_password_confirm(self):
        pwd = self.cleaned_data.get("password")
        comfirm_pwd = encrypt(self.cleaned_data.get("password_confirm"))
        if pwd != comfirm_pwd:
            raise forms.ValidationError("两次密码不一致")
        return comfirm_pwd


class LoginModelForm(BootstrapForm, forms.ModelForm):  # 用户登录表单
    username = forms.CharField(label="用户名")
    password = forms.CharField(label="密码", widget=forms.PasswordInput)
    code = forms.CharField(label="验证码", widget=forms.TextInput, required=False)

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return encrypt(password)

    class Meta:
        model = User
        fields = ["username", "password"]
