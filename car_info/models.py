from sqlalchemy import Column, Integer, String, DateTime, func

from database import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    model = Column(String)
    brand = Column(String)
    region = Column(String)
    mileage = Column(Integer)
    color = Column(String)
    salon = Column(String)
    contacts = Column(String)
    cached_at = Column(DateTime, default=func.now(), index=True)
