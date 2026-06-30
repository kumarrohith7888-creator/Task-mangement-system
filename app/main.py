from fastapi import FastAPI
from app.database import Base, engine
from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management System",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def home():
    return {"message": "Welcome to Task Management System"}