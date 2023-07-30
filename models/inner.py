from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """ Модель данных пользователя для запросов"""
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class ProductBase(BaseModel):
    """Модель данных товара для запросов"""
    name: str
    price: int


class UserProductBase(BaseModel):
    """Модель данных свяхи товаров и пользователей"""
    id: int
    user_id: int
    price_id: int


class UserResponse(UserBase):
    """Модель данных пользователя с ID (используется при возврате данных из базы данных)"""
    id: int


# Модель данных товара с ID
class ProductResponse(ProductBase):
    """Модель данных товара с ID"""
    id: int


class UserProductResponse(UserProductBase):
    """Связь товара и пользователя"""
    id: list[UserProductBase]


class UserUpdate(UserBase):
    """Модель данных пользователя для обновления (с опциональными полями)"""
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
