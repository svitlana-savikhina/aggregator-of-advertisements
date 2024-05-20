from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from autoria_scraper.parse import get_advertisement_info, save_car_to_database
from car_info import crud, schemas
from dependencies import get_db
from user import models
from user.auth import get_current_active_user

router = APIRouter()


@router.get("/parse_car_info/",
            summary="Parse car information",
            description="Parses car information from the given URL and saves it to the database")
def parse_car_info(car_url: str = Query(..., description="URL of the car advertisement"),
                   current_user: models.User = Depends(get_current_active_user),
                   db: Session = Depends(get_db)):
    car_item = get_advertisement_info(car_url)
    saved_car = save_car_to_database(car_item)
    return {
        "message": "Car information parsed and saved successfully!",
        "car_id": saved_car.id,
    }


@router.get("/car/{car_id}", response_model=schemas.Car)
def get_car(
    car_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    db_car = crud.get_car(db, car_id=car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car


@router.get("/cars/", response_model=List[schemas.Car])
def get_cars_by_period(
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    if start_date >= end_date:
        raise HTTPException(
            status_code=400, detail="Start date must be before end date"
        )
    return crud.get_cars_by_period(db=db, start_date=start_date, end_date=end_date)


@router.get("/cars/stats/", response_model=schemas.CarStats)
def read_car_stats(
    brand: str,
    model: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return crud.get_car_stats(db=db, brand=brand, model=model)
