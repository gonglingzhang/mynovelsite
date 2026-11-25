from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .form import NovelCreateForm, NovelUpdateForm, NovelVolumeCreateForm, NovelVolumeEditForm, NovelChapterCreateForm
from .models import NovelCategoryModel, NovelLabelModel, NovelBasicInfoModel, NovelChapterModel, NovelContentModel, NovelVolumeModel, NovelBookMarkModel, NovelFavoriteModel, NovelLikeModel
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.dateformat import format
from bs4 import BeautifulSoup
from django.urls import reverse
from django.db.models import F, Q, Count

# Create your views here.


# 创建小说视图（小说作者）
@login_required
@require_http_methods(["GET", "POST"])
def novel_create(request):
    novel_category_use = NovelCategoryModel.objects.filter(category_status=1)
    novel_label_use = NovelLabelModel.objects.filter(label_status=1)
    if request.method == "GET":
        return render(request, "novel_content/novel_create.html", {
            "categories": novel_category_use,
            "labels": novel_label_use,
        })
    else:
        form = NovelCreateForm(request.POST, request.FILES)
        if form.is_valid():
            # 处理 POST 请求，获取用户提交的表单数据
            novel_name = request.POST.get("novel_name")
            novel_reader_gender = request.POST.get("novel_reader_gender")
            novel_category = request.POST.getlist("novel_category")
            novel_label = request.POST.getlist("novel_label")
            novel_intro = request.POST.get("novel_intro")
            # 这里可以添加保存数据到数据库的逻辑
            # 根据用户身份自动设置小说公开状态：管理员=公开，普通用户=非公开
            is_public = request.user.is_staff or request.user.is_superuser
            novel_basicinfo = NovelBasicInfoModel.objects.create(
                novel_name=novel_name,
                novel_author=request.user,
                novel_reader_gender=novel_reader_gender,
                novel_intro=novel_intro,
                novel_public=is_public,
            )
            novel_basicinfo.novel_category.set(novel_category)
            novel_basicinfo.novel_label.set(novel_label)
            novel_basicinfo.novel_home_imgpath = request.FILES.get("novel_cover")
            novel_basicinfo.save()
            NovelVolumeModel.objects.create(
                volume_name="第一卷",
                novel_basicinfo=novel_basicinfo,
            )
            return redirect('novel_content:reverse_my_novel_list')
        else:
            # 表单验证失败，重新渲染创建页面并显示错误信息
            return render(request, "novel_content/novel_create.html", {
                "form": form,
                "errors": form.errors,
                "categories": novel_category_use,
                "labels": novel_label_use,
            })


# 修改小说视图（小说作者）
@login_required
@require_http_methods(["GET", "POST"])
def novel_update(request, novel_id):
    novel_category_use = NovelCategoryModel.objects.filter(category_status=1)
    novel_label_use = NovelLabelModel.objects.filter(label_status=1)
    novel_basicinfo = get_object_or_404(NovelBasicInfoModel, id=novel_id, novel_author=request.user)
    if request.method == "GET":
        return render(request, "novel_content/novel_update.html", {
            "novel": novel_basicinfo,
            "categories": novel_category_use,
            "labels": novel_label_use,
        })
    else:
        form = NovelUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            # 处理 POST 请求，获取用户提交的表单数据
            novel_name = request.POST.get("novel_name")
            novel_reader_gender = request.POST.get("novel_reader_gender")
            novel_category = request.POST.getlist("novel_category")
            novel_label = request.POST.getlist("novel_label")
            novel_intro = request.POST.get("novel_intro")
            # 直接通过查询集更新，无需save()
            NovelBasicInfoModel.objects.filter(id=novel_id).update(
                novel_name=novel_name,
                novel_author=request.user,
                novel_reader_gender=novel_reader_gender,
                novel_intro=novel_intro,
            )
            novel_basicinfo.novel_category.set(novel_category)
            novel_basicinfo.novel_label.set(novel_label)
            if request.FILES.get("novel_cover"):
                # 直接赋值文件对象
                novel_basicinfo.novel_home_imgpath = request.FILES.get("novel_cover")
                # 调用实例save()方法触发文件保存
                novel_basicinfo.save()
            # 检查是否存在第一卷
            first_volume = NovelVolumeModel.objects.filter(novel_basicinfo=novel_basicinfo, volume_name="第一卷").first()
            if not first_volume:
                # 如果不存在第一卷，创建第一卷
                NovelVolumeModel.objects.create(
                    volume_name="第一卷",
                    novel_basicinfo=novel_basicinfo,
                )
            return redirect('novel_content:reverse_my_novel_list')
        else:
            # 表单验证失败，重新渲染创建页面并显示错误信息
            return render(request, "novel_content/novel_update.html", {
                "novel": novel_basicinfo,
                "form": form,
                "errors": form.errors,
                "categories": novel_category_use,
                "labels": novel_label_use,
            })


