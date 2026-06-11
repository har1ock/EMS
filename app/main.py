
from fastapi import FastAPI
from app.routers import users, events

app = FastAPI(title="Event Managment API")

app.include_router(users.router)
app.include_router(events.router)

@app.get("/")
def root():
    return {"message": "Api is running"}
