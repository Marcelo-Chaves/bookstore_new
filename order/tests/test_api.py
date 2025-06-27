#agora temos que acrescentar no product/tests/test_api.py
import pytest
from rest_framework.test import APIClient
from order.models import Order

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_create_multiple_orders(client):
    pedidos = [
        {
            "customer_name": "marcelo chaves",
            "email": "marcelo.chaves@gmail.com",
            "product_name": "livros",
            "quantity": "100",
            "price": "20.00",
            "status": "pending"
        },
        {
            "customer_name": "ana silva",
            "email": "ana.silva@gmail.com",
            "product_name": "cadernos",
            "quantity": "50",
            "price": "10.00",
            "status": "pending"
        }
    ]

    with open("dados_testes_order.txt", "a", encoding="utf-8") as f:
        for pedido in pedidos:
            response = client.post("/api/order/orders/", pedido, format="json")


            f.write("== Novo Pedido Criado ==\n")
            for key, value in pedido.items():
                f.write(f"{key}: {value}\n")
            f.write(f"Status HTTP: {response.status_code}\n")
            f.write("-" * 40 + "\n")

            assert response.status_code == 201

    assert Order.objects.count() == len(pedidos)