# 小说作者的小说列表（小说作者）
@login_required
def my_novel_list(request):
    user = request.user
    # 获取筛选条件 获取前端status的值，若为空则默认为'all'
    status = request.GET.get('status', 'all')
    if status == 'all':
        user_novels = NovelBasicInfoModel.objects.filter(novel_author=user).order_by('-novel_create_time')
    elif status == 'serializing':
        user_novels = NovelBasicInfoModel.objects.filter(novel_author=user).exclude(novel_status=1).order_by('-novel_create_time')
    elif status == 'completed':
        user_novels = NovelBasicInfoModel.objects.filter(novel_author=user, novel_status=1).order_by('-novel_create_time')
    else:
        user_novels = NovelBasicInfoModel.objects.filter(novel_author=user).order_by('-novel_create_time')
    content = {
        'user_novels': user_novels,
        'current_status': status  # 传递当前筛选状态到模板，确认用户点击的是哪个按钮，在前端根据这个值进行高亮显示
    }
    return render(request, 'novel_content/novel_my_novel_list.html', content)


# 具体某小说详情（小说作者）
@login_required
def my_novel_detail(request, novel_id):
    try:
        # 获取指定小说的基本信息
        novel = NovelBasicInfoModel.objects.get(id=novel_id, novel_author=request.user)
        # 获取该小说的章节列表
        # chapters = NovelChapterModel.objects.filter(
        #     novel_basicinfo=novel).order_by('chapter_no')
        latest_chapter = NovelChapterModel.objects.filter(novel_basicinfo=novel).order_by('-chapter_update_time').first()
        return render(request, "novel_content/novel_my_novel_detail.html", {
            "novel": novel,
            # "chapters": chapters,
            "latest_chapter": latest_chapter,
        })
    except NovelBasicInfoModel.DoesNotExist:
        messages.error(request, "小说不存在或您没有权限查看该小说。")
        return render(request, "novel_content/novel_my_novel_list.html")


# 给小说新增卷（小说作者）
@login_required
@require_http_methods(["POST"])
def novel_volume_create(request, novel_id):
    novel = get_object_or_404(NovelBasicInfoModel, id=novel_id, novel_author=request.user)
    form = NovelVolumeCreateForm(request.POST, novel_id=novel_id)
    if form.is_valid():
        volume_name = form.cleaned_data.get('volume_name')
        new_volume = NovelVolumeModel.objects.create(
            volume_name=volume_name,
            novel_basicinfo=novel,
        )
        # 使用 django.utils.dateformat 格式化日期
        formatted_time = format(new_volume.volume_create_time, 'Y年n月j日 H:i')
        return JsonResponse({
            'success': True,
            'message': f"新卷 '{new_volume.volume_name}' 创建成功！",
            'new_volume_name': new_volume.volume_name,
            'new_volume_create_time': formatted_time,
            'new_volume_id': new_volume.id
        })
    else:
        # 渲染表单页面并返回 HTML
        rendered_form = render(
            request, "novel_content/novel_my_novel_detail.html", {"novel": novel, "form": form})
        return JsonResponse({'success': False, 'html': rendered_form.content.decode('utf-8')})


