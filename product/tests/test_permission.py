import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from product.models.category import Category
from product.permissions.custom import IsManagerOrReadOnly

# ------------------------
# Fixtures
# ------------------------
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
    def _auth_client(user):
        client = APIClient()
        token, _ = Token.objects.get_or_create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        return client
    return _auth_client

@pytest.fixture
def category(db, staff_user):
    return Category.objects.create(name="Categoria Teste", description="Descrição")

# ------------------------
# Permission tests
# ------------------------
@pytest.mark.django_db
def test_create_category_denied_for_regular_user(auth_client, regular_user):
    client = auth_client(regular_user)
    url = reverse("category-list")
    data = {"name": "Categoria Bloqueada", "description": "Não permitido"}
    response = client.post(url, data, format="json")
    assert response.status_code == 403

@pytest.mark.django_db
def test_create_category_allowed_for_staff(auth_client, staff_user):
    client = auth_client(staff_user)
    url = reverse("category-list")
    data = {"name": "Categoria Permitida", "description": "Permitido"}
    response = client.post(url, data, format="json")
    assert response.status_code == 201
    assert Category.objects.filter(name="Categoria Permitida").exists()
