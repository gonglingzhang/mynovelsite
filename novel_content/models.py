from django.db import models
from novel_authentication.models import NovelUserModel
import time
from datetime import datetime
from django.core.files.images import get_image_dimensions


# 该函数用于生成文件上传的存储路径。
def up_to(instance, filename):
    if instance.novel_author:
        # 若模型实例的 novel_author 字段存在，则获取该作者的用户 ID
        user_id = instance.novel_author.id
    else:
        # 若 novel_author 为空，可设置一个默认值，如 'unknown'
        user_id = 'unknown'
    # 使用时间戳和原始文件名组合成新的文件名，并与用户 ID 拼接成完整的存储路径
    return '/'.join(['novel', str(user_id), str(datetime.now().strftime('%Y%m%d%H%M%S')) + '_' + filename])


# 小说分类字典
class NovelCategoryModel(models.Model):
    category_name = models.CharField(max_length=255, verbose_name='分类名称')
    category_status = models.BooleanField(default=1, verbose_name='是否起效', db_comment='1表示有效')

    class Meta:
        verbose_name = '小说分类'
        verbose_name_plural = verbose_name


# 小说标签字典
class NovelLabelModel(models.Model):
    label_name = models.CharField(max_length=255, verbose_name='标签名称')
    label_status = models.BooleanField(default=1, verbose_name='是否起效', db_comment='1表示有效')

    class Meta:
        verbose_name = '小说标签'
        verbose_name_plural = verbose_name


# 小说基本信息表
class NovelBasicInfoModel(models.Model):
    novel_name = models.CharField(unique=True, max_length=255, verbose_name='小说名称',
                                  error_messages={
                                      'unique': '小说名称已存在，请更换其他名称。',
                                      'max_length': '小说名称不能超过255个字符。',
                                  })
    novel_author = models.ForeignKey(NovelUserModel, on_delete=models.CASCADE, related_name='written_novels', verbose_name='小说作者')
    novel_category = models.ManyToManyField(NovelCategoryModel, related_name='category_basicinfo', verbose_name='小说分类')
    novel_label = models.ManyToManyField(NovelLabelModel, related_name='label_basicinfo', verbose_name='小说标签')
    novel_intro = models.TextField(verbose_name='小说简介')
    novel_home_imgpath = models.ImageField(null=True, blank=True, upload_to=up_to, verbose_name='小说首页图片路径')
    # 目标读者: 0=女频, 1=男频, 2=全民向
    READER_GENDER_CHOICES = [
        (0, '女频'),
        (1, '男频'),
        (2, '全民向'),
    ]
    novel_reader_gender = models.IntegerField(
        default=1,
        choices=READER_GENDER_CHOICES,
        verbose_name='目标读者',
        db_comment='0女频,1男频,2全民向',
    )
    novel_public = models.BooleanField(default=1, verbose_name='是否公开', db_comment='0表示不公开,1表示公开')
    novel_status = models.BooleanField(default=0, verbose_name='是否完结', db_comment='0表示连载,1表示完结')
    # novel_active = models.BooleanField(default=1, verbose_name='是否可读', db_comment='0表示不可读,1表示可读')
    novel_click = models.IntegerField(default=0, verbose_name='小说点击量')
    novel_click_like = models.IntegerField(default=0, verbose_name='小说点赞量')
    novel_click_favorite = models.IntegerField(default=0, verbose_name='小说收藏量(书架)')
    novel_word_count = models.IntegerField(default=0, verbose_name='小说总字数')
    novel_create_time = models.DateTimeField(auto_now_add=True, verbose_name='小说创建时间')
    novel_update_time = models.DateTimeField(auto_now=True, verbose_name='小说更新时间')

    class Meta:
        verbose_name = '小说基本信息'
        verbose_name_plural = verbose_name