# 删除小说卷（小说作者）
@login_required
def novel_del_volume(request, novel_id, volume_id):
    try:
        novel = NovelBasicInfoModel.objects.get(id=novel_id, novel_author=request.user)
        volume = NovelVolumeModel.objects.get(id=volume_id, novel_basicinfo=novel)
        volume.delete()
        return JsonResponse({'status': 'success', 'message': f"卷 '{volume.volume_name}' 删除成功！"})
    except NovelVolumeModel.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': "卷不存在或您没有权限删除该卷。"})


# 修改小说卷名字（小说作者）
@login_required
@require_http_methods(["POST"])
def novel_edit_volume(request, novel_id, volume_id):
    novel = get_object_or_404(NovelBasicInfoModel, id=novel_id, novel_author=request.user)
    volume = NovelVolumeModel.objects.get(id=volume_id, novel_basicinfo=novel)
    form = NovelVolumeEditForm(
        request.POST, novel_id=novel_id, volume_id=volume_id)
    if form.is_valid():
        new_volume_name = request.POST.get('volume_name')
        # 直接在数据库层面更新卷名称
        updated_count = NovelVolumeModel.objects.filter(
            novel_basicinfo=novel,
            id=volume_id,
        ).update(volume_name=new_volume_name)
        if updated_count > 0:
            return JsonResponse({
                'status': 'success',
                'message': f"卷 '{new_volume_name}' 更新成功！",
                'new_volume_name': new_volume_name
            })
        else:
            return JsonResponse({'status': 'error', 'message': "未找到符合条件的记录进行更新。"})
    else:
        errors = form.errors.as_data()
        error_message = ""
        for field, error_list in errors.items():
            for error in error_list:
                error_message += str(error) + " "
        return JsonResponse({'status': 'error', 'message': error_message.strip()})


# 创建新小说章节（小说作者）
@login_required
@require_http_methods(["GET", "POST"])
def novel_chapter_create(request, novel_id):
    novel = get_object_or_404(NovelBasicInfoModel, id=novel_id)
    if request.method == 'GET':
        return render(request, 'novel_content/novel_chapter_create.html', {
            'novel': novel,
        })
    else:
        form = NovelChapterCreateForm(request.POST)
        if form.is_valid():
            # chapter_name从前端传过来的时候是 第1章，clean之后变成1
            chapter_no = form.cleaned_data.get('chapter_name')
            chapter_intro = form.cleaned_data.get('chapter_intro')
            chapter_content = form.cleaned_data.get('chapter_content')
            novel_volume_id = request.POST.get('novel_volume')
            novel_volume = NovelVolumeModel.objects.get(id=novel_volume_id)
            if NovelChapterModel.objects.filter(novel_basicinfo=novel, novel_volume=novel_volume, chapter_no=int(chapter_no)).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': f"章节 第'{chapter_no}'章 已存在！",
                })
            else:
                # 使用 BeautifulSoup 提取纯文本
                soup = BeautifulSoup(chapter_content, 'html.parser')
                pure_text = soup.get_text()
                # 统计纯文本的字符数量
                chapter_word_count = len(pure_text)
                new_chapter = NovelChapterModel.objects.create(
                    chapter_no=int(chapter_no),
                    chapter_name='第'+str(chapter_no)+'章',
                    chapter_intro=chapter_intro,
                    chapter_word_count=chapter_word_count,
                    novel_basicinfo=novel,
                    novel_volume=novel_volume,
                )
                new_chapter_content = NovelContentModel.objects.create(
                    novel_basicinfo=novel,
                    chapter_basicinfo=new_chapter,
                    content=chapter_content,
                )
                novel.novel_word_count += chapter_word_count
                novel.save()
                return JsonResponse({
                    'code': 200,
                    'status': 'success',
                    'message': f"新章节 '{new_chapter.chapter_name}{new_chapter.chapter_intro}' 创建成功！",
                    'novel_id': novel_id,
                    'novel_volume_id': novel_volume_id,
                    'new_chapter_id': new_chapter.id,
                })
        else:
            errors = form.errors.as_data()
            error_message = ""
            for field, error_list in errors.items():
                for error in error_list:
                 # 从 ValidationError 对象中提取错误信息列表
                    messages = error.messages
                    for msg in messages:
                        # 将每个错误信息添加到 error_message 中
                        error_message += msg + " \n"
            return JsonResponse({'status': 'error', 'message': error_message})


