from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import NovelFriendLinksModel, NovelSuggestModel
from .form import NovelSuggestForm
from django.contrib import messages
from django.db.models import Q
# Create your views here.


def novel_about_us(request):
    return render(request, "novel_others/novel_about_us.html")


def novel_contact_us(request):
    return render(request, "novel_others/novel_contact_us.html")


@require_http_methods(["GET", "POST"])
@login_required
def novel_suggest_us(request):
    if request.method == "GET":
        return render(request, "novel_others/novel_suggest_us.html")
    else:
        form = NovelSuggestForm(request.POST)
        if form.is_valid():
            suggest_title = form.cleaned_data.get('suggest_title')
            suggest_content = form.cleaned_data.get('suggest_content')
            suggest = NovelSuggestModel(
                user=request.user,
                suggest_title=suggest_title,
                suggest_content=suggest_content,
            )
            suggest.save()
            messages.success(request, '建议提交成功！')
            return render(request, "novel_others/novel_suggest_us.html")
        else:
            return render(request, "novel_others/novel_suggest_us.html", {"form": form})


@login_required
def novel_my_suggestions(request):
    user = request.user
    suggestions = NovelSuggestModel.objects.filter(Q(user=user) & Q(is_active=1)).order_by('-create_time')
    return render(request, 'novel_others/novel_my_suggestions.html', {'suggestions': suggestions})


def novel_friend_links(request):
    friend_links = NovelFriendLinksModel.objects.filter(is_active=1)
    context = {
        'friend_links': friend_links,
    }
    return render(request, "novel_others/novel_friend_links.html", context)


def delete_suggest(request, suggest_id):
    user = request.user
    suggestions = NovelSuggestModel.objects.filter(Q(user=user) & Q(is_active=1)).order_by('-create_time')
    try:
        suggest = NovelSuggestModel.objects.get(id=suggest_id, user=user)
        suggest.is_active = 0  # 将建议标记为不活跃
        suggest.save()
        messages.success(request, '建议已成功删除！')
    except NovelSuggestModel.DoesNotExist:
        messages.error(request, '未找到该建议或您没有权限删除它。')
    return render(request, "novel_others/novel_my_suggestions.html", {'suggestions': suggestions})