# 小说卷表
class NovelVolumeModel(models.Model):
    volume_no = models.IntegerField(default=0, verbose_name='卷序号', db_comment='卷序号(1,2,3)')
    volume_name = models.CharField(max_length=255, verbose_name='卷名称')
    # volume_active = models.BooleanField(default=1, verbose_name='卷是否可读', db_comment='0表示不可读,1表示可读')
    volume_click = models.IntegerField(default=0, verbose_name='卷点击量')
    volume_click_favorite = models.IntegerField(default=0, verbose_name='卷收藏量')
    volume_create_time = models.DateTimeField(auto_now_add=True, verbose_name='卷创建时间')
    volume_update_time = models.DateTimeField(auto_now=True, verbose_name='卷更新时间')
    novel_basicinfo = models.ForeignKey(NovelBasicInfoModel, on_delete=models.CASCADE, related_name='novel_volume', verbose_name='小说id')

    class Meta:
        verbose_name = '小说卷信息'
        verbose_name_plural = verbose_name
        # 设置 novel_basicinfo 和 volume_name 组合唯一
        unique_together = ('novel_basicinfo', 'volume_name')


# 小说章节信息表
class NovelChapterModel(models.Model):
    chapter_no = models.IntegerField(default=0, verbose_name='章节顺序', db_comment='章节顺序(1234)')
    chapter_name = models.CharField(max_length=255, verbose_name='章节名称', db_comment='章节名称(第一章)')
    chapter_intro = models.TextField(verbose_name='章节简介', db_comment='章节简介(百鬼夜行)')
    # chapter_active = models.BooleanField(default=1, verbose_name='章节是否可读', db_comment='0表示不可读,1表示可读')
    chapter_click = models.IntegerField(default=0, verbose_name='章节点击量')
    chapter_click_favorite = models.IntegerField(default=0, verbose_name='章节收藏量')
    chapter_word_count = models.IntegerField(default=0, verbose_name='章节字数')
    chapter_create_time = models.DateTimeField(auto_now_add=True, verbose_name='章节创建时间')
    chapter_update_time = models.DateTimeField(auto_now=True, verbose_name='章节更新时间')
    novel_basicinfo = models.ForeignKey(NovelBasicInfoModel, on_delete=models.CASCADE, related_name='novel_chapter', verbose_name='小说id')
    novel_volume = models.ForeignKey(NovelVolumeModel, on_delete=models.CASCADE, related_name='volume_chapter', verbose_name='卷id')

    class Meta:
        verbose_name = '小说章节信息'
        verbose_name_plural = verbose_name
        unique_together = ('novel_basicinfo', 'novel_volume', 'chapter_name')


# 小说章节内容表
class NovelContentModel(models.Model):
    novel_basicinfo = models.ForeignKey(NovelBasicInfoModel, on_delete=models.CASCADE, related_name='novel_content', verbose_name='小说id')
    chapter_basicinfo = models.ForeignKey(NovelChapterModel, on_delete=models.CASCADE, related_name='chapter_content', verbose_name='章节id')
    content = models.TextField(verbose_name='章节内容')


# 点赞小说
class NovelLikeModel(models.Model):
    user = models.ForeignKey(NovelUserModel, on_delete=models.CASCADE, related_name='like_novels', verbose_name='用户')
    novel = models.ForeignKey(NovelBasicInfoModel, on_delete=models.CASCADE, related_name='like_by', verbose_name='小说')
    like_time = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        unique_together = ('user', 'novel')  # 确保一个用户对同一本小说只点赞一次
        verbose_name = '小说点赞'
        verbose_name_plural = verbose_name


# 收藏小说
class NovelFavoriteModel(models.Model):
    user = models.ForeignKey(NovelUserModel, on_delete=models.CASCADE, related_name='favorited_novels', verbose_name='用户')
    novel = models.ForeignKey(NovelBasicInfoModel, on_delete=models.CASCADE, related_name='favorited_by', verbose_name='小说')
    favorite_time = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        unique_together = ('user', 'novel')  # 确保一个用户对同一本小说只能收藏一次
        verbose_name = '小说收藏'
        verbose_name_plural = verbose_name


# 小说书签
class NovelBookMarkModel(models.Model):
    user = models.ForeignKey(NovelUserModel, on_delete=models.CASCADE, verbose_name='用户')
    novel = models.ForeignKey(NovelBasicInfoModel, on_delete=models.CASCADE, verbose_name='小说id')
    chapter = models.ForeignKey(NovelChapterModel, on_delete=models.CASCADE, verbose_name='章节id')
    book_mark_create_time = models.DateTimeField(auto_now_add=True, verbose_name='书签创建时间')

    class Meta:
        verbose_name = '小说书签'
        verbose_name_plural = verbose_name
