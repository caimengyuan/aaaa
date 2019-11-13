from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import CommentForm
from blog.models import Post

# Create your views here.
@require_POST
def comment(request, post_pk):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来
    post = get_object_or_404(Post, pk=post_pk)

    # django将用户提交的数据封装在request.POST中，这是以给类字典对象
    # 我们利用这些数据构造了CommentFrom的实例，这样就生成了一个绑定了用户提交数据的表单
    form = CommentForm(request.POST)

    # 当调用form.is_valid()方法时，django自动帮我们检查表单的数据是否符合格式要求
    if form.is_valid():
        # 合法，调用表单的save方法保存数据到数据库
        # comment=False的作用仅仅利用表单的数据生成Comment模型类的实例，但还不保存评论数据到数据库
        comment = form.save(commit=False)

        # 将评论和被评论的文章关联起来
        comment.post = post

        # 最终将评论数据保存近数据库，调用模型实例的save方法
        comment.save()

        messages.add_message(request, messages.SUCCESS, '评论发表成功(＾Ｕ＾)ノ~ＹＯ', extra_tags='success')
        # 重定向到post的详情页，实际当redirect函数接收一个模型的实例时，它会调用这个模型实例的get_absolute_url方法
        # 然后重定向到get_absolute_url方法返回的URL
        return redirect(post)

    # 不合法，渲染一个预览页面，用于展示表单的错误
    # 这里被评论的文章post也传给了模板，因为我们需要根据post来生成表单的提交地址
    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(request, messages.ERROR, '评论发表失败，请修改表单中的错误后重新提交哟', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)