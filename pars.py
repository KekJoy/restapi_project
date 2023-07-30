from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from models.db import Product


# def add_item(data: Product):
#     exists_name = SessionLocal.query(Product.name).filter(Product.name == data.name)
#     if not SessionLocal.query(exists_name.exists()).scalar():
#         SessionLocal.add(data)
#         SessionLocal.commit()
#         print("Товар добавлен")
#     elif SessionLocal.query(Product.price).filter(Product.price == data.price):
#         print("Цена не изменилась")


def get_price(url):

    service = Service(executable_path=r"C:\Work\restapi_project\chromedriver.exe")
    options = Options()
    driver = webdriver.Chrome(options=options, service=service)

    driver.implicitly_wait(10) 

    driver.get(url)

    price = driver.find_element(By.CLASS_NAME, "eb8dq160").text
    name = driver.find_element(By.CLASS_NAME, "eotjnw00").text
        
    price = int(price.removesuffix('₽').replace(" ", ""))
        
    data = Product(name=name, price=price, url=url)

    driver.quit()

    return data
