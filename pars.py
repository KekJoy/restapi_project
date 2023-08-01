from pydantic import HttpUrl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from config_data import config
from models import Product


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
