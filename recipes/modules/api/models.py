import uuid

from django.db import models
from django.utils.translation import gettext as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Recipe(BaseModel):
    difficulty_levels = [
        ("beginner", _("Iniciante")),
        ("intermediate", _("Intermediário")),
        ("advanced", _("Avançado"))
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, max_length=1024)
    image_url = models.URLField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    difficulty_level = models.CharField(choices=difficulty_levels, max_length=255)


class Ingredient(models.Model):
    UNIT_TYPES = [
        ("teaspoon", _("Colher de Chá")),
        ("tablespoon", _("Colher de Sopa")),
        ("cup", _("Xícara")),
        ("milliliter", _("ml")),
        ("liter", _("l")),
        ("milligram", _("mg")),
        ("gram", _("g")),
        ("kilogram", _("kg")),
        ("millimeter", _("mm")),
        ("centimeter", _("cm")),
        ("meter", _("m")),
        ("to_taste", _("A gosto")),
    ]
    CATEGORIES = [
        ("Eggs, milk and milk products", _("Ovos, leites e derivados de leite")),
        ("Fats and oils", _("Gorduras e óleos")),
        ("Fruits", _("Frutas")),
        ("Grain, nuts and baking products", _("Cereais, nozes e produtos de panificação")),
        ("Herbs and spices", _("Ervas e especiarias")),
        ("Meat, sausages and fish", _("Carnes, linguiças e peixes")),
        ("Pasta, rice and pulses", _("Macarrão, arroz e leguminosas")),
        ("Vegetables", _("Legumes")),
        ("Others", _("Outros")),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, related_name="ingredients", null=True)
    quantity = models.FloatField(null=True)
    unit_type = models.CharField(choices=UNIT_TYPES, max_length=255)
    name = models.CharField(max_length=255)
    category = models.CharField(choices=CATEGORIES, null=True, max_length=255)


class Step(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, related_name="steps", null=True)
    step = models.IntegerField()
    description = models.TextField(blank=True, max_length=1024)
