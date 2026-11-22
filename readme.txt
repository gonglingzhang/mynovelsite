0.从0开始创建django项目：
cmd中运行
django-admin startproject MYBLOG
创建django框架，默认包含app：MYBLOG

1.django项目下额外创建新的app：
创建新的app：
python manage.py startapp NEWBLOG

2.运行django项目：
python manage.py runserver

3.新建项目中settings.py文件常见修改：
3.0
import os

3.1 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'template_html',  # 添加自定义应用
]

3.2
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 添加模板目录
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'django.templatetags.static',  # 添加静态文件标签
            ],
        },
    },
]

3.3
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # 添加静态文件目录
]

# Media files (user-uploaded files)
# https://docs.djangoproject.com/en/5.0/topics/files/
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 添加媒体文件目录

3.4
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'database_name',  # 数据库名称
        'USER': 'root',  # 数据库用户名
        'PASSWORD': 'root',  # 数据库密码   
        'HOST': 'localhost',  # 数据库主机地址
        'PORT': '3306',  # 数据库端口
    }
}


4.新建项目中urls.py文件常见修改：

4.0
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include, reverse
from template_html import views
from django.conf import settings
from django.conf.urls.static import static

4.1
urlpatterns = [
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 增加媒体文件


5. ORM模型
5.1 
首先确保app在settings.py中已经添加了自定义应用 INSTALLED_APPS

5.2
使用 python manage.py makemigrations 创建模型，结果会在app下生成migrations文件夹，文件夹下会有对应class的脚本

5.3
使用 python manage.py migrate 运行app下migrations文件夹中的脚本，同步到数据库中。

6.创建管理员账户
首先运行5，进行数据库迁移。
然后创建管理员命令：
 py manage.py createsuperuser
按照提示进行依次输入：
用户名: gonglingzhang
邮箱地址: 1113684931@qq.com
Password:P@ssw0rd

后台管理员登录页面：
http://127.0.0.1:8000/admin/
使用用户名，密码进行登录。不是邮箱和密码。
