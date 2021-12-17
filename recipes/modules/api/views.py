from rest_framework import generics


class RecipeListCreateView(generics.ListCreateAPIView):
    ...


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    ...


class RecipeStepsView(generics.ListCreateAPIView):
    ...


class RecipeStepDetailView(generics.RetrieveUpdateDestroyAPIView):
    ...