# 完结小说（小说作者）
@login_required
@require_http_methods(["POST"])
def novel_finish(request, novel_id):
    novel = get_object_or_404(NovelBasicInfoModel, id=novel_id)
    novel.novel_status = 1
    novel.save()
    return JsonResponse({'status': 'success', 'message': '小说已完结！'})


# 连载小说（小说作者）
@login_required
@require_http_methods(["POST"])
def novel_loading(request, novel_id):
    novel = get_object_or_404(NovelBasicInfoModel, id=novel_id)
    novel.novel_status = 0
    novel.save()
    return JsonResponse({'status': 'success', 'message': '小说已可以继续连载！'})


# 删除小说（小说作者）
@login_required
@require_http_methods(["POST"])
def novel_del(request, novel_id):
    novel = get_object_or_404(NovelBasicInfoModel, id=novel_id)
    novel.delete()
    return JsonResponse({'status': 'success', 'message': '小说已删除！'})


# 删除章节（小说作者）
@login_required
@require_http_methods(["POST"])
def novel_chapter_del(request, novel_id, chapter_id):
    novel = get_object_or_404(NovelBasicInfoModel, id=novel_id)
    chapter = get_object_or_404(
        NovelChapterModel, id=chapter_id, novel_basicinfo=novel)
    chapter.delete()
    return JsonResponse({'status': 'success', 'message': '章节已删除！'})


# 编辑章节（小说作者）
@login_required
@require_http_methods(["GET", "POST"])
def novel_chapter_edit(request, novel_id, chapter_id):
    novel = get_object_or_404(NovelBasicInfoModel, id=novel_id)
    novel_chapter = get_object_or_404(NovelChapterModel, id=chapter_id)
    raw_chapter_word_count = novel_chapter.chapter_word_count
    novel_chapter_content = get_object_or_404(NovelContentModel, novel_basicinfo=novel, chapter_basicinfo=novel_chapter)
    if request.method == 'GET':
        return render(request, 'novel_content/novel_chapter_edit.html', {
            'novel': novel,
            'novel_chapter': novel_chapter,
            'novel_chapter_content': novel_chapter_content,
        })
    else:
        form = NovelChapterCreateForm(request.POST)
        if form.is_valid():
            # chapter_name从前端传过来的时候是 第1章，clean之后变成1
            chapter_no = form.cleaned_data.get('chapter_name')
            chapter_intro = form.cleaned_data.get('chapter_intro')
            chapter_content = form.cleaned_data.get('chapter_content')
            novel_volume_id = request.POST.get('novel_volume')
            novel_volume = NovelVolumeModel.objects.get(id=novel_volume_id)
            # 使用 BeautifulSoup 提取纯文本
            soup = BeautifulSoup(chapter_content, 'html.parser')
            pure_text = soup.get_text()
            # 统计纯文本的字符数量
            chapter_word_count = len(pure_text)

            # 检查是否会违反唯一约束
            duplicate_chapter = NovelChapterModel.objects.filter(
                novel_basicinfo=novel,
                novel_volume=novel_volume,
                chapter_name='第'+str(chapter_no)+'章'
            ).exclude(id=novel_chapter.id).exists()
            if duplicate_chapter:
                return JsonResponse({
                    'status': 'error',
                    'message': f"章节 第'{chapter_no}'章 已存在！",
                })
            # 更新章节信息
            novel_chapter.chapter_no = int(chapter_no)
            novel_chapter.chapter_name = '第'+str(chapter_no)+'章'
            novel_chapter.chapter_intro = chapter_intro
            novel_chapter.chapter_word_count = chapter_word_count
            novel_chapter.novel_volume = novel_volume
            novel_chapter.save()

            # 更新章节内容
            novel_chapter_content.novel_basicinfo = novel
            novel_chapter_content.chapter_basicinfo = novel_chapter
            novel_chapter_content.content = chapter_content
            novel_chapter_content.save()
            novel.novel_word_count -= raw_chapter_word_count
            novel.novel_word_count += chapter_word_count
            novel.save()
            return JsonResponse({
                'code': 200,
                'status': 'success',
                'message': f"新章节 '{novel_chapter.chapter_name}{novel_chapter.chapter_intro}' 创建成功！",
                'novel_id': novel_id,
                'novel_volume_id': novel_volume_id,
                'novel_chapter_id': novel_chapter.id,
            })
        else:
            errors = form.errors.as_data()
            error_message = ""
            for field, error_list in errors.items():
                for error in error_list:
                 # 从 ValidationError 对象中提取错误信息列表
                    messages = error.messages
                    for msg in messages:
                        # 将每个错误信息添加到 error_message 中
                        error_message += msg + " \n"
            return JsonResponse({'status': 'error', 'message': error_message})


