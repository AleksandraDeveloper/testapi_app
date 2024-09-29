# это файл для описания схем, необходимых на стороне сервера для описания API, что мы будем принимать и отправлять
from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class ConfigDict:
        from_attributes = True


class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    product_quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int

    class ConfigDict:
        from_attributes = True


class OrderBase(BaseModel):
    creation_date: date
    status: str = "В процессе"


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderResponse(OrderBase):
    id: int
    items: List[OrderItemResponse]

    class ConfigDict:
        from_attributes = True
