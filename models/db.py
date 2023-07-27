from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import mapped_column

from database import Base


class Product(Base):
    __tablename__ = "product"

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
    __tablename__ = "user_product"

    id = Column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"))
    product_id = mapped_column(ForeignKey("product.id"))


