from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import NovelUserModel, NovelCaptchaModel


@admin.register(NovelCaptchaModel)
class NovelCaptchaModelAdmin(admin.ModelAdmin):
    """验证码模型管理"""
    list_display = ('email', 'captcha', 'created_time', 'updated_time')
    search_fields = ('email',)
    list_filter = ('created_time',)
    readonly_fields = ('created_time', 'updated_time')


class NovelUserModelAdmin(BaseUserAdmin):
    """自定义用户管理 - 继承Django的UserAdmin"""

    # 列表页显示的字段
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_staff', 'is_superuser', 'is_active', 'active',
        'last_login', 'created_time'
    )

    # 列表页可点击的字段链接
    list_display_links = ('username', 'email')

    # 可搜索的字段
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # 右侧过滤栏字段
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'active',
        'groups', 'created_time', 'last_login'
    )

    # 每页显示数量
    list_per_page = 20

    # 可直接在列表页编辑的字段
    list_editable = ('is_active', 'active')

    # 只读字段（在编辑页）
    readonly_fields = ('last_login', 'created_time', 'updated_time')

    # 编辑页面的字段分组布局
    fieldsets = (
        ('基本信息', {
            'fields': ('username', 'email', 'password')
        }),
        ('个人信息', {
            'fields': ('first_name', 'last_name', 'extra1', 'extra2')
        }),
        ('权限设置', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'active',
                'groups', 'user_permissions'
            ),
            'classes': ('collapse',)  # 可折叠
        }),
        ('时间信息', {
            'fields': ('last_login', 'created_time', 'updated_time'),
            'classes': ('collapse',)
        }),
    )

    # 新增用户页面的字段（密码单独处理）
    add_fieldsets = (
        ('创建新用户', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('个人信息', {
            'classes': ('collapse',),
            'fields': ('first_name', 'last_name', 'extra1', 'extra2')
        }),
        ('权限设置', {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')
        }),
    )

    # 列表页排序
    ordering = ('-created_time',)

    # 按日期层级导航
    date_hierarchy = 'created_time'

    # 保存时处理密码哈希
    def save_model(self, request, obj, form, change):
        """保存用户时自动处理密码哈希"""
        if change:  # 编辑用户时
            if 'password' in form.changed_data:
                obj.set_password(obj.password)
        else:  # 新增用户时
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


# 注册用户模型
admin.site.register(NovelUserModel, NovelUserModelAdmin)


# 自定义Admin站点标题
admin.site.site_header = '小说网站管理后台'
admin.site.site_title = '小说网站管理'
admin.site.index_title = '欢迎使用小说网站管理后台'
