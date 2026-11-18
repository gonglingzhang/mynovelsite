from django import forms
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from .models import NovelSuggestModel


class NovelSuggestForm(forms.Form):
    suggest_title = forms.CharField(required=True, min_length=2, max_length=100, label='建议主题', error_messages={
        'required': '请输入建议主题。',
        'min_length': '建议主题长度不能少于2个字符。',
        'max_length': '建议主题长度不能超过100个字符。',
    })
   # 将 forms.Textarea 作为 widget 参数传递给 forms.CharField
    suggest_content = forms.CharField(required=True, label='建议内容', error_messages={
        'required': '请输入建议内容。',
    },
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50})
    )
