import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from order.models import Order
from product.models import Product, Category
from rest_framework.authtoken.models import Token

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
    return Product.objects.create(name="Produto Teste", price=10.0, category=category)

@pytest.fixture
def order(db, staff_user, product):
    return Order.objects.create(
        name="Pedido Teste",
        description="Descrição do pedido",
        quantity=1,
        product=product,
        user=staff_user,
        created_by=staff_user
    )

# ------------------------
# CRUD tests
# ------------------------
@pytest.mark.django_db
class TestOrderAPI:

    def test_create_order_regular_user(self, auth_client, regular_user, product):
        client = auth_client(regular_user)
        url = reverse("order-list")
        data = {
            "name": "Pedido User",
            "description": "Teste",
            "quantity": 2,
            "product": product.id
        }
        response = client.post(url, data, format="json")
        assert response.status_code == 201  # mudou de 403 para 201
        assert Order.objects.filter(user=regular_user, product=product).exists()

    def test_create_order_staff_user(self, auth_client, staff_user, product):
        client = auth_client(staff_user)
        url = reverse("order-list")
        data = {
            "name": "Pedido Staff",
            "description": "Teste",
            "quantity": 5,
            "product": product.id
        }
        response = client.post(url, data, format="json")
        assert response.status_code == 201
        assert Order.objects.filter(name="Pedido Staff").exists()

    def test_list_orders(self, auth_client, staff_user, order):
        client = auth_client(staff_user)
        url = reverse("order-list")
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        results = data.get("results", data)
        assert any(o["id"] == order.id for o in results)

    def test_update_order(self, auth_client, staff_user, order):
        client = auth_client(staff_user)
        url = reverse("order-detail", args=[order.id])
        data = {
            "name": "Pedido Atualizado",
            "description": order.description,
            "quantity": 10,
            "product": order.product.id
        }
        response = client.put(url, data, format="json")
        assert response.status_code == 200
        order.refresh_from_db()
        assert order.name == "Pedido Atualizado"
        assert order.quantity == 10

    def test_delete_order(self, auth_client, staff_user, order):
        client = auth_client(staff_user)
        url = reverse("order-detail", args=[order.id])
        response = client.delete(url)
        assert response.status_code == 204
        assert not Order.objects.filter(id=order.id).exists()
