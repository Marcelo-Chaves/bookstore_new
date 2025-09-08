import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from product.models import Category


@pytest.mark.django_db
class TestProductCRUD:

    def setup_method(self):
        self.client = APIClient()
        self.url = "/api/product/categories/"
        self.user = User.objects.create_user(username="regular", password="1234")
        self.staff = User.objects.create_user(username="staff", password="1234", is_staff=True)

    def test_list_categories_public(self):
        Category.objects.create(name="Livros", description="Categoria de livros")
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.data["results"][0]["name"] == "Livros"

    def test_create_category_denied_for_regular_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {"name": "Eletrônicos", "description": "Categoria de eletrônicos"})
        assert response.status_code == 403

    def test_create_category_allowed_for_staff(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.post(self.url, {"name": "Games", "description": "Categoria de games"})
        assert response.status_code == 201
        assert Category.objects.filter(name="Games").exists()

    def test_update_category_allowed_for_staff(self):
        self.client.force_authenticate(user=self.staff)
        category = Category.objects.create(name="Velho", description="Categoria antiga")
        url_detail = f"{self.url}{category.id}/"
        response = self.client.put(url_detail, {"name": "Novo", "description": "Categoria atualizada"})
        assert response.status_code == 200
        category.refresh_from_db()
        assert category.name == "Novo"
        assert category.description == "Categoria atualizada"

    def test_delete_category_allowed_for_staff(self):
        self.client.force_authenticate(user=self.staff)
        category = Category.objects.create(name="Excluir", description="Categoria a excluir")
        url_detail = f"{self.url}{category.id}/"
        response = self.client.delete(url_detail)
        assert response.status_code == 204
        assert not Category.objects.filter(id=category.id).exists()
