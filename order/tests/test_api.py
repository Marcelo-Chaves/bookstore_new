#agora temos que acrescentar no product/tests/test_api.py
import pytest
from rest_framework.test import APIClient
from order.models import Order


@pytest.fixture
def client():
    return APIClient()


def salvar_dados_teste(tipo_operacao, dados, status):
    with open("dados_testes_order.txt", "a", encoding="utf-8") as f:
        f.write(f"== {tipo_operacao.upper()} ==\n")
        for key, value in dados.items():
            f.write(f"{key}: {value}\n")
        f.write(f"Status HTTP: {status}\n")
        f.write("-" * 40 + "\n")


@pytest.mark.django_db
def test_create_order(client):
    data = {
        "customer_name": "Marcelo Chaves",
        "email": "marcelo.chaves@gmail.com",
        "product_name": "Livros",
        "quantity": 100,
        "price": "20.00",
        "status": "pending"
    }

    response = client.post("/api/order/orders/", data, format="json")
    salvar_dados_teste("POST - Criar Pedido", data, response.status_code)

    assert response.status_code == 201
    assert Order.objects.count() == 1


@pytest.mark.django_db
def test_list_orders(client):
    response = client.get("/api/order/orders/")
    salvar_dados_teste("GET - Listar Pedidos", {}, response.status_code)
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_order(client):
    order = Order.objects.create(
        customer_name="João Silva",
        email="joao.silva@gmail.com",
        product_name="Caneta",
        quantity=10,
        price="5.00",
        status="pending"
    )

    data = {
        "customer_name": "João Silva Atualizado",
        "email": "joao.silva@gmail.com",
        "product_name": "Caneta Azul",
        "quantity": 15,
        "price": "7.00",
        "status": "confirmed"
    }

    response = client.put(f"/api/order/orders/{order.id}/", data, format="json")
    salvar_dados_teste("PUT - Atualizar Pedido", data, response.status_code)

    assert response.status_code == 200
    order.refresh_from_db()
    assert order.customer_name == "João Silva Atualizado"


@pytest.mark.django_db
def test_delete_order(client):
    order = Order.objects.create(
        customer_name="Carlos Teste",
        email="carlos@email.com",
        product_name="Caderno",
        quantity=5,
        price="15.00",
        status="pending"
    )

    response = client.delete(f"/api/order/orders/{order.id}/")
    salvar_dados_teste("DELETE - Remover Pedido", {"id": order.id}, response.status_code)

    assert response.status_code == 204
    assert Order.objects.count() == 0

