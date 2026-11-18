import random
import string
import time
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from .form import NovelRegisterForm, NovelLoginForm, NovelChangePasswordForm, NovelResetPWDForm
from .models import NovelUserModel, NovelCaptchaModel
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
User = NovelUserModel
# Create your views here.


# 登录 GET方法是用户访问登录页面的时候用到，POST是登录的时候用到。
@require_http_methods(["GET", "POST"])
def novel_login(request):
    if request.method == "GET":
        return render(request, "novel_authentication/novel_login.html",)
    else:
        form = NovelLoginForm(request.POST)
        if form.is_valid():
            username_email = form.cleaned_data.get('username_email')
            password = form.cleaned_data.get('password')
            remember_pwd = form.cleaned_data.get('remember_pwd')
            user = User.objects.filter(
                Q(email=username_email) | Q(username=username_email)).first()
            if user and check_password(password, user.password):
                auth_login(request, user)
                if not remember_pwd:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(604800)
                # 登录成功后，将用户名传递给前端页面
                return redirect(reverse('index'))  # 重定向到首页
            else:
                return render(request, "novel_authentication/novel_login.html", {
                    "error_message": "用户名或密码错误！"
                })
        else:
            return render(request, "novel_authentication/novel_login.html", {"form": form})


# 注册
@require_http_methods(["GET", "POST"])
def novel_register(request):
    if request.method == "GET":
        return render(request, "novel_authentication/novel_register.html",)
    else:
        form = NovelRegisterForm(request.POST)
        # form.is_valid()已经将该表单验证合法了，具体验证的东西在class NovelRegisterForm(forms.Form)的def clean_中配置了。
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = User(username=username, email=email)
            user.password = make_password(password)
            user.save()
            return redirect(reverse('novel_auth:reverse_novel_login'))
        else:
            # 返回错误信息到前端页面
            return render(request, "novel_authentication/novel_register.html", {"form": form})


# 重置密码
@require_http_methods(["GET", "POST"])
def novel_reset_pwd(request):
    if request.method == "GET":
        return render(request, "novel_authentication/novel_reset_pwd.html",)
    else:
        form = NovelResetPWDForm(request.POST)
        # form.is_valid()已经将该表单验证合法了，具体验证的东西在class NovelRegisterForm(forms.Form)的def clean_中配置了。
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('new_password')
            user = User.objects.filter(email=email).first()
            user.set_password(password)
            user.save()
            return redirect(reverse('novel_auth:reverse_novel_login'))
        else:
            # 返回错误信息到前端页面
            return render(request, "novel_authentication/novel_reset_pwd.html", {"form": form})


# 发送验证码
def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code": 400, "message": "邮箱不能为空。"})
    # 生成验证码
    captcha = ''.join(random.sample(string.digits, 4))
    # 验证码存储逻辑可以根据需要添加，例如存入数据库或缓存
    NovelCaptchaModel.objects.update_or_create(
        email=email, defaults={'captcha': captcha})
    # 发送验证码
    send_mail("欢迎注册星群免费小说", message=f"您的验证码是：{captcha}", recipient_list=[
              email], from_email=None)
    return JsonResponse({"code": 200, "message": "验证码已发送，请注意查收。", "captcha": captcha})


@login_required
def novel_logout(request):
    auth_logout(request)
    return redirect(reverse('novel_auth:reverse_novel_login'))  # 登出后重定向到登录界面


# 修改密码
@require_http_methods(["GET", "POST"])
def novel_change_password(request):
    if request.method == 'GET':
        return render(request, "novel_authentication/novel_change_password.html")
    else:
        form = NovelChangePasswordForm(request.POST)
        if form.is_valid():
            username_email = form.cleaned_data.get('username_email')
            new_password_confirm = form.cleaned_data.get('new_password_confirm')
            user = User.objects.filter(Q(email=username_email) | Q(username=username_email)).first()
            user.password = make_password(new_password_confirm)
            user.save()
            return redirect(reverse("novel_auth:reverse_novel_login"))
        else:
            # 返回错误信息到前端页面
            print(form.errors)
            return render(request, "novel_authentication/novel_change_password.html", {"form": form})
