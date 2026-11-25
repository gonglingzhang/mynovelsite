from django.contrib import admin

# Register your models here.
from .models import NovelCategoryModel, NovelLabelModel, NovelBasicInfoModel


# Register your models here.
class NovelCategoryModelAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_status')
    search_fields = ('category_name',)


class NovelLabelModelAdmin(admin.ModelAdmin):
    list_display = ('label_name', 'label_status')
    search_fields = ('label_name',)


class NovelBasicInfoModelAdmin(admin.ModelAdmin):
    # 列表页显示的字段
    list_display = (
        'novel_name', 'novel_author', 'novel_reader_gender',
        'novel_public', 'novel_status', 'novel_word_count',
        'novel_create_time', 'novel_update_time',
    )

    # 可点击的链接字段（其余字段可编辑）
    list_display_links = ('novel_name',)

    # 列表页可直接行内编辑的字段
    list_editable = ('novel_public', 'novel_status')

    # 搜索字段
    search_fields = ('novel_name', 'novel_author__username',)

    # 侧边筛选栏
    list_filter = (
        'novel_public', 'novel_status',
        'novel_reader_gender',
        'novel_category', 'novel_label',
        'novel_create_time',
    )

    # 每页数量
    list_per_page = 20

    # 按日期导航
    date_hierarchy = 'novel_create_time'

    # 列表页排序
    ordering = ('-novel_create_time',)

    # 编辑页字段分组布局
    fieldsets = (
        ('基本信息', {
            'fields': ('novel_name', 'novel_author', 'novel_intro', 'novel_home_imgpath')
        }),
        ('分类标签', {
            'fields': ('novel_category', 'novel_label', 'novel_reader_gender')
        }),
        ('发布设置', {
            'fields': ('novel_public', 'novel_status'),
            'description': '管理员可在此设置小说是否公开。公开=所有人可见，非公开=仅作者本人可见。'
        }),
        ('统计数据', {
            'fields': ('novel_click', 'novel_click_like', 'novel_click_favorite', 'novel_word_count'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('novel_create_time', 'novel_update_time'),
            'classes': ('collapse',)
        }),
    )

    # 只读字段（自动生成的字段）
    readonly_fields = ('novel_create_time', 'novel_update_time')


admin.site.register(NovelCategoryModel, NovelCategoryModelAdmin)
admin.site.register(NovelLabelModel, NovelLabelModelAdmin)
admin.site.register(NovelBasicInfoModel, NovelBasicInfoModelAdmin)
