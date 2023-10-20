from django.core import validators
from django.db import models
from django.utils import timezone

from foodgram.constants import (
    AmountIngredientLimit,
    RecipeLimit,
    IngredientLimit,
    TagLimit, RecipeValidate, AmountIngredientValidate
)
from users.models import CustomUser


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        verbose_name='Автор',
        null=True,
        related_name='recipes'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=RecipeLimit.MAX_LEN_NAME.value,
    )
    image = models.ImageField(
        verbose_name='Фото рецепта',
        upload_to='recipes/image/'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Тег',
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        verbose_name='Игредиенты',
        related_name='recipes',
        through='AmountIngredient'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        default=RecipeLimit.DEFAULT,
        validators=(
            validators.MinValueValidator(
                RecipeValidate.MIN_COOKING_TIME.value,
                f'Минимальное время приготовления'
                f' {RecipeValidate.MIN_COOKING_TIME.value} мин.',
            ),
            validators.MaxValueValidator(
                RecipeValidate.MAX_COOKING_TIME.value,
                f'Максимальное вреся приготовления '
                f'{RecipeValidate.MAX_COOKING_TIME.value} мин.',
            ),
        ),
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=TagLimit.MAX_LEN_NAME.value,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=TagLimit.MAX_LEN_COLOR.value,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Url',
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=IngredientLimit.MAX_LEN_NAME.value
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=IngredientLimit.MAX_LEN_MEASUREMENT_UNIT.value
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_title_measurement_unit'
            )
        ]

    def __str__(self):
        return (f'{self.name[:IngredientLimit.INGREDIENT_TITLE.value]}'
                f' {self.measurement_unit}')


class AmountIngredient(models.Model):
    ingredients = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        related_name='recipe'
    )
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE,
                               related_name='ingredient')
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        default=AmountIngredientLimit.DEFAULT,
        validators=(
            validators.MinValueValidator(
                AmountIngredientValidate.MIN_AMOUNT_INGREDIENTS.value,
                f'Минимальное кол-во ингредиентов '
                f'{AmountIngredientValidate.MIN_AMOUNT_INGREDIENTS.value}',
            ),
            validators.MaxValueValidator(
                AmountIngredientValidate.MAX_AMOUNT_INGREDIENTS.value,
                'Слишком много ингредиентов!',
            ),
        ),
    )

    class Meta:
        verbose_name = 'Кол-во ангредиента'
        verbose_name_plural = 'Кол-во ингредиентов'

    def __str__(self):
        return f'{self.ingredients} + {self.recipe}'


class FavoriteShoppingCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.user} add {self.recipe}'


class Favorite(FavoriteShoppingCart):
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        default_related_name = 'favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_favorite'
            )
        ]


class Cart(FavoriteShoppingCart):
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        default_related_name = 'shopping_list'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_cart'
            )
        ]
