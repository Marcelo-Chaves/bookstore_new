import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from product.models import Product, Category

@pytest.mark.django_db
class TestProductAndCategoryPermissions:

    def setup_method(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Categoria Pública")
        self.product = Product.objects.create(
            name="Produto Público",
            description="Produto visível sem login",
            price=10.0,
            category=self.category
        )

    def test_product_list_is_public(self):
        """Qualquer usuário (mesmo sem autenticação) pode listar produtos"""
        url = reverse("product-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) > 0

    def test_category_list_is_public(self):
        """Qualquer usuário (mesmo sem autenticação) pode listar categorias"""
        url = reverse("category-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) > 0

    def test_product_create_requires_staff(self, regular_user):
        """Usuário regular NÃO pode criar produto"""
        self.client.force_authenticate(user=regular_user)
        url = reverse("product-list")
        data = {
            "name": "Produto Teste",
            "description": "Teste",
            "price": 15.0,
            "category": self.category.id,
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == 403  # proibido

    def test_category_create_requires_staff(self, regular_user):
        """Usuário regular NÃO pode criar categoria"""
        self.client.force_authenticate(user=regular_user)
        url = reverse("category-list")
        data = {"name": "Categoria Teste"}
        response = self.client.post(url, data, format="json")
        assert response.status_code == 403  # proibido
