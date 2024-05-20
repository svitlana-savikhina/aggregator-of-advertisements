from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from autoria_scraper.parse import get_advertisement_info
from car_info import models, schemas

CACHE_EXPIRATION_TIME = timedelta(days=1)


def get_car(db: Session, car_id: int):
    return db.query(models.Car).filter(models.Car.id == car_id).first()


def get_cars_by_period(db: Session, start_date: datetime, end_date: datetime):
    if start_date >= end_date:
        raise ValueError("Start date must be before end date")
    return (
        db.query(models.Car)
        .filter(models.Car.cached_at >= start_date, models.Car.cached_at <= end_date)
        .all()
    )


"""Function to Retrieve Car Statistics by Brand and Model"""


def get_car_stats(db: Session, brand: str, model: str):
    min_price = (
        db.query(models.Car)
        .filter(models.Car.brand == brand, models.Car.model == model)
        .order_by(models.Car.price.asc())
        .first()
        .price
    )
    max_price = (
        db.query(models.Car)
        .filter(models.Car.brand == brand, models.Car.model == model)
        .order_by(models.Car.price.desc())
        .first()
        .price
    )

    today = datetime.now()
    day_ago = today - timedelta(days=1)
    week_ago = today - timedelta(weeks=1)
    month_ago = today - timedelta(days=30)

    count_per_day = (
        db.query(models.Car)
        .filter(
            models.Car.brand == brand,
            models.Car.model == model,
            models.Car.cached_at >= day_ago,
        )
        .count()
    )
    count_per_week = (
        db.query(models.Car)
        .filter(
            models.Car.brand == brand,
            models.Car.model == model,
            models.Car.cached_at >= week_ago,
        )
        .count()
    )
    count_per_month = (
        db.query(models.Car)
        .filter(
            models.Car.brand == brand,
            models.Car.model == model,
            models.Car.cached_at >= month_ago,
        )
        .count()
    )

    return schemas.CarStats(
        brand=brand,
        model=model,
        min_price=min_price,
        max_price=max_price,
        count_per_day=count_per_day,
        count_per_week=count_per_week,
        count_per_month=count_per_month,
    )


"""Updating cached data in the database daily"""


def get_cached_data(db: Session):
    cached_data = db.query(models.Car).order_by(models.Car.cached_at.desc()).first()
    return cached_data


def update_cached_data(db: Session):
    time_since_last_update = datetime.now() - get_cached_data(db).cached_at
    if time_since_last_update < CACHE_EXPIRATION_TIME:
        return
    else:
        new_data = get_advertisement_info()
        car = models.Car(
            name=new_data["name"],
            price=new_data["price"],
            model=new_data["model"],
            brand=new_data["brand"],
            region=new_data["region"],
            mileage=new_data["mileage"],
            color=new_data["color"],
            salon=new_data["salon"],
            contacts=new_data["contacts"],
            cached_at=datetime.now(),
        )
        db.add(car)
        db.commit()
        db.refresh(car)
        return car
