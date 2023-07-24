from sqlalchemy import create_engine, String, Integer, Column, ForeignKey, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from pydantic import BaseModel
from typing import Optional


Base = declarative_base()

class Product(Base):

    __tablename__="Product"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    url = Column(String)


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, index=True)



class UserProduct(Base):

    __tablename__="user_Product"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    price_id = Column(Integer)


engine = create_engine("sqlite:///db.sqlite")
conn = engine.connect()

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Модель данных пользователя для запросов
class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None


#Модель даных товара для запросов

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


# Получение сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def add_item(data:Product):
    exists_name = SessionLocal.query(Product.name).filter(Product.name==data.name)
    if not SessionLocal.query(exists_name.exists()).scalar():
        SessionLocal.add(data)
        SessionLocal.commit()
        print("Товар добавлен")
    elif SessionLocal.query(Product.price).filter(Product.price==data.price):
        print("Цена не изменилась")