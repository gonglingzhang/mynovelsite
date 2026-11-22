"""
URL configuration for mynovelsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from . import settings, views
from django.conf.urls.static import static
from django.contrib import admin


admin.site.site_header = "星群小说网站管理系统"       # 页面顶部的大字（最主要！截图看到的）
admin.site.site_title = "星群小说网站管理系统"    # 浏览器标签标题
admin.site.index_title = "星群小说网站管理系统"   # 后台首页下面的标题


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('404/', views.error_404, name='404'),
    path('auth/', include('novel_authentication.urls', namespace="novel_auth")),
    path('others/', include('novel_others.urls', namespace="novel_others")),
    path('content/', include('novel_content.urls', namespace="novel_content")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
