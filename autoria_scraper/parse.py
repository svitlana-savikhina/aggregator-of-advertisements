from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from sqlalchemy import func

from database import SessionLocal
from car_info.models import Car

BASE_URL = "https://auto.ria.com/uk/"

HOME_URL = urljoin(BASE_URL, "auto_hyundai_tucson_34825798.html")


@dataclass
class CarItem:
    name: str
    price: int
    model: str
    brand: str
    region: str
    mileage: int
    color: str
    salon: str
    contacts: str
    cached_at: datetime


def get_contact():
    driver = webdriver.Chrome()
    driver.get(HOME_URL)
    contact = driver.find_element(By.CLASS_NAME, "contact-phone")
    button = contact.find_element(By.CLASS_NAME, "button")
    button.click()
    contacts = driver.find_element(By.CLASS_NAME, "popup-successful-call").text
    driver.close()
    return contacts


def get_advertisement_info():
    page = requests.get(HOME_URL).content
    soup = BeautifulSoup(page, "html.parser")

    name = soup.find("h3", class_="auto-content_title").text.strip()

    price_text = soup.find('div', class_='price_value').find('strong').text.strip()
    price_digits = ''.join(filter(str.isdigit, price_text))
    price = int(price_digits.replace(' ', ''))

    model = soup.find("span", class_="argument d-link__name").text.strip().split()[1]

    brand = soup.find("span", class_="argument d-link__name").text.strip().split()[0]

    region = soup.find(id="breadcrumbs").find_all('span')[-3].text.strip()

    mileage_text = soup.find("dd", class_="mhide").find("span", class_="argument").text.strip()
    mileage = int("".join(filter(str.isdigit, mileage_text)))

    color = (soup.find("div", class_="technical-info", id='details').
             find('span', class_='car-color').find_parent('span', class_='argument').text)

    salon = (soup.find('span', string='Матеріали салону').
             find_next('span', class_='argument').text.strip())

    contacts = get_contact()

    cached_at = func.now()

    return CarItem(
        name=name,
        price=price,
        model=model,
        brand=brand,
        region=region,
        mileage=mileage,
        color=color,
        salon=salon,
        contacts=contacts,
        cached_at=cached_at
    )


def save_car_to_database(car_item):
    car = Car(
        name=car_item.name,
        price=car_item.price,
        model=car_item.model,
        brand=car_item.brand,
        region=car_item.region,
        mileage=car_item.mileage,
        color=car_item.color,
        salon=car_item.salon,
        contacts=car_item.contacts,
        cached_at=car_item.cached_at

    )
    db = SessionLocal()
    db.add(car)
    db.commit()
    db.refresh(car)
    db.close()
    return car


car_item = get_advertisement_info()
save_car_to_database(car_item)