# 小说详情（读者）
@require_http_methods(["GET"])
def reader_novel_detail(request, novel_id):
    user = request.user
    novel = get_object_or_404(NovelBasicInfoModel, id=novel_id)

    # 权限校验：非公开小说只有作者本人或管理员能看
    if not novel.novel_public:
        is_author = request.user.is_authenticated and novel.novel_author == request.user
        is_admin = request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
        if not (is_author or is_admin):
            messages.warning(request, f'《{novel.novel_name}》为非公开作品，仅作者可见。')
            return redirect('/')

    novel_chapter = NovelChapterModel.objects.filter(novel_basicinfo=novel)
    first_chapter = NovelChapterModel.objects.filter(novel_basicinfo=novel).order_by('chapter_update_time').first()
    latest_chapter = NovelChapterModel.objects.filter(novel_basicinfo=novel).order_by('-chapter_update_time').first()
    if request.user.is_authenticated:
        is_like = NovelLikeModel.objects.filter(user=user, novel=novel).exists()
        is_favorited = NovelFavoriteModel.objects.filter(user=user, novel=novel).exists()
    else:
        is_like = ''
        is_favorited = ''
    return render(request, 'novel_content/reader_novel_detail.html', {
        'novel': novel,
        'novel_chapter': novel_chapter,
        'first_chapter': first_chapter,
        'latest_chapter': latest_chapter,
        'is_like': is_like,
        'is_favorited': is_favorited,
    })


# 创建小说点赞视图（读者）
@login_required
@require_http_methods(["GET"])
def novel_book_like(request, novel_id):
    user = request.user
    novel = get_object_or_404(NovelBasicInfoModel, id=novel_id)
    is_like = NovelLikeModel.objects.filter(user=user, novel=novel).exists()
    if is_like:
        NovelLikeModel.objects.filter(user=user, novel=novel).delete()
        NovelBasicInfoModel.objects.filter(id=novel_id).update(novel_click_like=F('novel_click_like')-1)
    else:
        NovelLikeModel.objects.create(
            user=user,
            novel=novel,
        )
        NovelBasicInfoModel.objects.filter(id=novel_id).update(novel_click_like=F('novel_click_like')+1)
    return redirect(request.META.get('HTTP_REFERER', '/'))


