import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from order.models import Order
from product.models import Product, Category

# -------------------
# Usuários
# -------------------
@pytest.fixture
def regular_user(db):
    user = User.objects.create_user(username="regular", password="pass")
    Token.objects.create(user=user)
    return user

@pytest.fixture
def staff_user(db):
    user = User.objects.create_user(username="staff", password="pass", is_staff=True)
    Token.objects.create(user=user)
    return user

# -------------------
# Categoria e Produto
# -------------------
@pytest.fixture
def category(db):
    return Category.objects.create(name="Categoria Teste", description="Teste")

@pytest.fixture
def product(db, category):
    return Product.objects.create(
        name="Produto Teste",
        description="Produto de teste",
        price=10.0,
        stock=5,
        category=category
    )

# -------------------
# Order
# -------------------
@pytest.fixture
def order(db, product, staff_user):
    return Order.objects.create(
        name="Pedido Teste",
        description="Descrição do pedido",
        quantity=1,
        product=product,
        created_by=staff_user
    )

# -------------------
# Client autenticado
# -------------------
@pytest.fixture
def auth_client():
    def _auth_client(user):
        from rest_framework.test import APIClient
        client = APIClient()
        token, _ = Token.objects.get_or_create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        return client
    return _auth_client
