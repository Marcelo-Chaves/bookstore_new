import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from order.models import Order
from product.models import Product, Category


@pytest.mark.django_db
class TestOrderCRUD:

    def setup_method(self):
        self.client = APIClient()
        self.url = "/api/orders/"  # URL corrigida para os pedidos
        self.user = User.objects.create_user(username="regular", password="1234")
        self.staff = User.objects.create_user(username="staff", password="1234", is_staff=True)

        # Criando categoria e produto para associar aos pedidos
        self.category = Category.objects.create(name="Categoria Teste")
        self.product = Product.objects.create(
            name="Produto Teste",
            description="Produto para teste",
            price=10.0,
            stock=5,
            category=self.category
        )

    def test_list_orders_requires_auth(self):
        response = self.client.get(self.url)
        assert response.status_code == 401  # não autenticado

    def test_create_order_authenticated(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.post(self.url, {
            "name": "Pedido 1",
            "description": "Teste",
            "quantity": 3,
            "product": self.product.id
        })
        assert response.status_code == 201
        assert Order.objects.filter(name="Pedido 1").exists()

    def test_update_order_authenticated(self):
        self.client.force_authenticate(user=self.staff)
        order = Order.objects.create(
            name="Antigo",
            description="Antigo",
            quantity=1,
            product=self.product,
            created_by=self.user,
            user=self.user
        )
        url_detail = f"{self.url}{order.id}/"
        response = self.client.put(url_detail, {
            "name": "Atualizado",
            "description": order.description,
            "quantity": 5,
            "product": self.product.id
        })
        assert response.status_code == 200
        order.refresh_from_db()
        assert order.name == "Atualizado"
        assert order.quantity == 5

    def test_delete_order_authenticated(self):
        self.client.force_authenticate(user=self.staff)
        order = Order.objects.create(
            name="Excluir",
            description="Excluir",
            quantity=1,
            product=self.product,
            created_by=self.user,
            user=self.user
        )
        url_detail = f"{self.url}{order.id}/"
        response = self.client.delete(url_detail)
        assert response.status_code == 204
        assert not Order.objects.filter(id=order.id).exists()

