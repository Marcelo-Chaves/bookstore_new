import pytest
from django.contrib.auth.models import User
from product.models import Category, Product

@pytest.mark.django_db
class TestProductPermissions:

    def setup_method(self):
        from rest_framework.test import APIClient
        self.client = APIClient()
        self.regular_user = User.objects.create_user(username="regular", password="1234")
        self.staff_user = User.objects.create_user(username="staff", password="1234", is_staff=True)
        self.category = Category.objects.create(name="Cat Teste", description="Descrição")
        self.product = Product.objects.create(
            name="Prod Teste",
            description="Desc",
            price=10.0,
            stock=5,
            category=self.category
        )
        self.url_categories = "/api/product/categories/"
        self.url_products = "/api/product/products/"

    # Category
    def test_category_create_denied_for_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(self.url_categories, {"name": "Nova", "description": "Desc"})
        assert response.status_code == 403

    def test_category_create_allowed_for_staff(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(self.url_categories, {"name": "Nova", "description": "Desc"})
        assert response.status_code == 201

    def test_category_list_is_public(self):
        response = self.client.get(self.url_categories)
        assert response.status_code == 200

    # Product
    def test_product_create_denied_for_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(
            self.url_products,
            {"name": "Produto Novo", "description": "Desc", "price": 5.0, "category": self.category.id}
        )
        assert response.status_code == 403

    def test_product_create_allowed_for_staff(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(
            self.url_products,
            {"name": "Produto Novo", "description": "Desc", "price": 5.0, "category": self.category.id}
        )
        assert response.status_code == 201

    def test_product_list_is_public(self):
        response = self.client.get(self.url_products)
        assert response.status_code == 200
