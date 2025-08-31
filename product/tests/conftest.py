import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from product.models import Category, Product

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def regular_user(db):
    user = User.objects.create_user(username="user", password="pass")
    Token.objects.create(user=user)
    return user

@pytest.fixture
def staff_user(db):
    user = User.objects.create_user(username="staff", password="pass", is_staff=True)
    Token.objects.create(user=user)
    return user

@pytest.fixture
def auth_client():
    """Retorna um client autenticado para o usuário fornecido"""
    def _auth_client(user):
        client = APIClient()
        token, _ = Token.objects.get_or_create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        return client
    return _auth_client

@pytest.fixture
def category(db):
    return Category.objects.create(name="Categoria Teste")

@pytest.fixture
def product(db, category):
    return Product.objects.create(
        name="Produto Teste",
        description="Descrição teste",
        price=100.0,
        stock=20,
        is_active=True,
        category=category
    )
