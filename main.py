from fastapi import FastAPI

from database import engine, Base
from routes import products_router, users_router

Base.metadata.create_all(bind=engine)


# Создание экземпляра FastAPI
app = FastAPI()

app.include_router(products_router)
app.include_router(users_router)

# todo add .env support