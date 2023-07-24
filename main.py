from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import update
from typing import List, Optional
from database import UserResponse, UserBase, User, UserUpdate, Product, ProductBase, ProductResponse, get_db, UserProduct, UserProductBase, UserProductResponse
from pars import get_price

# Создание экземпляра FastAPI
app = FastAPI()


# Создание нового пользователя
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#Создание нового товара
@app.post("/products/", response_model=ProductBase)
def create_product(url, user_id: int, db: Session = Depends(get_db)):
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

# Получение списка всех пользователей
@app.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

#Получение списка всех товаров
@app.get("/products/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products


# Получение пользователя по его ID
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

# Получение информации о товаре по его ID
@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

#Получение информации о товарах пользователя
@app.get("/user_products/{user_id}")
def read_user_products(user_id: int, db: Session = Depends(get_db)):
    products = db.query(UserProduct).filter(UserProduct.user_id == user_id).all()
    print(products)
    if not products:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    product_name = []
    for el in products:
        product_name.append(db.query(Product).filter(Product.id == el.price_id).all())
    return product_name


# Обновление информации о пользователе
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    for key, value in user_update.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


#Обновление цены товара
@app.put("/products/{product_id}", response_model=ProductResponse)
def update_price(product_id: int, db: Session = Depends(get_db)):
    db_products = db.query(Product).filter(Product.id == product_id).first()
    if not db_products:
        raise HTTPException(status_code=404, detail="Товар не найден")
    else:
        product_url = db_products.url
        new_price = get_price(product_url)
        db.query(Product).filter(Product.id == product_id).update({'price':new_price.price})
        db.commit()
    return db_products


# Удаление пользователя по его ID
@app.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db.delete(db_user)
    db.commit()
    return db_user


#Удаление товара по его ID
@app.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    db.delete(db_product)
    db.commit()
    return db_product
