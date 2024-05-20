import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from sqlalchemy import func

from autoria_scraper.items import CarItem
from database import SessionLocal
from car_info.models import Car


def get_contact(car_url):
    driver = webdriver.Chrome()
    driver.get(car_url)
    accept_cookies_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label.js-close.c-notifier-btn"))
    )
    accept_cookies_button.click()
    contact = driver.find_element(By.CLASS_NAME, "contact-phone")
    button = contact.find_element(By.CLASS_NAME, "button")
    button.click()
    contacts = driver.find_element(By.CLASS_NAME, "popup-successful-call-desk").text
    driver.close()
    return contacts


def get_advertisement_info(car_url):
    page = requests.get(car_url).content
    soup = BeautifulSoup(page, "html.parser")

    name = soup.find("h3", class_="auto-content_title").text.strip()

    price_text = soup.find("div", class_="price_value").find("strong").text.strip()
    price_digits = "".join(filter(str.isdigit, price_text))
    price = int(price_digits.replace(" ", ""))

    model = soup.find("span", class_="argument d-link__name").text.strip().split()[1]

    brand = soup.find("span", class_="argument d-link__name").text.strip().split()[0]

    region = soup.find(id="breadcrumbs").find_all("span")[-3].text.strip()

    mileage_text = (
        soup.find("dd", class_="mhide").find("span", class_="argument").text.strip()
    )
    mileage = int("".join(filter(str.isdigit, mileage_text)))

    color_element = soup.find("div", class_="technical-info", id="details")
    color = (
        color_element.find("span", class_="car-color").find_parent("span", class_="argument").text
        if color_element and color_element.find("span", class_="car-color") else "Unknown"
    )

    salon_element = soup.find("span", string="Матеріали салону")
    salon = salon_element.find_next("span", class_="argument").text.strip() if salon_element else "Unknown"

    contacts = get_contact(car_url)

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
        cached_at=cached_at,
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
        cached_at=car_item.cached_at,
    )
    db = SessionLocal()
    db.add(car)
    db.commit()
    db.refresh(car)
    db.close()
    return car
