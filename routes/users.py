from typing import List

from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from database import get_db
from models import UserProduct, Product, User
from models import UserBase, UserResponse, UserUpdate
from models import Message

users_router = APIRouter(prefix='/users', tags=['users'])


@users_router.post("/", response_model=UserResponse)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    """Создание нового пользователя"""
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



@users_router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Получение списка всех пользователей"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@users_router.get("/{user_id}", response_model=UserResponse, responses={404: {"model": Message}})
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Получение пользователя по его ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=204, detail="Пользователь не найден")
    return user


@users_router.put("/{user_id}", response_model=UserResponse, responses={404: {"model": Message}})
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """Обновление информации о пользователе"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=204, detail="Пользователь не найден")
    for key, value in user_update.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


@users_router.delete("/{user_id}", response_model=UserResponse, responses={404: {"model": Message}})
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Удаление пользователя по его ID"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=204, detail="Пользователь не найден")
    db.delete(db_user)
    db.commit()
    return db_user


@users_router.get("/products/{user_id}", responses={404: {"model": Message}})
def read_user_products(user_id: int, db: Session = Depends(get_db)):
    """Получение информации о товарах пользователя"""
    products = db.query(UserProduct).filter(UserProduct.user_id == user_id).all()
    print(products)
    if not products:
        raise HTTPException(status_code=204, detail="Пользователь не найден")
    product_name = []
    for el in products:
        product_name.append(db.query(Product).filter(Product.id == el.price_id).all())
    return product_name
