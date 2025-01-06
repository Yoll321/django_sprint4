from django import forms

from blog.models import Post, Comment
from django.contrib.auth import get_user_model


User = get_user_model()


class PostForm(forms.ModelForm):
    """Форма для создания или обновления поста."""

    class Meta:
        model = Post
        fields = (
            'title',
            'text',
            'category',
            'location',
            'pub_date',
        )


class ProfileForm(forms.ModelForm):
    """Форма для создания или обновления профиля."""

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


class CommentForm(forms.ModelForm):
    """Форма для написания комментария."""

    class Meta:
        model = Comment
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({
            'style': 'height: 100px; width: 600px;'
        })
