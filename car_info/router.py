from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from car_info import crud, schemas
from dependencies import get_db

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/car/{car_id}", response_model=schemas.Car)
def get_car(car_id: int, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id=car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car


@router.get("/cars/", response_model=List[schemas.Car])
def get_cars_by_period(start_date: datetime, end_date: datetime, db: Session = Depends(get_db)):
    return crud.get_cars_by_period(db=db, start_date=start_date, end_date=end_date)


@router.get("/cars/stats/", response_model=schemas.CarStats)
def read_car_stats(brand: str, model: str, db: Session = Depends(get_db)):
    return crud.get_car_stats(db=db, brand=brand, model=model)
