from django.conf import settings
from django.db import models

CustomUser = settings.AUTH_USER_MODEL
INGREDIENT_TITLE = 10


class Recipe(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,
                               null=True, related_name='recipes')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='recipes/image/')
    text = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='recipes')
    ingredients = models.ManyToManyField('Ingredient',
                                         related_name='recipes',
                                         through='AmountIngredient')
    cooking_time = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=60, unique=True)
    color = models.CharField(max_length=16, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=60)
    measurement_unit = models.CharField(max_length=10)

    class Meta:
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_title_measurement_unit'
            )
        ]

    def __str__(self):
        return f'{self.name[:INGREDIENT_TITLE]} {self.measurement_unit}'


class AmountIngredient(models.Model):
    ingredients = models.ForeignKey('Ingredient', on_delete=models.CASCADE,
                                    related_name='recipe')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE,
                               related_name='ingredient')
    amount = models.PositiveIntegerField(default=1)

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
        default_related_name = 'favorites'


class Cart(FavoriteShoppingCart):
    class Meta:
        default_related_name = 'shopping_list'