# 创建小说收藏视图（读者）
@login_required
@require_http_methods(["GET"])
def novel_book_favorite(request, novel_id):
    user = request.user
    novel = get_object_or_404(NovelBasicInfoModel, id=novel_id)
    is_favorited = NovelFavoriteModel.objects.filter(user=user, novel=novel)
    if is_favorited:
        NovelFavoriteModel.objects.filter(user=user, novel=novel).delete()
        NovelBasicInfoModel.objects.filter(id=novel_id).update(novel_click_favorite=F('novel_click_favorite')-1)
    else:
        NovelFavoriteModel.objects.create(
            user=user,
            novel=novel,
        )
        NovelBasicInfoModel.objects.filter(id=novel_id).update(novel_click_favorite=F('novel_click_favorite')+1)
    return redirect(request.META.get('HTTP_REFERER', '/'))


# 小说章节详情（读者）
@require_http_methods(["GET"])
def reader_novel_chapter_detail(request, novel_id, volume_id, chapter_id):
    novel = get_object_or_404(NovelBasicInfoModel, id=novel_id)

    # 权限校验：非公开小说的章节只有作者本人或管理员能看
    if not novel.novel_public:
        is_author = request.user.is_authenticated and novel.novel_author == request.user
        is_admin = request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
        if not (is_author or is_admin):
            messages.warning(request, f'《{novel.novel_name}》为非公开作品，仅作者可见。')
            return redirect('/')
    novel_chapter = get_object_or_404(NovelChapterModel, id=chapter_id)
    novel_chapter_content = get_object_or_404(NovelContentModel, novel_basicinfo=novel, chapter_basicinfo=novel_chapter)
    first_chapter = NovelChapterModel.objects.filter(novel_basicinfo=novel, novel_volume=volume_id).order_by('chapter_no').first()
    is_first_chapter = novel_chapter == first_chapter
    last_chapter = NovelChapterModel.objects.filter(novel_basicinfo=novel, novel_volume=volume_id).order_by('chapter_no').last()
    is_last_chapter = novel_chapter == last_chapter
    user = request.user
    if request.user.is_authenticated:
        is_book_mark = NovelBookMarkModel.objects.filter(user=user, chapter_id=chapter_id).exists()
        # 获取当前用户的书签（假设已实现）
        user_bookmarks = NovelBookMarkModel.objects.filter(user=request.user, chapter__novel_basicinfo_id=novel_id).select_related('chapter')
    else:
        is_book_mark = ''
        user_bookmarks = ''
    # 新增：提取所有书签章节ID到列表
    bookmark_ids = [bookmark.chapter.id for bookmark in user_bookmarks]
    # 获取上一章节
    previous_chapter = NovelChapterModel.objects.filter(
        novel_basicinfo=novel,
        novel_volume=volume_id,
        chapter_no__lt=novel_chapter.chapter_no
    ).order_by('-chapter_no').first()

    # 获取下一章节
    next_chapter = NovelChapterModel.objects.filter(
        novel_basicinfo=novel,
        novel_volume=volume_id,
        chapter_no__gt=novel_chapter.chapter_no
    ).order_by('chapter_no').first()

   # 【新增】生成下一章 URL
    next_chapter_url = reverse('novel_content:reverse_reader_novel_chapter_detail', args=[novel.id, volume_id, next_chapter.id]) if next_chapter else None
    return render(request, 'novel_content/reader_novel_chapter_detail.html', {
        'novel': novel,
        'novel_chapter': novel_chapter,
        'novel_chapter_content': novel_chapter_content,
        'is_first_chapter': is_first_chapter,
        'is_last_chapter': is_last_chapter,
        'previous_chapter': previous_chapter,
        'next_chapter': next_chapter,
        'next_chapter_url': next_chapter_url,
        'is_book_mark': is_book_mark,
        'user_bookmarks': user_bookmarks,
        'bookmark_ids': bookmark_ids,
    })


