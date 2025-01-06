from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()
help_text_dict = {
    'is_published': 'Снимите галочку, чтобы скрыть публикацию.',
    'slug': """Идентификатор страницы для URL; разрешены символы\
 латиницы, цифры, дефис и подчёркивание.""",
    'pub_date': """Если установить дату и время в будущем — можно делать\
 отложенные публикации."""
}


class BaseModel(models.Model):
    created_at = models.DateTimeField(      # Устанавливается автоматически
        verbose_name='Добавлено',
        auto_now_add=True,
    )
    is_published = models.BooleanField(     # Устанавливается администратором
        verbose_name='Опубликовано',
        default=True,
        help_text=help_text_dict['is_published'],
    )

    class Meta:
        abstract = True


class Location(BaseModel):
    name = models.CharField(
        verbose_name='Название места',
        max_length=256,
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Category(BaseModel):
    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=help_text_dict['slug'],
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Post(BaseModel):
    # Доступно пользователю
    title = models.CharField('Заголовок', max_length=256)
    text = models.TextField('Текст')    # Доступно пользователю
    pub_date = models.DateTimeField(    # Доступно пользователю
        'Дата и время публикации',
        help_text=help_text_dict['pub_date']
    )
    author = models.ForeignKey(         # Устанавливается автоматически
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
    )
    location = models.ForeignKey(       # Доступно пользователю
        Location,
        verbose_name='Местоположение',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    category = models.ForeignKey(       # Доступно пользователю
        Category,
        verbose_name='Категория',
        null=True,
        on_delete=models.SET_NULL,
    )
    image = models.ImageField(
        'Картинка',
        upload_to='post_images',
        blank=True,
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


class Comment(BaseModel):
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    post = models.ForeignKey(
        Post,
        verbose_name='Комментируемый пост',
        on_delete=models.CASCADE,
        related_name='comments',
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментариии'
        ordering = ('created_at',)

    def __str__(self) -> str:
        return self.text[:settings.REPRESENTATION_LENGTH]
