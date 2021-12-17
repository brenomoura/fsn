from django.contrib.auth.models import User
from django.forms import model_to_dict
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from modules.api.models import Recipe, Ingredient, Step


def serialize_dt(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class TestRecipeAPI(APITestCase):

    def setUp(self) -> None:
        super(TestRecipeAPI, self).setUp()
        self.user = User.objects.create_user(
            username="test_user", email="test_user@test.com", password="test_password"
        )
        # Usar OAuth?
        token, created = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        self.recipe1 = Recipe.objects.create(
            name="recipe 1",
            difficulty_level="beginner"
        )
        self.ingredient1 = Ingredient.objects.create(
            recipe=self.recipe1,
            quantity=1,
            unit_type="meter",
            name="gold",
        )

        self.step1 = Step.objects.create(
            recipe=self.recipe1,
            description="Step 1",
            step=1
        )
        self.recipe1_data = {
            "id": str(self.recipe1.id),
            "name": self.recipe1.name,
            "description": self.recipe1.description,
            "image": self.recipe1.image_url,
            "video": self.recipe1.video_url,
            "difficulty_level": self.recipe1.difficulty_level,
            "created_at": serialize_dt(self.recipe1.created_at),
            "updated_at": serialize_dt(self.recipe1.updated_at),
            "ingredients": [
                model_to_dict(self.ingredient1)
            ],
            "steps": [
                model_to_dict(self.step1)
            ]
        }

        self.recipe2 = Recipe.objects.create(
            name="recipe 2",
            difficulty_level="beginner"
        )
        self.ingredient2 = Ingredient.objects.create(
            recipe=self.recipe2,
            quantity=1,
            unit_type="meter",
            name="gold",
        )

        self.step2 = Step.objects.create(
            recipe=self.recipe2,
            description="Step 2",
            step=1
        )

        self.recipe2_data = {
            "id": str(self.recipe2.id),
            "name": self.recipe2.name,
            "description": self.recipe2.description,
            "image": self.recipe2.image_url,
            "video": self.recipe2.video_url,
            "difficulty_level": self.recipe2.difficulty_level,
            "created_at": serialize_dt(self.recipe2.created_at),
            "updated_at": serialize_dt(self.recipe2.updated_at),
            "ingredients": [
                model_to_dict(self.ingredient2)
            ],
            "steps": [
                model_to_dict(self.step2)
            ]
        }

    def test_create_recipe_authenticated(self):
        data = {
            "name": "Something 111",
            "description": "Super Description",
            "image": "image_url.com/1231231",
            "video": "video_url.com/1231231",
            "difficulty_level": "beginner",
            "ingredients": [
                {
                    "quantity": 200,
                    "unit_type": "ml",
                    "ingredient": "some cool ingredient",
                    "category": "Fruits"  # TODO - Lista de Categorias (Recheio, Massa, Etc)
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

    def test_create_recipe_unauthenticated(self):
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
        self.client.credentials()
        res = self.client.post("/api/v1/recipes/", data=data, format="json")
        self.assertEqual(res.status_code, 401)

    def test_list_recipes_authenticated(self):
        res = self.client.get("/api/v1/recipes/")
        self.assertEqual(res.status_code, 200)
        self.assertListEqual(res.json()["results"], [self.recipe1_data, self.recipe2_data])

    def test_list_recipes_unauthenticated(self):
        self.client.credentials()
        res = self.client.get("/api/v1/recipes/")
        self.assertEqual(res.status_code, 401)

    def test_detail_recipes_authenticated(self):
        res = self.client.get(f"/api/v1/recipes/{str(self.recipe1.id)}/")
        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.json(), self.recipe1_data)

    def test_detail_recipes_unauthenticated(self):
        self.client.credentials()
        res = self.client.get(f"/api/v1/recipes/{str(self.recipe1.id)}/")
        self.assertEqual(res.status_code, 401)

    def test_update_recipes_authenticated(self):
        data = {
            "name": "New Name"
        }
        res = self.client.patch(f"/api/v1/recipes/{str(self.recipe1.id)}/", data=data, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.json(), self.recipe1_data)

    def test_update_recipes_unauthenticated(self):
        data = {
            "name": "New Name"
        }
        self.client.credentials()
        res = self.client.patch(f"/api/v1/recipes/{str(self.recipe1.id)}/", data=data, format="json")
        self.assertEqual(res.status_code, 401)

    def test_delete_recipes_authenticated(self):
        res = self.client.delete(f"/api/v1/recipes/{str(self.recipe1.id)}/")
        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.json(), self.recipe1_data)

    def test_delete_recipes_unauthenticated(self):
        self.client.credentials()
        res = self.client.delete(f"/api/v1/recipes/{str(self.recipe1.id)}/")
        self.assertEqual(res.status_code, 401)

