from typing import List

from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from database import get_db
from models.db import UserProduct, Product, User
from models.inner import UserBase, UserResponse, UserUpdate
from models.types import Message

users_router = APIRouter(prefix='/users', tags=['users'])


@users_router.post("/", response_model=UserResponse)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    """# Создание нового пользователя"""
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Получение списка всех пользователей
@users_router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


# Получение пользователя по его ID
@users_router.get("/{user_id}", response_model=UserResponse, responses={404: {"model": Message}})
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        # todo: поменять все 404 на 204 , не забыть про анотацию ошибок
        raise HTTPException(status_code=204, detail="Пользователь не найден")
    return user


# Обновление информации о пользователе
@users_router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    for key, value in user_update.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


# Удаление пользователя по его ID
@users_router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db.delete(db_user)
    db.commit()
    return db_user


# Получение информации о товара/х пользователя
@users_router.get("/products/{user_id}")
def read_user_products(user_id: int, db: Session = Depends(get_db)):
    products = db.query(UserProduct).filter(UserProduct.user_id == user_id).all()
    print(products)
    if not products:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    product_name = []
    for el in products:
        product_name.append(db.query(Product).filter(Product.id == el.price_id).all())
    return product_name
