import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from order.models.order import Order
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
    user = User.objects.create_user(username="user", password="pass")
    Token.objects.create(user=user)
    return user

@pytest.fixture
def staff_user(db):
    user = User.objects.create_user(username="staff", password="pass", is_staff=True)
    Token.objects.create(user=user)
    return user

@pytest.fixture
def order(db, staff_user):
    return Order.objects.create(
        name="Pedido Teste",
        description="Descrição do pedido",
        created_by=staff_user
    )

# ------------------------
# Permission tests
# ------------------------
@pytest.mark.django_db
def test_list_orders_allowed_to_all(auth_client, staff_user, order):
    client = auth_client(staff_user)
    url = reverse("order-list")
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    results = data.get("results", data)
    assert any(o["name"] == order.name for o in results)


@pytest.mark.django_db
def test_create_order_denied_for_regular_user(auth_client, regular_user):
    client = auth_client(regular_user)
    url = reverse("order-list")
    data = {"name": "Pedido Bloqueado", "description": "Não permitido"}
    response = client.post(url, data, format="json")
    assert response.status_code == 403

@pytest.mark.django_db
def test_create_order_allowed_for_staff(auth_client, staff_user):
    client = auth_client(staff_user)
    url = reverse("order-list")
    data = {"name": "Pedido Staff", "description": "Permitido"}
    response = client.post(url, data, format="json")
    assert response.status_code == 201
    assert Order.objects.filter(name="Pedido Staff").exists()
