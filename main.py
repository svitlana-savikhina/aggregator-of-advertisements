from fastapi import FastAPI
from car_info import router as car_info_router

app = FastAPI()

app.include_router(car_info_router.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

