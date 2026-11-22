from django import forms
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from .models import NovelUserModel, NovelCaptchaModel


User = NovelUserModel


# class里面的form要与html中的name保持一致
class NovelRegisterForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': '邮箱'}),
        error_messages={
            'required': '请输入邮箱。',
            'invalid': '请输入有效的邮箱地址。',
        },
    )
    username = forms.CharField(
        required=True,
        min_length=2,
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': '用户名'}),
        error_messages={
            'required': '请输入用户名。',
            'min_length': '用户名长度在2~20之间！',
            'max_length': '用户名长度在2~20之间！',
        },
    )
    password1 = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        widget=forms.PasswordInput(attrs={'placeholder': '密码'}),
        error_messages={
            'required': '请输入密码。',
            'min_length': '密码长度必须在6到20个字符之间！',
            'max_length': '密码长度必须在6到20个字符之间！',
        },
    )
    password2 = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        widget=forms.PasswordInput(attrs={'placeholder': '确认密码'}),
        error_messages={
            'required': '请输入确认密码。',
            'min_length': '密码长度必须在6到20个字符之间！',
            'max_length': '密码长度必须在6到20个字符之间！',
        },
    )
    verification_code = forms.CharField(
        required=True,
        min_length=4,
        max_length=4,
        widget=forms.TextInput(attrs={'placeholder': '验证码'}),
        error_messages={
            'required': '请输入验证码。',
            'min_length': '验证码长度为4位！',
            'max_length': '验证码长度为4位！',
        },
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    # 这里clean_后面的命名要和上面的字段保持一致。且是按照顺序执行的,比如要对比password1和password2是否一致的时候，如果设置为clean_password1，那么就获取不到password2的数据，因为还没有执行到。
    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('该邮箱已被注册，请使用其他邮箱。')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        exists = User.objects.filter(username=username).exists()
        if exists:
            raise forms.ValidationError('该用户名已被注册，请换一个吧。')
        return username

    def clean_password2(self):
        password = self.cleaned_data.get('password1')
        confirm_password = self.cleaned_data.get('password2')
        if password != confirm_password:
            raise forms.ValidationError('密码和确认密码不一致，请重新输入。')
        return confirm_password

    def clean_verification_code(self):
        captcha = self.cleaned_data.get('verification_code', '').upper()
        session_captcha = self.request.session.get('image_captcha', '') if self.request else ''
        if not session_captcha or captcha != session_captcha:
            raise forms.ValidationError('验证码错误，请重新输入。')
        # 使用后清除
        del self.request.session['image_captcha']
        return captcha


class NovelResetPWDForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': '邮箱'}),
        error_messages={
            'required': '请输入邮箱。',
            'invalid': '请输入有效的邮箱地址。',
        },
    )
    new_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        widget=forms.PasswordInput(attrs={'placeholder': '密码'}),
        error_messages={
            'required': '请输入密码。',
            'min_length': '密码长度必须在6到20个字符之间！',
            'max_length': '密码长度必须在6到20个字符之间！',
        },
    )
    new_password_confirm = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        widget=forms.PasswordInput(attrs={'placeholder': '确认密码'}),
        error_messages={
            'required': '请输入确认密码。',
            'min_length': '密码长度必须在6到20个字符之间！',
            'max_length': '密码长度必须在6到20个字符之间！',
        },
    )
    verification_code = forms.CharField(
        required=True,
        min_length=4,
        max_length=4,
        widget=forms.TextInput(attrs={'placeholder': '验证码'}),
        error_messages={
            'required': '请输入验证码。',
            'min_length': '验证码长度为4位！',
            'max_length': '验证码长度为4位！',
        },
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    # 这里clean_后面的命名要和上面的字段保持一致。且是按照顺序执行的,比如要对比password1和password2是否一致的时候，如果设置为clean_password1，那么就获取不到password2的数据，因为还没有执行到。
    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if not exists:
            raise forms.ValidationError('邮箱输入错误,请重新输入。')
        return email

    def clean_new_password_confirm(self):
        password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('new_password_confirm')
        print(password, confirm_password)
        if password != confirm_password:
            raise forms.ValidationError('密码和确认密码不一致，请重新输入。')
        return confirm_password

    def clean_verification_code(self):
        captcha = self.cleaned_data.get('verification_code', '').upper()
        session_captcha = self.request.session.get('image_captcha', '') if self.request else ''
        if not session_captcha or captcha != session_captcha:
            raise forms.ValidationError('验证码错误，请重新输入。')
        # 使用后清除
        del self.request.session['image_captcha']
        return captcha


class NovelLoginForm(forms.Form):
    username_email = forms.CharField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': '请输入用户名或者邮箱。'}),
        error_messages={
            'required': '请输入用户名或者邮箱。'
        },
    )
    password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        widget=forms.PasswordInput(attrs={'placeholder': '密码'}),
        error_messages={
            'required': '请输入密码。',
            'min_length': '密码长度必须在6到20个字符之间！',
            'max_length': '密码长度必须在6到20个字符之间！',
        },
    )
    remember_pwd = forms.IntegerField(required=False)


class NovelChangePasswordForm(forms.Form):
    username_email = forms.CharField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': '请输入用户名或者邮箱。'}),
        error_messages={
            'required': '请输入用户名或者邮箱。'
        },
    )
    raw_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        widget=forms.PasswordInput(attrs={'placeholder': '原始密码'}),
        error_messages={
            'required': '请输入原始密码。',
            'min_length': '原始密码长度必须在6到20个字符之间！',
            'max_length': '原始密码长度必须在6到20个字符之间！',
        },
    )
    new_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        widget=forms.PasswordInput(attrs={'placeholder': '新密码'}),
        error_messages={
            'required': '请输入新密码。',
            'min_length': '新密码长度必须在6到20个字符之间！',
            'max_length': '新密码长度必须在6到20个字符之间！',
        },
    )
    new_password_confirm = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        widget=forms.PasswordInput(attrs={'placeholder': '确认新密码'}),
        error_messages={
            'required': '请输入确认新密码。',
            'min_length': '确认新密码长度必须在6到20个字符之间！',
            'max_length': '确认新密码长度必须在6到20个字符之间！',
        },
    )

    def clean(self):
        cleaned_data = super().clean()
        username_email = cleaned_data.get('username_email')
        raw_password = cleaned_data.get('raw_password')
        new_password = cleaned_data.get('new_password')
        new_password_confirm = cleaned_data.get('new_password_confirm')
        exists = User.objects.filter(
            Q(username=username_email) | Q(email=username_email)).exists()
        user = User.objects.filter(
            Q(email=username_email) | Q(username=username_email)).first()
        if not exists:
            raise forms.ValidationError('用户名或者邮箱输入错误，请重新输入。')
        if not check_password(raw_password, user.password):
            raise forms.ValidationError('原始密码输入错误，请重新输入。')
        if raw_password == new_password:
            raise forms.ValidationError('新密码与旧密码一样，无需更改。')
        if new_password != new_password_confirm:
            print('新密码和确认新密码不一致，请重新输入。')
            raise forms.ValidationError('新密码和确认新密码不一致，请重新输入。')
        return cleaned_data
