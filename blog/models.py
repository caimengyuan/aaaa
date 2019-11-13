import markdown

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, timezone
from django.utils.html import strip_tags

'''
    文章 id	标题	正文	发表时间	分类	标签
        1	title 1	text 1	2016-12-23	Django	Django 学习
        2	title 2	text 2	2016-12-24	Django	Django 学习
        3	title 3	text 3	2016-12-26	Python	Python 学习
    
    将分类和标签分别建表：
    分类 id	分类名
        1	Django
        2	Python
    标签 id	标签名
        1	Django 学习
        2	Python 学习
'''


# Create your models here.
# 分类表
class Category(models.Model):
    '''
    Category 即表名 分类名
    类的属性对应表格的列，属性名即列名
    '''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 标签表
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 文章表
class Post(models.Model):
    # 文章的标题
    title = models.CharField(max_length=70)
    # 文章正文
    # 存储较短的字符串可以使用charfield，一大段文本用TextField
    body = models.TextField()
    # 创建时间
    created_time = models.DateTimeField()
    # 最后一次修改时间
    modified_time = models.DateTimeField()
    # 文章摘要（可以为空，但是charfield要求必须存入数据，否则会报错）
    # 指定charfield的blank=true参数值后就可以允许空值了
    excerpt = models.CharField(max_length=200, blank=True)
    # 文章和分类是 多对一的关联关系 使用ForeinKey
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # 文章和标签是 多对多的关联关系 使用ManyToManyField
    tags = models.ManyToManyField(Tag, blank=True)
    # 文章作者
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 文章和作者是多对一的关系
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 新增views字段记录阅读量
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        # 自动获取摘要
        # 首先实例化一个markdown类，用于渲染body得文本
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # 先将Markdown文本渲染成HTML文本
        # strip_tags去掉HTML文本得全部HTML标签
        # 从文本摘取前54隔字符给excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']