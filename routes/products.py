from typing import List

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from pydantic import HttpUrl
from sqlalchemy.orm import Session

from database import get_db
from models.db import Product, UserProduct
from models.inner import ProductBase, ProductResponse
from pars import get_price

products_router = APIRouter(prefix='/products', tags=['product'])


# Создание нового товара
@products_router.post("/", response_model=ProductBase)
def create_product(url: HttpUrl, user_id: int, db: Session = Depends(get_db)):
    db_product = get_price(url)
    is_include = db.query(Product).filter(Product.name == db_product.name).first()
    if is_include:
        user_product = UserProduct(user_id=user_id, price_id=is_include.id)
        db.add(user_product)
        db.commit()
    else:
        db.add(db_product)
        db.commit()
        user_product = UserProduct(user_id=user_id, price_id=db_product.id)
        db.add(user_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    return db_product


# Получение списка всех товаров
@products_router.get("/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products


# Получение информации о товаре по его ID
@products_router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product


# Обновление цены товара
@products_router.put("/{product_id}", response_model=ProductResponse)
def update_price(product_id: int, db: Session = Depends(get_db)):
    db_products = db.query(Product).filter(Product.id == product_id).first()
    if not db_products:
        raise HTTPException(status_code=404, detail="Товар не найден")
    else:
        product_url = db_products.url
        new_price = get_price(product_url)
        db.query(Product).filter(Product.id == product_id).update({'price': new_price.price})
        db.commit()
    return db_products


# Удаление товара по его ID
@products_router.delete("/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    db.delete(db_product)
    db.commit()
    return db_product