# 创建书签视图（读者）
@login_required
@require_http_methods(["GET"])
def novel_book_mark(request, novel_id, chapter_id):
    user = request.user
    is_book_mark = NovelBookMarkModel.objects.filter(user=user, chapter_id=chapter_id)
    if is_book_mark:
        NovelBookMarkModel.objects.filter(user=user, chapter_id=chapter_id).delete()
    else:
        NovelBookMarkModel.objects.create(
            user=user,
            novel_id=novel_id,
            chapter_id=chapter_id,
        )
    return redirect(request.META.get('HTTP_REFERER', '/'))


# 创建分类视图（读者）
@login_required
@require_http_methods(["GET"])
def reader_novel_category(request):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    # ============ 1. 获取所有筛选参数 ============
    status = request.GET.get('status', 'all')          # all / serializing / completed
    reader = request.GET.get('reader', 'all')          # all / male / female
    category_id = request.GET.get('category', 'all')    # all / category_id (ManyToMany)
    label_id = request.GET.get('label', 'all')          # all / label_id (ManyToMany)
    order_by = request.GET.get('order', 'update')       # update / click / favorite / words
    keyword = request.GET.get('keyword', '').strip()   # 搜索关键词
    page = request.GET.get('page', '1')

    # ============ 2. 构建可见性过滤：公开小说 ∪ 当前用户自己的小说 ============
    visible_filter = Q(novel_public=1)
    if request.user.is_authenticated:
        visible_filter = visible_filter | Q(novel_author=request.user)

    # 获取字典数据（分类、标签 + 小说数量）
    base_for_count = NovelBasicInfoModel.objects.filter(visible_filter)
    # 用 ManyToMany 反向统计每个分类/标签下的公开小说数
    categories = NovelCategoryModel.objects.filter(
        category_status=1
    ).annotate(
        #     novel_count=Count('novelbasicinfomodel', filter=Q(novelbasicinfomodel__novel_public=1))
        # ).order_by('-novel_count')
        # labels = NovelLabelModel.objects.filter(
        #     label_status=1
        # ).annotate(
        #     novel_count=Count('novelbasicinfomodel', filter=Q(novelbasicinfomodel__novel_public=1))
        # ).order_by('-novel_count')
        novel_count=Count('category_basicinfo', filter=Q(category_basicinfo__novel_public=1))
    ).order_by('-novel_count')
    labels = NovelLabelModel.objects.filter(
        label_status=1
    ).annotate(
        novel_count=Count('label_basicinfo', filter=Q(label_basicinfo__novel_public=1))
    ).order_by('-novel_count')

    # ============ 3. 构建查询集 ============
    # 基础：只显示用户可见的小说（公开 ∪ 自己写的）
    queryset = NovelBasicInfoModel.objects.filter(visible_filter)

    # 3.1 关键词搜索（搜索小说名称和作者）
    if keyword:
        # from django.db.models import Q
        # queryset = queryset.filter(
        #     Q(novel_name__icontains=keyword) |
        #     Q(novel_author__username__icontains=keyword) |
        #     Q(novel_author__user_nickname__icontains=keyword) if hasattr(NovelUserModel, 'user_nickname') else Q(novel_name__icontains=keyword)
        # )
        queryset = queryset.filter(
            Q(novel_name__icontains=keyword) |
            Q(novel_author__username__icontains=keyword)
        )

    # 3.2 状态筛选
    if status == 'serializing':
        queryset = queryset.filter(novel_status=0)
    elif status == 'completed':
        queryset = queryset.filter(novel_status=1)

    # 3.3 读者性别筛选（男频/女频/全民向）
    if reader == 'male':
        queryset = queryset.filter(novel_reader_gender=1)
    elif reader == 'female':
        queryset = queryset.filter(novel_reader_gender=0)
    elif reader == 'universal':
        queryset = queryset.filter(novel_reader_gender=2)

    # 3.4 分类筛选（ManyToMany）
    if category_id != 'all' and category_id.isdigit():
        queryset = queryset.filter(novel_category__id=int(category_id)).distinct()

    # 3.5 标签筛选（ManyToMany）
    if label_id != 'all' and label_id.isdigit():
        queryset = queryset.filter(novel_label__id=int(label_id)).distinct()

    # 3.6 排序
    order_map = {
        'update': '-novel_update_time',
        'click': '-novel_click',
        'favorite': '-novel_click_favorite',
        'words': '-novel_word_count',
    }
    queryset = queryset.order_by(order_map.get(order_by, '-novel_update_time'))

    # ============ 4. 各筛选维度的数量统计 ============
    total_count = base_for_count.count()
    serializing_count = base_for_count.filter(novel_status=0).count()
    completed_count = base_for_count.filter(novel_status=1).count()
    male_count = base_for_count.filter(novel_reader_gender=1).count()
    female_count = base_for_count.filter(novel_reader_gender=0).count()
    universal_count = base_for_count.filter(novel_reader_gender=2).count()

    # ============ 5. 分页 ============
    per_page = 12  # 每页12本
    paginator = Paginator(queryset, per_page)
    try:
        novel_page = paginator.page(page)
    except PageNotAnInteger:
        novel_page = paginator.page(1)
    except EmptyPage:
        novel_page = paginator.page(paginator.num_pages)

    # ============ 6. 构造上下文 ============
    content = {
        # 当前页数据
        'novel_page': novel_page,
        'novels': novel_page.object_list,
        # 分页信息
        'is_paginated': paginator.num_pages > 1,
        'page_obj': novel_page,
        'total_pages': paginator.num_pages,
        # 字典数据
        'categories': categories,
        'labels': labels,
        # 当前筛选状态
        'current_status': status,
        'current_reader': reader,
        'current_category': category_id,
        'current_label': label_id,
        'current_order': order_by,
        'keyword': keyword,
        # 各维度数量统计
        'total_count': total_count,
        'serializing_count': serializing_count,
        'completed_count': completed_count,
        'male_count': male_count,
        'female_count': female_count,
        'universal_count': universal_count,
        # 分页 URL 参数（便于模板构建翻页链接）
        'base_query': f'status={status}&reader={reader}&category={category_id}&label={label_id}&order={order_by}&keyword={keyword}',
    }
    return render(request, 'novel_content/reader_novel_category.html', content)


