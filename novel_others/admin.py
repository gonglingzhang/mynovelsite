from django.contrib import admin
from .models import NovelFriendLinksModel,NovelSuggestModel


# Register your models here.
class NovelFriendLinksModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'description', 'is_active',)
    search_fields = ('name', 'link')
    ordering = ('-create_time',)

class NovelSuggestModelAdmin(admin.ModelAdmin):
    list_display = ('suggest_title', 'suggest_content', 'is_active', 'is_processed','is_accepted','noaccept_reason')
    search_fields = ('suggest_title', 'suggest_content')
    ordering = ('-create_time',)



admin.site.register(NovelFriendLinksModel, NovelFriendLinksModelAdmin)
admin.site.register(NovelSuggestModel, NovelSuggestModelAdmin)