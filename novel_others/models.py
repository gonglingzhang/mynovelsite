from django.db import models
from novel_authentication.models import NovelUserModel

# Create your models here.


class NovelSuggestModel(models.Model):
    # 使用 ForeignKey 关联到 NovelUserModel 的 email 字段
    user = models.ForeignKey(
        NovelUserModel,
        on_delete=models.CASCADE,  # 当关联用户被删除时，建议也会被删除
        to_field='email',  # 指定关联到 NovelUserModel 的 email 字段
        verbose_name='用户邮箱',
        db_comment='关联用户的邮箱'
    )
    suggest_title = models.CharField(max_length=100, verbose_name='建议标题')
    suggest_content = models.TextField(verbose_name='建议内容')
    is_active = models.BooleanField(
        default=1, verbose_name='是否起效', db_comment='1是起效')
    is_processed = models.BooleanField(
        default=0, verbose_name='是否处理', db_comment='1是已处理，0是未处理')
    process_time = models.DateTimeField(auto_now=True, verbose_name='处理时间')
    is_accepted = models.BooleanField(
        default=0, verbose_name='是否采纳', db_comment='1是已采纳，0是未采纳')
    noaccept_reason = models.CharField(null=True, blank=True,
                                       max_length=2000, verbose_name='未采纳原因', db_comment='未采纳原因')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    extra1 = models.CharField(
        null=True, blank=True, max_length=100, verbose_name='额外字段1', db_comment='备用字段1')
    extra2 = models.CharField(
        null=True, blank=True, max_length=100, verbose_name='额外字段2', db_comment='备用字段2')
    extra3 = models.CharField(
        null=True, blank=True, max_length=100, verbose_name='额外字段3', db_comment='备用字段3')

    class Meta:
        verbose_name = '用户建议'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']


class NovelFriendLinksModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='友情链接名称')
    link = models.CharField(max_length=100, verbose_name='友情链接地址(以http开头)')
    description = models.CharField(max_length=100, verbose_name='友情链接描述')
    is_active = models.BooleanField(
        default=1, verbose_name='是否起效', db_comment='1是起效')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
