from dataclasses import dataclass
from datetime import datetime


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
