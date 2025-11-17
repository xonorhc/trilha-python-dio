from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class PostBase(SQLModel):
    title: str = Field(index=True)
    content: str | None = Field(default=None, index=True)


class Post(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    published_at: datetime | None = Field(default=datetime.now(UTC))
    published: bool = Field(default=False)


class PostCreate(PostBase):
    published: bool


class PostPublic(PostBase):
    id: int


class PostUpdate(PostBase):
    title: str | None
    content: str | None
    published: bool | None
