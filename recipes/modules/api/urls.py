from django.urls import path

from modules.api import views

urlpatterns = [
    path(
        f"recipes/",
        views.RecipeListCreateView.as_view(), name="recipes_v1"
    ),
    path(
        f"recipes/<uuid:pk>/",
        views.RecipeDetailView.as_view(), name="recipe_detail_v1"
    ),
    path(
        f"recipes/<uuid:pk>/steps/",
        views.RecipeStepListView.as_view(), name="recipe_steps_v1"
    ),
    path(
        f"recipes/<uuid:pk>/steps/<int:step>/",
        views.RecipeStepDetailView.as_view(), name="recipe_steps_v1"
    ),
    path(
        f"recipes/<uuid:pk>/ingredients/",
        views.RecipeIngredientsListView.as_view(), name="recipe_ingredient_v1"
    ),
    path(
        f"recipes/<uuid:pk>/ingredients/<uuid:ingredient>/",
        views.RecipeIngredientDetailView.as_view(), name="recipe_ingredient_v1"
    ),
]
