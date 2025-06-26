#agora vamos rodar os testes
import pytest
from rest_framework.test import APIClient
from product.models import Category, Product


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_create_category(client):
    response = client.post("/api/product/categories/", {"name": "Eletrônicos"}, format="json")
    assert response.status_code == 201
    assert Category.objects.count() == 1


@pytest.mark.django_db
def test_create_product_with_category(client):
    category = Category.objects.create(name="Informática")
    data = {
        "name": "Mouse Gamer",
        "description": "Mouse com RGB",
        "category_id": category.id,
        "price": 150.00,
        "stock": 50,
        "is_active": True
    }
    response = client.post("/api/product/products/", data, format="json")
    assert response.status_code == 201
    assert Product.objects.count() == 1


@pytest.mark.django_db
def test_list_products(client):
    response = client.get("/api/product/products/")
    assert response.status_code == 200
