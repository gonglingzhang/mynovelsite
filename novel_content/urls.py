from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse
from . import views
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import time
from datetime import datetime
from django.urls import re_path
import logging

logger = logging.getLogger(__name__)


@csrf_exempt  # 临时禁用 CSRF 验证，在生产环境中应使用合适的 CSRF 保护方式
def chapter_upload_image(request):
    if request.method == 'POST' and request.FILES.get('upload_image_name'):
        image = request.FILES['upload_image_name']
        image.name = str(datetime.now().strftime(
            '%Y%m%d%H%M%S')) + '_' + image.name
        # 假设上传到项目的 media 目录下，你可以根据实际情况修改
        media_root = 'media/chapter_upload_image'
        if not os.path.exists(media_root):
            os.makedirs(media_root)
        image_path = os.path.join(media_root, image.name)
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        # 返回图片的访问 URL，假设你的媒体文件通过 /media/chapter_upload_image/ 访问
        image_url = f'/media/chapter_upload_image/{image.name}'
        return JsonResponse({
            "errno": 0,
            "data": {
                "url": image_url,
            }
        })
    return JsonResponse({'errno': 1, 'message': '上传失败'}, status=400)


@csrf_exempt  # 临时禁用 CSRF 验证，在生产环境中应使用合适的 CSRF 保护方式
def chapter_upload_video(request):
    if request.method == 'POST' and request.FILES.get('upload_video_name'):
        video = request.FILES['upload_video_name']
        video.name = str(datetime.now().strftime(
            '%Y%m%d%H%M%S')) + '_' + video.name
        # 假设上传到项目的 media 目录下，你可以根据实际情况修改
        media_root = 'media/chapter_upload_video'
        if not os.path.exists(media_root):
            os.makedirs(media_root)
        video_path = os.path.join(media_root, video.name)
        with open(video_path, 'wb+') as destination:
            for chunk in video.chunks():
                destination.write(chunk)
        # 返回图片的访问 URL，假设你的媒体文件通过 /media/chapter_upload_video/ 访问
        video_url = f'/media/chapter_upload_video/{video.name}'
        return JsonResponse({
            "errno": 0,
            "data": {
                "url": video_url,
            }
        })
    return JsonResponse({'errno': 1, 'message': '上传失败'}, status=400)


app_name = "novel_content"
urlpatterns = [
    path('novel_create/', views.novel_create, name='reverse_novel_create'),
    path('novel_update/<int:novel_id>', views.novel_update, name='reverse_novel_update'),
    path('my_novel_list/', views.my_novel_list, name='reverse_my_novel_list'),
    path('reader_novel_favorite_list/', views.reader_novel_favorite_list, name='reverse_reader_novel_favorite_list'),
    path('my_novel_detail/<int:novel_id>/', views.my_novel_detail, name='reverse_my_novel_detail'),
    path('novel_volume_create/<int:novel_id>/', views.novel_volume_create, name='reverse_novel_volume_create'),
    path('novel_del_volume/<int:novel_id>/<int:volume_id>/', views.novel_del_volume, name='reverse_novel_del_volume'),
    path('novel_edit_volume/<int:novel_id>/<int:volume_id>/', views.novel_edit_volume, name='reverse_novel_edit_volume'),
    path('novel_chapter_create/<int:novel_id>/', views.novel_chapter_create, name='reverse_novel_chapter_create'),
    path('novel_finish/<int:novel_id>/', views.novel_finish, name='reverse_novel_finish'),
    path('novel_loading/<int:novel_id>/', views.novel_loading, name='reverse_novel_loading'),
    path('novel_del/<int:novel_id>/', views.novel_del, name='reverse_novel_del'),
    path('novel_chapter_del/<int:novel_id>/<int:chapter_id>/', views.novel_chapter_del, name='reverse_novel_chapter_del'),
    path('novel_chapter_edit/<int:novel_id>/<int:chapter_id>/', views.novel_chapter_edit, name='reverse_novel_chapter_edit'),
    path('media/chapter_upload_image/', chapter_upload_image, name='reverse_chapter_upload_image'),
    path('media/chapter_upload_video/', chapter_upload_video, name='reverse_chapter_upload_video'),
    path('reader_novel_detail/<int:novel_id>/', views.reader_novel_detail, name='reverse_reader_novel_detail'),
    path('reader_novel_chapter_detail/<int:novel_id>/<int:volume_id>/<int:chapter_id>/', views.reader_novel_chapter_detail, name='reverse_reader_novel_chapter_detail'),
    path('novel_book_mark/<int:novel_id>/<int:chapter_id>/', views.novel_book_mark, name='reverse_novel_book_mark'),
    path('novel_book_like/<int:novel_id>/', views.novel_book_like, name='reverse_novel_book_like'),
    path('novel_book_favorite/<int:novel_id>/', views.novel_book_favorite, name='reverse_novel_book_favorite'),
    path('reader_novel_category/', views.reader_novel_category, name='reverse_reader_novel_category'),
]
