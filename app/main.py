from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import session_local, engine

from app.models import Base, Product, Order
from app.schemas import (
    ProductCreate,
    ProductResponse,
    OrderCreate,
    OrderResponse,
    ProductUpdate,
)
from app.utils import get_product, check_quantity, update_quantity

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/products/", response_model=ProductResponse)  # Создание товара
def create_product(
    product: ProductCreate, db: Session = Depends(get_db)
) -> ProductResponse:
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/products/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.get("/products/{id}", response_model=ProductResponse)
def get_product_by_id(
    product_id: int, db: Session = Depends(get_db)
) -> ProductResponse:
    product = get_product(db, product_id)
    return product


@app.put("/products/{id}", response_model=ProductResponse)
def update_product(
    product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)
) -> ProductResponse:
    product = get_product(db, product_id)

    product.name = product_update.name
    product.description = product_update.description
    product.price = product_update.price
    product.quantity = product_update.quantity

    db.commit()
    db.refresh(product)
    return product


@app.delete("/products/{id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    db.delete(product)
    db.commit()
    return {"detail": "Товар удален"}


@app.post("/orders/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)) -> OrderResponse:
    for item in order.items:
        check_quantity(db, item.product_id, item.product_quantity)
        update_quantity(db, item.product_id, item.product_quantity)
    db_order = Order(creation_date=order.creation_date, status=order.status)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@app.get("/orders/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@app.get("/orders/{id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)) -> OrderResponse:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


@app.patch("/orders/{id}/status", response_model=OrderResponse)
def update_status(
    order_id: int, status: str, db: Session = Depends(get_db)
) -> OrderResponse:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    order.status = status
    db.commit()
    db.refresh(order)
    return order
