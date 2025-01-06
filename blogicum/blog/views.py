from datetime import datetime

from typing import Any

from django.contrib.auth.decorators import login_required
from django.db.models.base import Model as Model
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import \
    (CreateView, ListView, UpdateView, DetailView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .models import Post, Category, Comment
from .forms import PostForm, ProfileForm, CommentForm


User = get_user_model()


class PostListView(ListView):
    """Список постов для главной страницы"""

    model = Post
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lt=datetime.now()
        ).order_by('-pub_date')
        paginator = Paginator(post_list, 10)
        page_num = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_num)
        return context


class CategoryListView(ListView):
    """Список постов категории."""

    model = Post
    template_name = 'blog/category.html'
    paginate_by = 10  # Устанавливаем количество объектов на странице

    def get_queryset(self):
        # Получаем значение category_slug из kwargs
        category_slug = self.kwargs.get('category_slug')

        queryset = Post.objects.filter(
            is_published=True,
            category__slug=category_slug,
            category__is_published=True,
            pub_date__lt=datetime.now()
        )

        return queryset.order_by('-pub_date')


class PostCreateView(CreateView, LoginRequiredMixin):
    """Добавление поста."""

    template_name = 'blog/create.html'
    form_class = PostForm
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        new_post = form.save(commit=False)
        new_post.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    """Показ отдельного поста."""

    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.order_by('created_at')
        return context
    

@login_required
def edit_post(request, post_id):
    """Редактирует запись блога."""
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id)
    form = PostForm(
        request.POST, files=request.FILES or None, instance=post)
    if form.is_valid():
        post.save()
        return redirect('blog:post_detail', post_id)
    form = PostForm(instance=post)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def delete_post(request, post_id):
    """Удаляет запись блога."""
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id)
    if request.method == 'POST':
        form = PostForm(request.POST or None, instance=post)
        post.delete()
        return redirect('blog:index')
    form = PostForm(instance=post)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


class DeletePost(DeleteView, LoginRequiredMixin):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(self.request.POST or None,
                                   instance=self.object)
        return context


class ProfileUpdateView(UpdateView):
    """Изменение профиля."""

    template_name = 'blog/user.html'
    form_class = ProfileForm

    def get_object(self) -> Model:
        return self.request.user

    def get_success_url(self) -> str:
        return reverse_lazy('blog:profile', args=(self.request.user.username,))


class ProfileListView(ListView, LoginRequiredMixin):
    """Отображение личного профиля."""

    template_name = 'blog/profile.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        posts = Post.objects.filter(
            author=self.request.user
        ).order_by('-pub_date')
        paginator = Paginator(posts, 10)
        page_num = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_num)
        return context


@login_required
def add_comment(request, post_pk):
    """Добавляет комментарий к записи."""
    post = get_object_or_404(Post, id=post_pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect('blog:post_detail', post_pk)


@login_required
def edit_comment(request, post_pk, com_pk):
    """Редактирует комментарий."""
    comment = get_object_or_404(Comment, id=com_pk)
    if request.user != comment.author:
        return redirect('blog:post_detail', post_pk)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_pk)
    form = CommentForm(instance=comment)
    context = {'form': form, 'comment': comment}
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_pk, com_pk):
    """Удаляет комментарий."""
    comment = get_object_or_404(Comment, id=com_pk)
    if request.user != comment.author:
        return redirect('blog:post_detail', post_pk)
    if request.method == "POST":
        comment.delete()
        return redirect('blog:post_detail', post_pk)
    context = {'comment': comment}
    return render(request, 'blog/comment.html', context)
