from fastapi import FastAPI

from app import security
from app.db import create_db_and_tables
from app.routers import posts

app = FastAPI()

app.include_router(posts.router)
app.include_router(security.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
