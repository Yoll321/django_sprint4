from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
help_text_dict = {
    'is_published': 'Снимите галочку, чтобы скрыть публикацию.',
    'slug': """Идентификатор страницы для URL; разрешены символы\
 латиницы, цифры, дефис и подчёркивание.""",
    'pub_date': """Если установить дату и время в будущем — можно делать\
 отложенные публикации."""
}


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True,
    )
    is_published = models.BooleanField(
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
    title = models.CharField('Заголовок', max_length=256)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=help_text_dict['pub_date']
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
    )
    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title
