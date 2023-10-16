from django.contrib import admin

from .models import (Favorite, Ingredient, AmountIngredient, Recipe,
                     Cart, Tag)


class IngredientInline(admin.TabularInline):
    model = AmountIngredient
    extra = 3
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'cooking_time',
                    'favorites',)
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author', 'tags')
    inlines = (IngredientInline,)

    def favorites(self, obj):
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    prepopulated_fields = {'slug': ['name']}
    search_fields = ('name',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    search_fields = ('user',)
