from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse
from . import views
from django.views.generic.base import RedirectView

app_name = "novel_auth"
urlpatterns = [
    path('login', views.novel_login, name='reverse_novel_login'),
    path('register', views.novel_register, name='reverse_novel_register'),
    path('reset_pwd', views.novel_reset_pwd, name='reverse_novel_reset_pwd'),
    path('image_captcha', views.image_captcha, name='reverse_image_captcha'),
    path('logout', views.novel_logout, name='reverse_novel_logout'),
    path('change_password', views.novel_change_password, name='reverse_novel_change_password'),
]
