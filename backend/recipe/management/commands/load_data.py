import json

from django.core.management.base import BaseCommand
from recipe.models import Ingredient


class Command(BaseCommand):
    help = 'Load ingredients data from json to DB.'

    def handle(self, *args, **kwargs):
        with open(
                'data/ingredients.json', 'r',
                encoding='UTF-8'
        ) as ingredients:
            ingredient_data = json.loads(ingredients.read())
            for ingredient in ingredient_data:
                Ingredient.objects.get_or_create(**ingredient)
        self.stdout.write(self.style.SUCCESS('Data uploaded'))
