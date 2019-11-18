import markdown
import re
from .models import Post, Category, Tag
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.core.paginator import Paginator
from markdown.extensions.toc import TocExtension
'''
    首先接受了一个名为 request 的参数，这个 request 就是 Django 为我们封装好的 HTTP 请求，
它是类 HttpRequest 的一个实例。然后我们便直接返回了一个 HTTP 响应给用户，这个 HTTP 响应也是
Django 帮我们封装好的，它是类 HttpResponse 的一个实例，只是我们给它传了一个自定义的字符串参数。
'''
# Create your views here.


def index(request, page):
    # return HttpResponse('welcome')
    # return render(request, 'blog/index.html',
    #               context={'title': '我的博客首页',
    #                        'welcome': '欢迎访问'})
    # post_list = Post.objects.all().order_by('-created_time')
    post_list = Post.objects.all()
    # 对数据进行分页
    paginator = Paginator(post_list, 5)
    # 获取第page页的内容
    try:
        page = int(page)
    except Exception as e:
        page = 1

    if page > paginator.num_pages:
        page = 1

    # 获取第page页的page实例对象
    blog = paginator.page(page)

    # todo:进行页码的控制，一个页面上最多显示5个页码
    # 1.总页数少于5页，页面上显示所有页码
    # 2.如果当前页是前3页，显示1-5页
    # 3.如果当前页是后3页，显示后五页
    # 4.其他情况，显示当前页的前2页，当前页，当前页的后2页
    num_pages = paginator.num_pages
    if num_pages < 5:
        page = range(1, num_pages+1)
    elif page <= 3:
        page = range(1, 6)
    elif num_pages - page <= 2:
        page = range(num_pages-4, num_pages+1)
    else:
        page = range(page-2, page+3)

    # 组织模板上下文
    context = {'blog': blog, 'page': page, 'post_list': post_list}
    return render(request, 'blog/index.html', context)


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 记得在顶部引入 markdown 模块
    # post.body = markdown.markdown(post.body,
    #                               extensions=[
    #                                  'markdown.extensions.extra',
    #                                  'markdown.extensions.codehilite',
    #                                  'markdown.extensions.toc',
    #                               ])
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 'markdown.extensions.toc',
        # 目录生成
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    # post.toc = md.toc
    # 判断是否有目录
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html', context={'post': post})


# 归档页面
def archive(request, year, month):
    # post_list = Post.objects.filter(created_time__year=year,
    #                                 created_time__month=month).order_by('-created_time')
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month)
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 分类页面
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    # post_list = Post.objects.filter(category=cate).order_by('-created_time')
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 标签页面
def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    # post_list = Post.objects.filter(tags=t).order_by('-created_time')
    post_list = Post.objects.filter(tags=t)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 阅读量+1
    post.increase_views()

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return render(request, 'blog/detail.html', context={'post': post})


