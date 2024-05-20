from typing import Annotated

from fastapi import FastAPI, Depends

from user import routers as user_router
from car_info import routers as car_info_router
from user.auth import oauth2_scheme

app = FastAPI()

app.include_router(car_info_router.router)
app.include_router(user_router.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
