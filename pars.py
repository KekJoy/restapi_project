from pydantic import HttpUrl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from models import Product
from config_data import config


# def add_item(data: Product):
#     exists_name = SessionLocal.query(Product.name).filter(Product.name == data.name)
#     if not SessionLocal.query(exists_name.exists()).scalar():
#         SessionLocal.add(data)
#         SessionLocal.commit()
#         print("Товар добавлен")
#     elif SessionLocal.query(Product.price).filter(Product.price == data.price):
#         print("Цена не изменилась")


def get_price(url: HttpUrl):
    service = Service(executable_path=config.CHROME_DRIVER_PATH)
    options = Options()
    driver = webdriver.Chrome(options=options, service=service)

    driver.implicitly_wait(10)

    driver.get(str(url))

    price = driver.find_element(By.CLASS_NAME, "eb8dq160").text
    name = driver.find_element(By.CLASS_NAME, "eotjnw00").text

    price = int(price.removesuffix('₽').replace(" ", ""))

    data = Product(name=name, price=price, url=(str(url)))

    driver.quit()

    return data


if __name__ == '__main__':
    url = "https://www.citilink.ru/product/smartfon-honor-x8a-128gb-6gb-goluboi-3g-4g-2sim-6-7-ltps-1080x2388-and-1911907/"
    get_price(HttpUrl(url))
