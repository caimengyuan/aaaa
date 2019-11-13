from django import template
from comments.forms import CommentForm

register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'post': post,
    }


@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    # 获取和post关联的评论列表：即调用xxx_set属性来获取一个类似于objects的模型管理器
    # xxx_set中xxx为关联模型的类名
    # post.comment_set.all()等价于Comment.objects.filter(post=post)
    # comment_list = post.comment_set.all().order_by('-created_time')
    comment_list = post.comment_set.all()
    comment_count = comment_list.count()
    return{
        'comment_list': comment_list,
        'comment_count': comment_count,
    }