"""reviews models."""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from api.constants import CUT_OFF_MAX_LENGTH, MAX_LENGTH_NAME, MAX_LENGTH_SLUG
from django.contrib.auth import get_user_model

from .validators import validate_year


User = get_user_model()


class BaseCategoryGenre(models.Model):
    """Abstract class for Category and Genre."""

    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH_NAME,
    )
    slug = models.SlugField(
        'Слаг',
        max_length=MAX_LENGTH_SLUG,
        unique=True
    )

    class Meta:
        """CategoryGenre meta class."""

        abstract = True
        ordering = ('name',)

    def __str__(self):
        """Return  name."""
        return self.name


class Category(BaseCategoryGenre):
    """Title category model."""

    class Meta(BaseCategoryGenre.Meta):
        """Category model metaclass."""

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseCategoryGenre):
    """Title genre model."""

    class Meta(BaseCategoryGenre.Meta):
        """Genre model metaclass."""

        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Title model."""

    name = models.CharField(
        'Название произведения',
        max_length=MAX_LENGTH_NAME
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genres')
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=[validate_year],
        db_index=True
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=False)

    class Meta:
        """Title model metaclass."""

        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('year',)

    def __str__(self):
        """Return title name."""
        return self.name


class ReviewCommentsAbstract(models.Model):
    """Abstract class for common elements."""

    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        """ReviewCommentsAbstract meta class."""

        abstract = True
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:CUT_OFF_MAX_LENGTH]


class Review(ReviewCommentsAbstract):
    """Review model."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, 'Оценка не может быть меньше 1!'),
            MaxValueValidator(10, 'Оценка не может быть больше 10!'),
        ]
    )

    class Meta(ReviewCommentsAbstract.Meta):
        """Review meta class."""

        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review_per_user_per_title'
            )
        ]


class Comment(ReviewCommentsAbstract):
    """Comments model for reviews."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta(ReviewCommentsAbstract.Meta):
        """Comment meta class."""

        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
