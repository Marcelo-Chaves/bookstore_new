import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from order.models import Order
from product.models import Category, Product
from rest_framework.authtoken.models import Token


# ------------------------
# Fixtures
# ------------------------
@pytest.fixture
def auth_client():
    def _auth_client(user):
        client = APIClient()
        token, _ = Token.objects.get_or_create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        return client
    return _auth_client


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


@pytest.fixture
def category(db):
    return Category.objects.create(name="Categoria Teste")


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        name="Produto Teste",
        description="Descrição",
        price=10.0,
        stock=5,
        category=category
    )


@pytest.fixture
def order(db, staff_user, product):
    return Order.objects.create(
        user=staff_user,
        product=product,
        quantity=1
    )


# --------------------------
# Testes de permissão ORDER
# --------------------------

@pytest.mark.django_db
def test_order_create_denied_for_anonymous(product):
    client = APIClient()
    url = reverse("order-list")
    data = {"product": product.id, "quantity": 1}
    response = client.post(url, data, format="json")
    assert response.status_code == 401  # Deve exigir autenticação


@pytest.mark.django_db
def test_order_list_denied_for_anonymous(order):
    client = APIClient()
    url = reverse("order-list")
    response = client.get(url)
    assert response.status_code == 401  # Deve exigir autenticação


@pytest.mark.django_db
def test_order_create_allowed_for_regular_user(auth_client, regular_user, product):
    client = auth_client(regular_user)
    url = reverse("order-list")
    data = {
        "name": "Pedido Teste",
        "product": product.id,
        "quantity": 1
    }
    response = client.post(url, data, format="json")
    assert response.status_code == 201
    assert Order.objects.filter(user=regular_user, product=product).exists()


@pytest.mark.django_db
def test_order_list_allowed_for_regular_user(auth_client, regular_user, order):
    client = auth_client(regular_user)
    url = reverse("order-list")
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    results = data.get("results", data)
    assert any(o["quantity"] == order.quantity for o in results)


@pytest.mark.django_db
def test_order_create_allowed_for_staff(auth_client, staff_user, product):
    client = auth_client(staff_user)
    url = reverse("order-list")
    data = {
        "name": "Pedido Staff",
        "product": product.id,
        "quantity": 1
    }
    response = client.post(url, data, format="json")
    assert response.status_code == 201
    assert Order.objects.filter(user=staff_user, product=product).exists()


@pytest.mark.django_db
def test_order_list_allowed_for_staff(auth_client, staff_user, order):
    client = auth_client(staff_user)
    url = reverse("order-list")
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    results = data.get("results", data)
    assert any(o["quantity"] == order.quantity for o in results)


# --------------------------
# Testes de acesso público (Product e Category)
# --------------------------

@pytest.mark.django_db
def test_category_list_allowed_for_anonymous(category):
    client = APIClient()
    url = reverse("category-list")
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    results = data.get("results", data)
    assert any(c["name"] == category.name for c in results)


@pytest.mark.django_db
def test_product_list_allowed_for_anonymous(product):
    client = APIClient()
    url = reverse("product-list")
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    results = data.get("results", data)
    assert any(p["name"] == product.name for p in results)
