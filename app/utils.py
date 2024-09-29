from sqlalchemy.orm import Session
from fastapi import HTTPException, Path
from app.models import Product


def get_product(db: Session, product_id: int) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product


def check_quantity(db: Session, product_id: int, order_quantity: int):
    product = get_product(db, product_id)
    if product.quantity < order_quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Недостаточное количество товара на складе. Доступно: {product.quantity}",
        )


def update_quantity(db: Session, product_id: int, quantity: int):
    product = get_product(db, product_id)
    product.quantity -= quantity
    db.commit()
    db.refresh(product)
