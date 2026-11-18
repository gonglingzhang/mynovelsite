from django import forms
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from .models import NovelCategoryModel, NovelLabelModel, NovelBasicInfoModel, NovelVolumeModel, NovelChapterModel, NovelContentModel
from django.core.files.images import get_image_dimensions
from PIL import Image  # 导入 Pillow 库
from novel_authentication.models import NovelUserModel
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404


class NovelCreateForm(forms.Form):
    novel_name = forms.CharField(required=True, min_length=2, max_length=100, label='作品名称', error_messages={
        'required': '请输入作品名称。',
        'min_length': '作品名称长度不能少于2个字符。',
        'max_length': '作品名称长度不能超过100个字符。',
    })
    novel_cover = forms.ImageField(label='作品封面', required=False)
    novel_reader_gender = forms.ChoiceField(required=True, choices=[(0, '女频'), (1, '男频'), (2, '全民向')], label='目标读者', error_messages={
        'required': '请选择目标读者',
    })
    novel_category = forms.ModelMultipleChoiceField(
        required=True,
        queryset=NovelCategoryModel.objects.all(),  # 查询所有分类
        label='作品分类',
        error_messages={
            'required': '请至少选择一个作品分类',
        },
        widget=forms.CheckboxSelectMultiple  # 使用复选框作为前端展示
    )
    novel_label = forms.ModelMultipleChoiceField(
        required=True,
        queryset=NovelLabelModel.objects.all(),  # 查询所有分类
        label='作品标签',
        error_messages={
            'required': '请至少选择一个选择作品标签',
        },
        widget=forms.CheckboxSelectMultiple  # 使用复选框作为前端展示
    )
    novel_intro = forms.CharField(required=True, min_length=2, max_length=300, label='作品简介', error_messages={
        'required': '请输入作品简介。',
        'min_length': '作品简介长度不能少于2个字符。',
        'max_length': '作品简介长度不能超过300个字符。',
    },
    )

    def clean_novel_name(self):
        novel_name = self.cleaned_data.get('novel_name')
        if NovelBasicInfoModel.objects.filter(novel_name=novel_name).exists():
            raise forms.ValidationError('作品名称已存在，请更换其他名称。')
        return novel_name

    def clean_novel_cover(self):
        novel_cover = self.cleaned_data.get('novel_cover')
        if novel_cover:
            try:
                # 使用 Pillow 库打开图片
                img = Image.open(novel_cover)
                try:
                    img.verify()  # 验证图片完整性
                except Exception as e:
                    print(f"图片验证出错: {e}")  # 打印详细错误信息
                    raise forms.ValidationError('上传的文件不是有效的图片。')
                finally:
                    img.seek(0)  # 重置文件指针
                w, h = img.size
                if w > 1400 or h > 1800:
                    raise forms.ValidationError('封面图片尺寸过大，请上传不超过600x1000的图片。')
            except FileNotFoundError:
                raise forms.ValidationError('未找到上传的图片文件。')
        return novel_cover


class NovelUpdateForm(forms.Form):
    novel_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)
    novel_name = forms.CharField(required=True, min_length=2, max_length=100, label='作品名称', error_messages={
        'required': '请输入作品名称。',
        'min_length': '作品名称长度不能少于2个字符。',
        'max_length': '作品名称长度不能超过100个字符。',
    })
    novel_cover = forms.ImageField(label='作品封面', required=False)
    novel_reader_gender = forms.ChoiceField(required=True, choices=[(0, '女频'), (1, '男频')], label='目标读者', error_messages={
        'required': '请选择目标读者',
    })
    novel_category = forms.ModelMultipleChoiceField(
        required=True,
        queryset=NovelCategoryModel.objects.all(),  # 查询所有分类
        label='作品分类',
        error_messages={
            'required': '请至少选择一个作品分类',
        },
        widget=forms.CheckboxSelectMultiple  # 使用复选框作为前端展示
    )
    novel_label = forms.ModelMultipleChoiceField(
        required=True,
        queryset=NovelLabelModel.objects.all(),  # 查询所有分类
        label='作品标签',
        error_messages={
            'required': '请至少选择一个选择作品标签',
        },
        widget=forms.CheckboxSelectMultiple  # 使用复选框作为前端展示
    )
    novel_intro = forms.CharField(required=True, min_length=2, max_length=300, label='作品简介', error_messages={
        'required': '请输入作品简介。',
        'min_length': '作品简介长度不能少于2个字符。',
        'max_length': '作品简介长度不能超过300个字符。',
    },
    )

    def clean_novel_name(self):
        novel_basicinfo = get_object_or_404(NovelBasicInfoModel, id=self.cleaned_data.get('novel_id'))
        novel_name = self.cleaned_data.get('novel_name')
        if NovelBasicInfoModel.objects.filter(novel_name=novel_name).exists() and novel_basicinfo.novel_name != novel_name:
            raise forms.ValidationError('作品名称已存在，请更换其他名称。')
        return novel_name

    def clean_novel_cover(self):
        novel_cover = self.cleaned_data.get('novel_cover')
        if novel_cover:
            try:
                # 使用 Pillow 库打开图片
                img = Image.open(novel_cover)
                try:
                    img.verify()  # 验证图片完整性
                except Exception as e:
                    print(f"图片验证出错: {e}")  # 打印详细错误信息
                    raise forms.ValidationError('上传的文件不是有效的图片。')
                finally:
                    img.seek(0)  # 重置文件指针
                w, h = img.size
                if w > 1400 or h > 1800:
                    raise forms.ValidationError('封面图片尺寸过大，请上传不超过600x1000的图片。')
            except FileNotFoundError:
                raise forms.ValidationError('未找到上传的图片文件。')
        return novel_cover


