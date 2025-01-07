from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),

    path('category/<slug:category_slug>/',
         views.CategoryListView.as_view(),
         name='category_posts'),

    path('create_post/',
         views.create_post,
         name='create_post'),

    path('edit_profile/',
         views.ProfileUpdateView.as_view(),
         name='edit_profile'),

    path('profile/<str:name>',
         views.ProfileListView.as_view(),
         name='profile'),

    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),

    path('posts/<int:pk>/edit/', views.edit_post, name='edit_post'),

    path('posts/<int:pk>/delete/',
         views.delete_post,
         name='delete_post'),

    path('posts/<int:post_pk>/comment',
         views.add_comment,
         name='add_comment'),

    path('posts/<int:post_pk>/edit_comment/<int:com_pk>/',
         views.edit_comment,
         name='edit_comment'),

    path('posts/<int:post_pk>/delete_comment/<int:com_pk>/',
         views.delete_comment,
         name='delete_comment'),
]
