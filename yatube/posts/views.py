from re import template
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Post, Group, User

SYMBOLS_PER_PAGE = 10


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context) 


@login_required
def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.order_by('-pub_date')[:SYMBOLS_PER_PAGE]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)

def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    full_name = author.get_full_name()
    context = {
        'page_obj': page_obj,
        'post_list': post_list,
        'full_name': full_name,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)
    user = get_object_or_404(User, id=post.author.id)
    full_name = user.get_full_name()
    post_count = user.posts.select_related().count()
    context = {
        'post': post,
        'user': user,
        'full_name': full_name,
        'post_count': post_count,
    }
    return render(request, template, context)


def post_create(request):
    template= 'posts/create_post.html'
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, template, {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect(f'profile/{request.user.username}/')


def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect(
            'posts:post_detail', post_id
        )
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect(
            'posts:post_detail', post_id
        )
    return render(request, template, {
        'form': form, 'is_edit': True, 'post': post
    })

