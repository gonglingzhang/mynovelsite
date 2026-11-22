import io
import random
import string
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from PIL import Image, ImageDraw, ImageFont
from .form import NovelRegisterForm, NovelLoginForm, NovelChangePasswordForm, NovelResetPWDForm
from .models import NovelUserModel
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
        form = NovelRegisterForm(request.POST, request=request)
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
        form = NovelResetPWDForm(request.POST, request=request)
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


# 图片验证码
def image_captcha(request):
    # 生成 4 位随机验证码（字母+数字，排除易混淆字符）
    chars = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'
    captcha_text = ''.join(random.choice(chars) for _ in range(4))
    # 存入 session（用于注册/重置密码时校验）
    request.session['image_captcha'] = captcha_text

    # 创建图片
    width, height = 120, 40
    image = Image.new('RGB', (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(image)

    # 尝试加载字体，找不到就用默认
    try:
        font = ImageFont.truetype('arial.ttf', 26)
    except IOError:
        font = ImageFont.load_default()

    # 画验证码文字
    for i, char in enumerate(captcha_text):
        x = 15 + i * 25
        y = random.randint(2, 8)
        draw.text((x, y), char, fill=(random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)), font=font)

    # 画干扰线
    for _ in range(4):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=(random.randint(150, 220), random.randint(150, 220), random.randint(150, 220)))

    # 画干扰点
    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(random.randint(180, 230), random.randint(180, 230), random.randint(180, 230)))

    # 转为 PNG 返回
    buf = io.BytesIO()
    image.save(buf, 'PNG')
    buf.seek(0)
    return HttpResponse(buf, content_type='image/png')


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
