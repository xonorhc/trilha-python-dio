from database import metadata
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Table

posts = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("tittle", String(100), nullable=False, unique=True),
    Column("published_at", DateTime, nullable=True),
    Column("published", Boolean, default=False),
    Column("content", String, nullable=False),
)
