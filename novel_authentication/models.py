from time import timezone
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractUser

# Create your models here.


class NovelUserModel(AbstractUser):
    email = models.EmailField(
        unique=True, verbose_name="邮箱地址", db_comment="邮箱地址")
    username = models.CharField(max_length=20, unique=True, verbose_name='用户名', db_comment='用户名', validators=[
                                validators.MinLengthValidator(limit_value=2)])
    password = models.CharField(
        max_length=128, verbose_name='密码', db_comment='密码', validators=[
            validators.MinLengthValidator(limit_value=6)])
    active = models.BooleanField(
        default=1, verbose_name='是否有效', db_comment='1表示有效用户',)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)
    extra1 = models.CharField(max_length=120, blank=True,
                              null=True, verbose_name='拓展字段1', db_comment='拓展字段1')
    extra2 = models.CharField(max_length=120, blank=True,
                              null=True, verbose_name='拓展字段2', db_comment='拓展字段2')
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = '小说用户'
        verbose_name_plural = verbose_name


class NovelCaptchaModel(models.Model):
    email = models.EmailField(
        unique=True, verbose_name="邮箱地址", db_comment="邮箱地址")
    captcha = models.CharField(
        max_length=4, verbose_name="验证码", db_comment="验证码")
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '小说验证码'
        verbose_name_plural = verbose_name
