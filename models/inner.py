from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """ Модель данных пользователя для запросов"""
    username: str
    email: EmailStr
    full_name: Optional[str] = None


# Модель даных товара для запросов
class ProductBase(BaseModel):
    name: str
    price: int


class UserProductBase(BaseModel):
    id: int
    user_id: int
    price_id: int


# Модель данных пользователя с ID (используется при возврате данных из базы данных)
class UserResponse(UserBase):
    id: int


# Модель данных товара с ID
class ProductResponse(ProductBase):
    id: int


# Связь товара и пользователя
class UserProductResponse(UserProductBase):
    id: list[UserProductBase]


# Модель данных пользователя для обновления (с опциональными полями)
class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
