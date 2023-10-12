from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipe.models import (Favorite, Ingredient, AmountIngredient, Recipe,
                           Cart, Tag)
from rest_framework import status, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPagination
from api.permissions import AuthorStaffOrReadOnly
from api.serializers import (CreateRecipeSerializer, FavoriteSerializer,
                             IngredientSerializer, RecipeReadSerializer,
                             ShopListSerializer, SubscribeListSerializer,
                             TagSerializer, UserSerializer)
from users.models import Follow

CustomUser = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    @action(methods=('GET',), detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=('POST',),
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(CustomUser, id=kwargs.get('id'))
        serializer = SubscribeListSerializer(
            author, data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        Follow.objects.create(username=request.user, author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def destroy_shopping_cart(self, request, **kwargs):
        try:
            author = get_object_or_404(CustomUser, id=kwargs.get('id'))
            Follow.objects.get(username=request.user,
                               author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Follow.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=('GET',), detail=False,
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        queryset = CustomUser.objects.filter(following__username=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeListSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorStaffOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return CreateRecipeSerializer

    # @staticmethod
    # def send_message(ingredients):
    #     shopping_list = 'Купить в магазине:'
    #     for ingredient in ingredients:
    #         shopping_list += (
    #             f"\n{ingredient['ingredient__name']} "
    #             f"({ingredient['ingredient__measurement_unit']}) - "
    #             f"{ingredient['amount']}")
    #     file = 'shopping_list.txt'
    #     response = HttpResponse(shopping_list, content_type='text/plain')
    #     response['Content-Disposition'] = f'attachment; filename="{file}.txt"'
    #     return response
    #
    # @action(detail=False, methods=['GET'])
    # def download_shopping_cart(self, request):
    #     ingredients = AmountIngredient.objects.filter(
    #         recipe__shopping_list__user=request.user
    #     ).order_by('ingredients__name').values(
    #         'ingredients__name', 'ingredients__measurement_unit'
    #     ).annotate(amount=Sum('amount'))
    #     return self.send_message(ingredients)
    @action(detail=False, methods=('get',),
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request, **kwargs):
        ingredients = (
            AmountIngredient.objects
            .filter(recipe__shopping_list__user=request.user)
            .values('ingredients')
            .annotate(total_amount=Sum('amount'))
            .values_list('ingredients__name', 'total_amount',
                         'ingredients__measurement_unit')
        )
        file_list = []
        [file_list.append(
            '{} - {} {}.'.format(*ingredient)) for ingredient in ingredients]
        file = HttpResponse('Cписок покупок:\n' + '\n'.join(file_list),
                            content_type='text/plain')
        file['Content-Disposition'] = (
            f'attachment; filename=shopping_cart.txt')
        return file

    @action(detail=True, methods=('POST',),
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        context = {'request': request}
        try:
            recipe = Recipe.objects.get(id=pk)
        except Recipe.DoesNotExist:
            raise serializers.ValidationError('Рецепта не существует')
        data = {
            'user': request.user.id,
            'recipe': recipe.id
        }
        serializer = ShopListSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def destroy_shopping_cart(self, request, pk):
        try:
            recipe = get_object_or_404(Recipe, id=pk)
            Cart.objects.get(user=request.user,
                             recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=('POST',),
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        context = {"request": request}
        try:
            recipe = Recipe.objects.get(id=pk)
        except Recipe.DoesNotExist:
            raise serializers.ValidationError('Рецепта не существует')
        data = {
            'user': request.user.id,
            'recipe': recipe.id
        }
        serializer = FavoriteSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def destroy_favorite(self, request, pk):
        try:
            recipe = get_object_or_404(Recipe, id=pk)
            Favorite.objects.get(user=request.user,
                                 recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