class NovelVolumeCreateForm(forms.Form):
    volume_name = forms.CharField(required=True, min_length=2, max_length=100, label='卷名称', error_messages={
        'required': '请输入卷名称。',
        'min_length': '卷名称长度不能少于2个字符。',
        'max_length': '卷名称长度不能超过100个字符。',
    })

    def __init__(self, *args, **kwargs):
        # 从 kwargs 中获取 novel_id 参数
        self.novel_id = kwargs.pop('novel_id', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        volume_name = cleaned_data.get('volume_name')
        if self.novel_id and volume_name:
            try:
                novel = NovelBasicInfoModel.objects.get(id=self.novel_id)
                if NovelVolumeModel.objects.filter(novel_basicinfo=novel, volume_name=volume_name).exists():
                    raise forms.ValidationError('该作品下已存在相同名称的卷，请更换其他名称。')
            except NovelBasicInfoModel.DoesNotExist:
                raise forms.ValidationError('该作品不存在')
        return cleaned_data


class NovelVolumeEditForm(forms.Form):
    volume_name = forms.CharField(required=True, min_length=2, max_length=100, label='卷名称', error_messages={
        'required': '请输入卷名称。',
        'min_length': '卷名称长度不能少于2个字符。',
        'max_length': '卷名称长度不能超过100个字符。',
    })

    def __init__(self, *args, **kwargs):
        # 从 kwargs 中获取 novel_id 参数
        self.novel_id = kwargs.pop('novel_id', None)
        self.volume_id = kwargs.pop('volume_id', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        volume_name = cleaned_data.get('volume_name')
        if self.novel_id and volume_name:
            try:
                novel = NovelBasicInfoModel.objects.get(id=self.novel_id)
                if NovelVolumeModel.objects.filter(novel_basicinfo=novel, volume_name=volume_name).exists():
                    raise forms.ValidationError('该作品下已存在相同名称的卷，请更换其他名称。')
            except NovelBasicInfoModel.DoesNotExist:
                raise forms.ValidationError('该作品不存在')
        return cleaned_data


class NovelChapterCreateForm(forms.Form):
    chapter_name = forms.CharField(required=True,  label='章节名称')
    chapter_intro = forms.CharField(required=True, min_length=1, max_length=50, label='章节介绍', error_messages={
        'required': '请输入章节名称。',
        'min_length': '章节名称长度不能少于1个字符。',
        'max_length': '章节名称长度不能超过50个字符。',
    })
    chapter_content = forms.CharField(required=True, label='章节内容',)

    def clean_chapter_name(self):
        chapter_name = self.cleaned_data.get('chapter_name').replace('第', '').replace('章', '')
        if not chapter_name:
            raise forms.ValidationError('请输入章节号。')
        return chapter_name

    def clean_chapter_content(self):
        chapter_content = self.cleaned_data.get('chapter_content')
        if chapter_content:
            soup = BeautifulSoup(chapter_content, 'html.parser')
            pure_text = soup.get_text()
            if len(pure_text) < 10:
                raise forms.ValidationError('章节内容长度不能少于10个字符。')
        return chapter_content
