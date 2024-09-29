from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_product():
    response = client.post(
        "/products/",
        json={
            "name": "Диван",
            "description": "Мягкий диван красного цвета",
            "price": 30250.99,
            "quantity": 7,
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Диван"
    assert response.json()["price"] == 30250.99
    assert response.json()["quantity"] == 7


def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_product_by_id():
    # создание тестового товара
    create_response = client.post(
        "/products/",
        json={
            "name": "Стол",
            "description": "Белый стол из дерева",
            "price": 12105.89,
            "quantity": 18,
        },
    )
    product_id = create_response.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == product_id
    assert response.json()["name"] == "Стол"
    assert response.json()["quantity"] == 18


def test_update_product():
    create_response = client.post(
        "/products/",
        json={
            "name": "Кресло",
            "description": "Удобная спинка, мягкие подлокотники",
            "price": 5100.00,
            "quantity": 36,
        },
    )
    product_id = create_response.json()["id"]

    response = client.put(
        f"/products/{product_id}",
        json={
            "name": "Кресло",
            "description": "Удобная спинка, мягкие подлокотники",
            "price": 5100.00,
            "quantity": 34,
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Кресло"
    assert response.json()["quantity"] == 34


def test_create_order():
    product_response = client.post(
        "/products/",
        json={
            "name": "Тумбочка",
            "description": "Прикроватная тумбочка с удобными ручками",
            "price": 2500.00,
            "quantity": 26,
        },
    )
    product_id = product_response.json()["id"]
    response = client.post(
        "/orders/",
        json={
            "creation_date": "2024-09-25",
            "status": "Доставлен",
            "items": [{"product_id": product_id, "product_quantity": 1}],
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Доставлен"


def test_get_orders():
    response = client.get("/orders/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
