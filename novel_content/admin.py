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
    list_display = ('novel_name', 'novel_author')
    search_fields = ('novel_name', 'novel_author',)


admin.site.register(NovelCategoryModel, NovelCategoryModelAdmin)
admin.site.register(NovelLabelModel, NovelLabelModelAdmin)
admin.site.register(NovelBasicInfoModel, NovelBasicInfoModelAdmin)
