from django.core.management.base import BaseCommand
import json

from recipe.models import Ingredient


class Command(BaseCommand):
    help = 'Load ingredients data from json to DB.'

    def handle(self, *args, **kwargs):
        with open(
                'data/ingredients.json', 'r',
                encoding='UTF-8'
        ) as ingredients:
            ingredient_data = json.loads(ingredients.read())
            ingredients_to_create = [Ingredient(**ingredient) for ingredient in
                                     ingredient_data]
            Ingredient.objects.bulk_create(ingredients_to_create)
        self.stdout.write(self.style.SUCCESS('Data uploaded'))
