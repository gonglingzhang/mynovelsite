"""
WSGI config for mynovelsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

path = '/home/gonglingzhang/mynovelsite'  # 替换为你的项目路径
if path not in sys.path:
    sys.path.append(path)
# 这里【mynovelsite】是包含settings.py的文件夹名字！
os.environ['DJANGO_SETTINGS_MODULE'] = 'mynovelsite.settings'


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mynovelsite.settings')

application = get_wsgi_application()
