#agora temos que acrescentar no product/tests/test_api.py
import pytest
from rest_framework.test import APIClient
from order.models import Order

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_create_order(client):
    data = {
        "customer_name": "marcelo chaves",
        "email": "marcelo.chaves@gmail.com",
        "product_name": "livros",
        "quantity": "100",
        "price": "20.00",  # Corrigido: usar ponto, não vírgula
        "status": "pending"
    }

    response = client.post("/api/order/orders/", data, format="json")

    # Salva os dados em um arquivo
    with open("dados_testes_order.txt", "a", encoding="utf-8") as f:
        f.write("== Novo Pedido Criado ==\n")
        for key, value in data.items():
            f.write(f"{key}: {value}\n")
        f.write(f"Status HTTP: {response.status_code}\n")
        f.write("-" * 40 + "\n")

    assert response.status_code == 201
    assert Order.objects.count() == 1

