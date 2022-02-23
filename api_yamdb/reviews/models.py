from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    """Модель кастомного пользователя"""

    AUTHENTICATED = 'user'
    MODERATOR = 'moderator'
    ADMINISTRATOR = 'admin'
    ROLE_CHOICES = [
        (AUTHENTICATED, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMINISTRATOR, 'Администратор'),
    ]

    role = models.CharField(verbose_name='Роль', max_length=10,
                            choices=ROLE_CHOICES, default=AUTHENTICATED)
    bio = models.TextField(verbose_name='Биография', blank=True, null=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_registration'
            )
        ]

    @property
    def is_admin(self):
        return self.role == User.ADMINISTRATOR

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR


class Category(models.Model):
    """Модель категорий (типы) произведений («Фильмы», «Книги», «Музыка»)"""

    name = models.CharField(max_length=256, verbose_name='Имя категории')
    slug = models.SlugField(max_length=50, unique=True,
                            verbose_name='Слаг категории')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        indexes = [
            models.Index(fields=['name', ]),
        ]

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведения"""

    name = models.CharField(max_length=256, verbose_name='Имя жанра')
    slug = models.SlugField(max_length=50, unique=True,
                            verbose_name='Слаг жанра')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        indexes = [
            models.Index(fields=['name', ]),
        ]


class Title(models.Model):
    """
    Модель произведения, к которым пишут отзывы (определённый фильм, книга
    или песенка)
    """
    name = models.CharField(max_length=500, verbose_name='Название')
    year = models.PositiveIntegerField(verbose_name='Год выпуска',
                                       validators=[
                                           MinValueValidator(1000),
                                           MaxValueValidator(
                                               datetime.now().year)
                                       ])
    description = models.TextField(verbose_name='Описание', blank=True,
                                   null=True)
    genre = models.ManyToManyField(Genre,
                                   related_name='titles',
                                   verbose_name='Жанры произведения')
    category = models.ForeignKey(Category,
                                 related_name='titles',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='Категория произведения')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    """Модель отзыва о произведение"""

    text = models.TextField(verbose_name='текст отзыва')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)
    author = models.ForeignKey(User, verbose_name='Автор публикации',
                               related_name='reviews',
                               on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews', null=True,
                              verbose_name='Наименование произведения')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка произведения',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]


class Comment(models.Model):
    """Модель комментария к отзыву"""

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='автор комментария')
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments', verbose_name='отзыв')
    text = models.TextField(verbose_name='текст комментария')
    pub_date = models.DateTimeField(verbose_name='дата публикации',
                                    auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        indexes = [
            models.Index(fields=['text', ]),
            models.Index(fields=['author', ]),
        ]
