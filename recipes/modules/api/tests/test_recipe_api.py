from django.contrib.auth.models import User
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
        self.token, created = Token.objects.get_or_create(user=self.user)

        self.client = APIClient()
        # self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

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
            "image_url": self.recipe1.image_url,
            "video_url": self.recipe1.video_url,
            "difficulty_level": self.recipe1.difficulty_level,
            "created_at": serialize_dt(self.recipe1.created_at),
            "updated_at": serialize_dt(self.recipe1.updated_at),
            "ingredients": [
                {
                    'category': self.ingredient1.category,
                    'id': str(self.ingredient1.id),
                    'name': self.ingredient1.name,
                    'quantity': self.ingredient1.quantity,
                    'recipe': str(self.ingredient1.recipe.id),
                    'unit_type': str(self.ingredient1.unit_type),
                }
            ],
            "steps": [
                {
                    'description': self.step1.description,
                    'id': str(self.step1.id),
                    'recipe': str(self.step1.recipe.id),
                    'step': self.step1.step
                }
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
            "image_url": self.recipe2.image_url,
            "video_url": self.recipe2.video_url,
            "difficulty_level": self.recipe2.difficulty_level,
            "created_at": serialize_dt(self.recipe2.created_at),
            "updated_at": serialize_dt(self.recipe2.updated_at),
            "ingredients": [
                {
                    'category': self.ingredient2.category,
                    'id': str(self.ingredient2.id),
                    'name': self.ingredient2.name,
                    'quantity': self.ingredient2.quantity,
                    'recipe': str(self.ingredient2.recipe.id),
                    'unit_type': str(self.ingredient2.unit_type),
                }
            ],
            "steps": [
                {
                    'description': self.step2.description,
                    'id': str(self.step2.id),
                    'recipe': str(self.step2.recipe.id),
                    'step': self.step2.step
                }
            ]
        }

    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def unauthenticated(self):
        self.client.force_authenticate(user=None)

    def test_create_recipe_authenticated(self):
        data = {
            "name": "Something 111",
            "description": "Super Description",
            "image_url": "http://www.google.com/",
            "video_url": "http://www.google.com/",
            "difficulty_level": "beginner",
            "ingredients": [
                {
                    "quantity": 200,
                    "unit_type": "milligram",
                    "name": "some cool ingredient",
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
        self.authenticate()
        res = self.client.post("/api/v1/recipes/", data=data, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertTrue(Recipe.objects.get(name=data["name"]))

    def test_create_recipe_unauthenticated(self):
        data = {
            "name": "Something 111",
            "description": "Super Description",
            "image": "image_url.com/1231231",
            "video": "video_url.com/1231231",
            "difficulty_level": "beginner",
            "ingredients": [
                {
                    "quantity": 200,
                    "unit_type": "milligram",
                    "ingredient": "some cool ingredient",
                    "category": "fillings"
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
        self.unauthenticated()
        res = self.client.post("/api/v1/recipes/", data=data, format="json")
        self.assertEqual(res.status_code, 403)

    def test_list_recipes_authenticated(self):
        self.authenticate()
        res = self.client.get("/api/v1/recipes/")
        self.assertEqual(res.status_code, 200)
        self.assertListEqual(res.json()["results"], [self.recipe1_data, self.recipe2_data])

    def test_list_recipes_unauthenticated(self):
        self.unauthenticated()
        res = self.client.get("/api/v1/recipes/")
        self.assertEqual(res.status_code, 403)

    def test_detail_recipes_authenticated(self):
        self.authenticate()
        res = self.client.get(f"/api/v1/recipes/{str(self.recipe1.id)}/")
        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.json(), self.recipe1_data)

    def test_detail_recipes_unauthenticated(self):
        self.unauthenticated()
        res = self.client.get(f"/api/v1/recipes/{str(self.recipe1.id)}/")
        self.assertEqual(res.status_code, 403)

    def test_update_recipes_authenticated(self):
        data = {
            "name": "New Name",
        }
        self.authenticate()
        res = self.client.patch(f"/api/v1/recipes/{str(self.recipe1.id)}/", data=data, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["name"], data["name"])

    def test_update_recipes_authenticated_not_allowed(self):
        data = {
            "ingredients": [
                {"unit_type": "milligram"}
            ]
        }
        self.authenticate()
        res = self.client.patch(f"/api/v1/recipes/{str(self.recipe1.id)}/", data=data, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertListEqual(res.json(), [
            'For ingredients or steps update, please use their specific endpoints '
            '(recipes/<recipe_id/ingredients/<ingredient_id>/ or recipes/<recipe_id/steps/<step>/)'
        ])

    def test_update_recipes_unauthenticated(self):
        data = {
            "name": "New Name"
        }
        self.unauthenticated()
        res = self.client.patch(f"/api/v1/recipes/{str(self.recipe1.id)}/", data=data, format="json")
        self.assertEqual(res.status_code, 403)

    def test_delete_recipes_authenticated(self):
        self.authenticate()
        res = self.client.delete(f"/api/v1/recipes/{str(self.recipe1.id)}/")
        self.assertEqual(res.status_code, 204)

    def test_delete_recipes_unauthenticated(self):
        self.unauthenticated()
        res = self.client.delete(f"/api/v1/recipes/{str(self.recipe1.id)}/")
        self.assertEqual(res.status_code, 403)

    def test_list_recipe_ingredients_authenticated(self):
        self.authenticate()
        res = self.client.get(f"/api/v1/recipes/{str(self.recipe1.id)}/ingredients/")
        self.assertEqual(res.status_code, 200)
        self.assertListEqual(res.json()["results"], self.recipe1_data["ingredients"])

    def test_list_recipe_ingredients_unauthenticated(self):
        self.unauthenticated()
        res = self.client.get(f"/api/v1/recipes/{str(self.recipe1.id)}/ingredients/")
        self.assertEqual(res.status_code, 403)

    def test_detail_recipe_ingredient_authenticated(self):
        self.authenticate()
        res = self.client.get(f"/api/v1/recipes/{str(self.recipe1.id)}/ingredients/{str(self.ingredient1.id)}/")
        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.json(), self.recipe1_data["ingredients"][0])

    def test_detail_recipe_different_ingredient(self):
        self.authenticate()
        res = self.client.get(f"/api/v1/recipes/{str(self.recipe1.id)}/ingredients/{str(self.ingredient2.id)}/")
        self.assertEqual(res.status_code, 404)

    def test_detail_recipe_ingredient_unauthenticated(self):
        self.unauthenticated()
        res = self.client.get(f"/api/v1/recipes/{str(self.recipe1.id)}/ingredients/{str(self.ingredient1.id)}/")
        self.assertEqual(res.status_code, 403)

    def test_update_recipe_ingredient_authenticated(self):
        data = {
            "unit_type": "millimeter",
        }
        self.authenticate()
        res = self.client.patch(
            f"/api/v1/recipes/{str(self.recipe1.id)}/ingredients/{str(self.ingredient1.id)}/",
            data=data, format="json"
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["unit_type"], data["unit_type"])

    def test_update_recipe_ingredient_unauthenticated(self):
        data = {
            "unit_type": "millimeter",
        }
        self.unauthenticated()
        res = self.client.patch(
            f"/api/v1/recipes/{str(self.recipe1.id)}/ingredients/{str(self.ingredient1.id)}/",
            data=data, format="json"
        )

        self.assertEqual(res.status_code, 403)

    def test_delete_recipe_ingredient_authenticated(self):
        self.authenticate()
        res = self.client.delete(
            f"/api/v1/recipes/{str(self.recipe1.id)}/ingredients/{str(self.ingredient1.id)}/",
        )
        self.assertEqual(res.status_code, 204)

    def test_delete_recipe_ingredient_unauthenticated(self):
        self.unauthenticated()
        res = self.client.delete(
            f"/api/v1/recipes/{str(self.recipe1.id)}/ingredients/{str(self.ingredient1.id)}/",
        )
        self.assertEqual(res.status_code, 403)

    def test_list_recipe_steps_authenticated(self):
        self.authenticate()
        res = self.client.get(f"/api/v1/recipes/{str(self.recipe1.id)}/steps/")
        self.assertEqual(res.status_code, 200)
        self.assertListEqual(res.json()["results"], self.recipe1_data["steps"])

    def test_list_recipe_steps_unauthenticated(self):
        self.unauthenticated()
        res = self.client.get(f"/api/v1/recipes/{str(self.recipe1.id)}/steps/")
        self.assertEqual(res.status_code, 403)

    def test_detail_recipe_step_authenticated(self):
        self.authenticate()
        res = self.client.get(f"/api/v1/recipes/{str(self.recipe1.id)}/steps/{str(self.step1.step)}/")
        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.json(), self.recipe1_data["steps"][0])

    def test_detail_recipe_different_step(self):
        self.authenticate()
        res = self.client.get(f"/api/v1/recipes/{str(self.recipe1.id)}/steps/999999/")
        self.assertEqual(res.status_code, 404)

    def test_detail_recipe_step_unauthenticated(self):
        self.unauthenticated()
        res = self.client.get(f"/api/v1/recipes/{str(self.recipe1.id)}/steps/{str(self.step1.step)}/")
        self.assertEqual(res.status_code, 403)

    def test_update_recipe_step_authenticated(self):
        data = {
            "description": "something different",
        }
        self.authenticate()
        res = self.client.patch(
            f"/api/v1/recipes/{str(self.recipe1.id)}/steps/{str(self.step1.step)}/",
            data=data, format="json"
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["description"], data["description"])

    def test_update_recipe_step_unauthenticated(self):
        data = {
            "description": "something different",
        }
        self.unauthenticated()
        res = self.client.patch(
            f"/api/v1/recipes/{str(self.recipe1.id)}/steps/{str(self.step1.step)}/",
            data=data, format="json"
        )

        self.assertEqual(res.status_code, 403)

    def test_delete_recipe_step_authenticated(self):
        self.authenticate()
        res = self.client.delete(
            f"/api/v1/recipes/{str(self.recipe1.id)}/steps/{str(self.step1.step)}/",
        )
        self.assertEqual(res.status_code, 204)

    def test_delete_recipe_step_unauthenticated(self):
        self.unauthenticated()
        res = self.client.delete(
            f"/api/v1/recipes/{str(self.recipe1.id)}/steps/{str(self.step1.step)}/",
        )
        self.assertEqual(res.status_code, 403)
