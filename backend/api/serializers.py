from django.db.models import F
from django.shortcuts import get_object_or_404
from djoser import serializers as djoser_serializers
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status

from foodgram.constants import AmountIngredientValidate, RecipeValidate
from recipe.models import (Favorite, Ingredient, Recipe,
                           Tag, Cart, AmountIngredient)
from users.serializers import UserSerializer
from users.models import CustomUser


class SubscribeListSerializer(djoser_serializers.UserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )
        read_only_fields = (
            'email', 'username',
            'first_name', 'last_name'
        )

    def validate(self, data):
        author_id = self.context.get(
            'request').parser_context.get('kwargs').get('id')
        author = get_object_or_404(CustomUser, id=author_id)
        user = self.context.get('request').user
        if user.follower.filter(author=author_id).exists():
            raise serializers.ValidationError(
                detail='Подписка уже существует',
                code=status.HTTP_400_BAD_REQUEST,
            )
        if user == author:
            raise serializers.ValidationError(
                detail='Нельзя подписаться на самого себя',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data

    def get_is_subscribed(self, data):
        request = self.context.get('request')
        return request.user.is_authenticated and data.following.filter(
            username=request.user
        ).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[: int(limit)]
        serializer = RecipeShortSerializer(
            recipes, many=True, read_only=True
        )
        return serializer.data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AmountIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)

    def validate_amount(self, amount):
        if amount < AmountIngredientValidate.MIN_AMOUNT_INGREDIENTS.value:
            raise serializers.ValidationError(
                f'Минимальное кол-во ингредиентов '
                f'{AmountIngredientValidate.MIN_AMOUNT_INGREDIENTS.value}')
        if amount > AmountIngredientValidate.MAX_AMOUNT_INGREDIENTS.value:
            raise serializers.ValidationError(
                'Слишком много ингредиентов!')
        return amount


class CreateAmountIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = AmountIngredient
        fields = ('id', 'amount',)


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=False, many=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_ingredients(self, data):
        ingredients = data.ingredients.values(
            "id", "name", "measurement_unit", amount=F("recipe__amount")
        )
        return ingredients

    def get_is_favorited(self, data):
        request = self.context.get('request')
        return (request.user.is_authenticated
                and data.favorites.filter(user=request.user).exists())

    def get_is_in_shopping_cart(self, data):
        request = self.context.get('request')
        return (request.user.is_authenticated
                and data.shopping_list.filter(user=request.user).exists())


class CreateRecipeSerializer(serializers.ModelSerializer):
    ingredients = CreateAmountIngredientSerializer(
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        error_messages={'does_not_exist': 'Указанного тега не существует'}
    )
    image = Base64ImageField()
    author = UserSerializer(read_only=True, required=False)
    cooking_time = serializers.IntegerField(
        min_value=RecipeValidate.MIN_COOKING_TIME.value,
        max_value=RecipeValidate.MAX_COOKING_TIME.value,
        error_messages={
            'min_value': f'Время готовки должно быть не меньше '
                         f'{RecipeValidate.MIN_COOKING_TIME.value} мин',
            'max_value': f'Время готовки должно быть не больше '
                         f'{RecipeValidate.MAX_COOKING_TIME.value} мин',
        }
    )

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time')

    def validate_tags(self, tags):
        tags_list = set()
        if not tags:
            raise serializers.ValidationError(
                'Отсутствует тег рецепта!'
            )
        for tag in tags:
            if not Tag.objects.filter(id=tag.id).exists():
                raise serializers.ValidationError(
                    'Указанного тега не существует')
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError(
                    'Теги должны быть уникальны')
            tags_list.add(tag)
            if len(tags_list) < 1:
                raise serializers.ValidationError(
                    'Отсуствуют теги')
        return tags

    def validate_image(self, image):
        if not image:
            raise serializers.ValidationError(
                'Отсутствует фото рецепта!'
            )
        return image

    def validate_ingredients(self, data):
        ingredients_list = set()
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                'Отсутствуют ингридиенты!'
            )
        for ingredient in ingredients:
            if ingredient['id'] in ingredients_list:
                raise serializers.ValidationError(
                    'Есть одинаковые ингредиенты!'
                )
            ingredients_list.add(ingredient['id'])
            if (int(ingredient.get('amount')) < AmountIngredientValidate.
                    MIN_AMOUNT_INGREDIENTS.value):
                raise serializers.ValidationError(
                    'Количество ингредиента должно быть больше 0')

        return data

    def validate(self, data):
        tags_ids = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')

        if not tags_ids:
            raise serializers.ValidationError('Укажите теги')
        if not ingredients:
            raise serializers.ValidationError('Укажите ингредиенты')
        return data

    @staticmethod
    def create_ingredients(recipe, ingredients):
        ingredient_list = []
        for ingredient_data in ingredients:
            ingredient_list.append(
                AmountIngredient(
                    ingredients=ingredient_data['id'],
                    amount=ingredient_data['amount'],
                    recipe=recipe,
                )
            )
        AmountIngredient.objects.bulk_create(ingredient_list)

    def create(self, validated_data):
        request = self.context.get('request', None)
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients)
        return recipe

    def update(self, recipe, validated_data):
        user = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        if recipe.author != user:
            raise serializers.ValidationError(
                'Вы не можете обновить этот рецепт,'
                ' вы не являетесь его автором.')
        AmountIngredient.objects.filter(recipe=recipe).delete()
        self.create_ingredients(recipe, ingredients)
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context={
            'request': self.context.get('request')
        }).data


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('recipe', 'user')

    def validate(self, data):
        if data['user'].favorites.filter(recipe=data['recipe']).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен в избранное.'
            )
        return data

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class ShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('recipe', 'user')

    def validate(self, data):
        if data['user'].shopping_list.filter(recipe=data['recipe']).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен в корзину'
            )
        return data

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data
