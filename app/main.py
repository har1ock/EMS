
from fastapi import FastAPI
from app.routers import users


app = FastAPI(title="Event Managment API")
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Api is running"}


import os
print(f"Поточна директорія: {os.getcwd()}")
print(f"Чи існує файл бази за шляхом app.db: {os.path.exists('app.db')}")