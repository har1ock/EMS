
from fastapi import FastAPI

app = FastAPI(title="Event Managment API")

@app.get("/")
def root():
    return {"message": "Api is running"}