# 读者的书架（读者）
@login_required
def reader_novel_favorite_list(request):
    user = request.user
    # 获取筛选条件 获取前端status的值，若为空则默认为'all'
    status = request.GET.get('status', 'all')

    # 先获取所有收藏，用于计算各状态数量（只需查询一次）
    all_favorites = NovelFavoriteModel.objects.filter(user=user).select_related('novel')
    total_count = all_favorites.count()
    completed_count = all_favorites.filter(novel__novel_status=1).count()
    serializing_count = total_count - completed_count

    # 根据筛选条件获取当前页数据
    if status == 'all':
        favorite_novels = all_favorites.order_by('-favorite_time')
    elif status == 'serializing':
        favorite_novels = all_favorites.exclude(novel__novel_status=1).order_by('-favorite_time')
    elif status == 'completed':
        favorite_novels = all_favorites.filter(novel__novel_status=1).order_by('-favorite_time')
    else:
        favorite_novels = all_favorites.order_by('-favorite_time')

    # 获取用户收藏的小说对象集合（去重并保持收藏时间排序）
    favorite_novels = [favorite.novel for favorite in favorite_novels]

    content = {
        'favorite_novels': favorite_novels,
        'current_status': status,
        'total_count': total_count,
        'serializing_count': serializing_count,
        'completed_count': completed_count,
    }
    return render(request, 'novel_content/reader_novel_favorite_list.html', content)
