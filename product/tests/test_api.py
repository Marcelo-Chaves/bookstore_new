import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from product.models import Category, Product
from order.models import Order
from django.urls import reverse


@pytest.mark.django_db
class TestProductAPI:

    def setup_method(self):
        self.client = APIClient()
        # 🔹 Usuários
        self.user = User.objects.create_user(username="regular", password="1234")
        self.staff = User.objects.create_user(username="staff", password="1234", is_staff=True)

        # 🔹 Categoria para vincular os produtos
        self.category = Category.objects.create(name="Categoria Teste")

        # 🔹 Produto padrão
        self.product = Product.objects.create(
            name="Produto Teste",
            description="Descrição",
            price=20.0,
            stock=10,
            category=self.category,
        )

        # 🔹 URLs corretas
        self.url_products = "/api/products/"
        self.url_categories = "/api/categories/"
        self.url_orders = "/api/order/orders/"

    # -------------------- CATEGORY --------------------

    def test_create_category(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.post(self.url_categories, {"name": "Nova Categoria"}, format="json")
        assert response.status_code == 201
        assert Category.objects.filter(name="Nova Categoria").exists()

    def test_list_categories(self):
        response = self.client.get(self.url_categories)
        assert response.status_code == 200
        assert response.data["results"][0]["name"] == self.category.name

    # -------------------- PRODUCT --------------------

    def test_create_product(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.post(
            self.url_products,
            {
                "name": "Produto Novo",
                "description": "Novo",
                "price": 15.5,
                "stock": 7,
                "category": self.category.id,
            },
            format="json",
        )
        assert response.status_code == 201
        assert Product.objects.filter(name="Produto Novo").exists()

    def test_list_products(self):
        response = self.client.get(self.url_products)
        assert response.status_code == 200
        assert response.data["results"][0]["name"] == self.product.name

    # -------------------- ORDER --------------------

    def test_create_order(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("order-list")
        data = {
            "name": "Pedido Teste",
            "product": self.product.id,
            "quantity": 2
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == 201
        assert Order.objects.filter(user=self.user, product=self.product).exists()

    def test_list_orders(self):
        Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=1,
            name="Pedido Teste",
            created_by=self.user
        )
        self.client.force_authenticate(user=self.user)
        url = reverse("order-list")
        response = self.client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert any(o["quantity"] == 1 for o in data.get("results", data))

    def test_update_order(self):
        order = Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=1,
            name="Pedido Teste",
            created_by=self.user
        )
        self.client.force_authenticate(user=self.user)
        url = reverse("order-detail", args=[order.id])
        data = {
            "name": order.name,
            "product": self.product.id,
            "quantity": 5
        }
        response = self.client.put(url, data, format="json")
        assert response.status_code == 200
        order.refresh_from_db()
        assert order.quantity == 5

    def test_delete_order(self):
        order = Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=1,
            name="Pedido Teste",
            created_by=self.user
        )
        self.client.force_authenticate(user=self.user)
        url = reverse("order-detail", args=[order.id])
        response = self.client.delete(url)
        assert response.status_code == 204
        assert not Order.objects.filter(id=order.id).exists()

