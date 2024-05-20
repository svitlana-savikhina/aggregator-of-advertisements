from pydantic import BaseModel
from datetime import datetime


class CarBase(BaseModel):
    name: str
    price: int
    model: str
    brand: str
    region: str
    mileage: int
    color: str
    salon: str
    contacts: str


class Car(CarBase):
    id: int
    cached_at: datetime

    class Config:
        orm_mode: True


class CarStats(BaseModel):
    brand: str
    model: str
    min_price: int
    max_price: int
    count_per_day: int
    count_per_week: int
    count_per_month: int
