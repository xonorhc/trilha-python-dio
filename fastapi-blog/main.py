from contextlib import asynccontextmanager

import databases
import sqlalchemy as sa
from controllers import post
from fastapi import FastAPI

DATABASE_URL = "sqlite:///./db.sqlite3"

database = databases.Database(DATABASE_URL)
metadata = sa.MetaData()
engine = sa.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(post.router)
