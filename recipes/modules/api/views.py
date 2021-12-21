from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from modules.api.models import Recipe, Ingredient, Step
from modules.api.serializers import RecipeSerializer, StepSerializer, IngredientSerializer


class RecipeListCreateView(generics.ListCreateAPIView):
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Recipe.objects.all()


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Recipe.objects.all()


class RecipeIngredientsListView(generics.ListCreateAPIView):
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        qs = super(RecipeIngredientsListView, self).get_queryset()
        return qs.filter(recipe=self.kwargs["pk"])


class RecipeIngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), recipe=self.kwargs.get("pk"), id=self.kwargs.get("ingredient")
        )


class RecipeStepListView(generics.ListCreateAPIView):
    serializer_class = StepSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Step.objects.all()

    def get_queryset(self):
        qs = super(RecipeStepListView, self).get_queryset()
        return qs.filter(recipe=self.kwargs["pk"])


class RecipeStepDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StepSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Step.objects.all()

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), recipe=self.kwargs.get("pk"), step=self.kwargs.get("step")
        )

