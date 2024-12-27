from django.shortcuts import render, get_object_or_404
from datetime import datetime

from .models import Post, Category


def index(request):
    template_name = 'blog/index.html'
    n = 5
    post_list = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=datetime.now()
    ).order_by('-pub_date')[:n]
    context = {
        'post_list': post_list
    }
    return render(request, template_name, context)


def post_detail(request, id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lt=datetime.now()
        ),
        id=id
    )
    context = {'post': post}
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(
            is_published=True
        ),
        slug=category_slug
    )
    post_list = Post.objects.filter(
        is_published=True,
        pub_date__lt=datetime.now(),
        category__slug=category_slug,
    ).order_by('-pub_date')
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, template_name, context)
