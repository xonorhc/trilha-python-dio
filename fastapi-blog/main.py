from contextlib import asynccontextmanager

import databases
import sqlalchemy as sa
from controllers import post
from fastapi import FastAPI

DATABASE_URL = "sqlite:///./db.sqlite3"

database = databases.Database(DATABASE_URL)
metadata = sa.MetaData()
engine = sa.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


@asynccontextmanager
async def lifespan(app: FastAPI):
    from models.post import posts

    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(post.router)
