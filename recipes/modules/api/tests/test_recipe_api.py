from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient

from modules.api.models import Recipe


class TestRecipeAPI(APITestCase):

    def setUp(self) -> None:
        super(TestRecipeAPI, self).setUp()
        self.user = User.objects.create_user(
            username="test_user", email="test_user@test.com", password="test_password"
        )
        # Usar OAuth?
        # token, created = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()

    def test_create_recipe_authenticated(self):
        data = {
            "name": "Something 111",
            "description": "Super Description",
            "image": "image_url.com/1231231",
            "video": "video_url.com/1231231",
            "difficulty_level": "beginner",  # TODO - Lista de dificuldades (beginner, intermediate, advanced)
            "ingredients": [
                {
                    "quantity": 200,
                    "unit_type": "ml",
                    "ingredient": "some cool ingredient",
                    "category": "fillings"  # TODO - Lista de Categorias (Recheio, Massa, Etc)
                }
            ],
            "steps": [
                {
                    "step": 1,
                    "description": "throw away everything and buy a delivery"
                },
                {
                    "step": 2,
                    "description": "just kidding, don't do the step above"
                },
            ]

        }
        res = self.client.post("/api/v1/recipes/", data=data, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertTrue(Recipe.objects.get(name=data["name"]))
