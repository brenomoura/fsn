from django.utils.translation import gettext as _
from rest_framework import serializers

from modules.api.models import Recipe, Step, Ingredient


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.ListSerializer(child=IngredientSerializer())
    steps = serializers.ListSerializer(child=StepSerializer())

    def create(self, validated_data):
        ingredients_data = validated_data.pop("ingredients")
        steps_data = validated_data.pop("steps")
        recipe = Recipe.objects.create(**validated_data)
        Ingredient.objects.bulk_create([
            Ingredient(recipe=recipe, **ingredient)
            for ingredient in ingredients_data
        ])
        Step.objects.bulk_create([
            Step(recipe=recipe, **step)
            for step in steps_data
        ])
        return recipe

    def update(self, instance, validated_data):
        if validated_data.get("ingredients") or validated_data.get("steps"):
            raise serializers.ValidationError(
                detail=_("For ingredients or steps update, please use their "
                         "specific endpoints (recipes/<recipe_id/ingredients/<ingredient_id>/ "
                         "or recipes/<recipe_id/steps/<step>/)")
            )
        return super(RecipeSerializer, self).update(instance, validated_data)

    class Meta:
        model = Recipe
        fields = "__all__"
