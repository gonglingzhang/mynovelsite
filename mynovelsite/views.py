# 网站名称：星群小说网站管理系统V1.0
# 版本号：V1.0
# 著作权人：公令璋
# 开发完成日期：2026年11月18日
from django.shortcuts import render
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from novel_content.models import NovelBasicInfoModel, NovelFavoriteModel, NovelLikeModel


def most_neary_liked_novels(last_days, user=None):
    """获取最近 N 天内的热门小说，同时过滤非公开小说。
    user 为当前请求用户（可为匿名），用于包含用户自己的非公开小说。
    """
    thirty_days_ago = timezone.now() - timedelta(days=last_days)
    # 筛选 30 天内的收藏记录，按小说分组统计收藏数
    hot_novels = NovelLikeModel.objects.filter(like_time__gte=thirty_days_ago).values('novel').annotate(like_count=Count('id'))
    novel_ids = [item['novel'] for item in hot_novels]

    # 构建可见性过滤
    visible_filter = Q(novel_public=1)
    if user and user.is_authenticated:
        visible_filter = visible_filter | Q(novel_author=user)

    novels = NovelBasicInfoModel.objects.filter(id__in=novel_ids).filter(visible_filter).order_by('-novel_click_like')
    return novels


def index(request):
    # 构建可见性过滤：公开小说 ∪ 当前用户自己的小说（未登录则只有公开）
    visible_filter = Q(novel_public=1)
    if request.user.is_authenticated:
        visible_filter = visible_filter | Q(novel_author=request.user)

    # 最新的10本小说
    latest_novels = NovelBasicInfoModel.objects.filter(visible_filter).order_by('-novel_create_time')[:10]
    # 热门小说（点赞最多）
    hot_novels = NovelBasicInfoModel.objects.filter(visible_filter).order_by('-novel_click_like')[:10]
    # 月度热门（近30天点赞）
    hot_30days_novels = most_neary_liked_novels(30, request.user)[:10]
    # 男生精选
    male_liked_novels = NovelBasicInfoModel.objects.filter(visible_filter, novel_reader_gender=1).order_by('-novel_click_like')[:10]
    # 女生精选
    female_liked_novels = NovelBasicInfoModel.objects.filter(visible_filter, novel_reader_gender=0).order_by('-novel_click_like')[:10]
    # 全民向精选
    universal_liked_novels = NovelBasicInfoModel.objects.filter(visible_filter, novel_reader_gender=2).order_by('-novel_click_like')[:10]
    # 网站推荐（点击最多）
    website_suggest_novels = NovelBasicInfoModel.objects.filter(visible_filter).order_by('-novel_click')[:6]

    context = {
        'latest_novels': latest_novels,
        'hot_novels': hot_novels,
        'hot_30days_novels': hot_30days_novels,
        'male_liked_novels': male_liked_novels,
        'female_liked_novels': female_liked_novels,
        'universal_liked_novels': universal_liked_novels,
        'website_suggest_novels': website_suggest_novels,
    }
    return render(request, 'index.html', context=context)


def test(request):
    return render(request, 'test.html')


def error_404(request):
    return render(request, '404.html')
