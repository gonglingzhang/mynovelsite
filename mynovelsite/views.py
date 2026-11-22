# 网站名称：星群小说网站管理系统V1.0
# 版本号：V1.0
# 著作权人：公令璋
# 开发完成日期：2026年11月18日
from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from novel_content.models import NovelBasicInfoModel, NovelFavoriteModel, NovelLikeModel


def most_neary_liked_novels(last_days):
    # 获取 30 天前的日期
    thirty_days_ago = timezone.now() - timedelta(days=last_days)
    # 筛选 30 天内的收藏记录，按小说分组统计收藏数
    hot_novels = NovelLikeModel.objects.filter(like_time__gte=thirty_days_ago).values('novel').annotate(like_count=Count('id'))
    # 获取小说信息
    novel_ids = [item['novel'] for item in hot_novels]
    novels = NovelBasicInfoModel.objects.filter(id__in=novel_ids).order_by('-novel_click_like')
    return novels


def index(request):
    # 获取最新的10本小说
    latest_novels = NovelBasicInfoModel.objects.all().order_by('-novel_create_time')[:10]
    hot_novels = NovelBasicInfoModel.objects.all().order_by('-novel_click_like')[:10]
    print([i.novel_name for i in hot_novels])
    hot_30days_novels = most_neary_liked_novels(30)[:10]
    male_liked_novels = NovelBasicInfoModel.objects.filter(novel_reader_gender=1).order_by('-novel_click_like')[:10]
    female_liked_novels = NovelBasicInfoModel.objects.filter(novel_reader_gender=0).order_by('-novel_click_like')[:10]
    universal_liked_novels = NovelBasicInfoModel.objects.filter(novel_reader_gender=2).order_by('-novel_click_like')[:10]
    website_suggest_novels = NovelBasicInfoModel.objects.all().order_by('-novel_click')[:6]
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
