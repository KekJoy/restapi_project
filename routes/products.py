from typing import List

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from pydantic import HttpUrl
from sqlalchemy.orm import Session

from database import get_db
from models import Product, UserProduct
from models import ProductBase, ProductResponse
from pars import get_price
from models import Message

products_router = APIRouter(prefix='/products', tags=['product'])


@products_router.post("/", response_model=ProductBase)
def create_product(url: HttpUrl, user_id: int, db: Session = Depends(get_db)):
    """Создание нового товара"""
    db_product = get_price(url)
    is_include = db.query(Product).filter(Product.name == db_product.name).first()
    if is_include:
        user_product = UserProduct(user_id=user_id, product_id=is_include.id)
        db.add(user_product)
        db.commit()
    else:
        db.add(db_product)
        db.commit()
        user_product = UserProduct(user_id=user_id, product_id=db_product.id)
        db.add(user_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    return db_product


@products_router.get("/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Получение списка всех товаров"""
    products = db.query(Product).offset(skip).limit(limit).all()
    return products


@products_router.get("/{product_id}", response_model=ProductResponse, responses={404: {"model": Message}})
def read_product(product_id: int, db: Session = Depends(get_db)):
    """Получение информации о товаре по его ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=204, detail="Товар не найден")
    return product


@products_router.put("/{product_id}", response_model=ProductResponse, responses={404: {"model": Message}})
def update_price(product_id: int, db: Session = Depends(get_db)):
    """Обновление цены товара"""
    db_products = db.query(Product).filter(Product.id == product_id).first()
    if not db_products:
        raise HTTPException(status_code=204, detail="Товар не найден")
    else:
        product_url = db_products.url
        new_price = get_price(product_url)
        db.query(Product).filter(Product.id == product_id).update({'price': new_price.price})
        db.commit()
    return db_products


@products_router.delete("/{product_id}", response_model=ProductResponse, responses={404: {"model": Message}})
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """ Удаление товара по его ID"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=204, detail="Товар не найден")
    db.delete(db_product)
    db.commit()
    return db_product
