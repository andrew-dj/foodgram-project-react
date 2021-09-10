from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=100)
    measurement_unit = models.CharField('Единица измерения', max_length=20)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    BLUE = '#4A61DD'
    GREEN = '#49B64E'
    ORANGE = '#E26C2D'
    PURPLE = '#8775D2'
    YELLOW = '#F9A62B'

    colors = [
        (BLUE, 'Синий'),
        (GREEN, 'Зелёный'),
        (ORANGE, 'Оранжевый'),
        (PURPLE, 'Фиолетовый'),
        (YELLOW, 'Жёлтый')
    ]

    name = models.CharField('Название тега', max_length=200, unique=True)
    color = models.CharField('Код цвета RGB', choices=colors, max_length=7)
    slug = models.SlugField('Slug', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Subscriptions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE,
                                   verbose_name='Подписчик',
                                   verbose_name_plural='Подписчики',
                                   related_name='subscribing'
                                   )

    class Meta:
        odering = ['id'],
        verbose_name = 'Подписка',
        verbose_name_plural = 'Подписки',
        constraints = models.UniqueConstraint(
            fields=['user', 'subscriber'],
            name='Unique subscription checker'
        )


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Автор',
                             related_name='recipes'
                             )
    name = models.CharField('Название', max_length=200)
    image = models.ImageField('Изображение', upload_to='recipes/')
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='Ingredient_amount',
                                         related_name='recipes',
                                         verbose_name='Ингредиенты'
                                         )
    tag = models.ManyToManyField(Tag,
                                 verbose_name='Тэг',
                                 verbose_name_plural='Тэги'
                                 )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[validators.MinValueValidator(1,
                    message='Время приготовления не может быть менее 1 минуты!'
                                                 )
                    ],
        verbose_name='Время приготовления в минутах'
    )

    class Meta:
        ordering = ['-id'],
        verbose_name = 'Рецепт',
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientsAmount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   verbose_name='Ингредиент')
    amount = models.PositiveSmallIntegerField('Количество')

    class Meta:
        verbose_name = 'Количество ингредиента',
        verbose_name_plural = 'Количества ингредиентов'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorite',
                               verbose_name='Рецепт')

    class Meta:
        ordering = ['-id'],
        verbose_name = 'Избранный рецепт',
        verbose_name_plural = 'Избранные рецепты'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='incart',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт')

    class Meta:
        ordering = ['-id'],
        verbose_name = 'Рецепт в корзине',
        verbose_name_plural = 'Рецепты в корзине'
