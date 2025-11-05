from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class PostBase(SQLModel):
    title: str = Field(index=True)
    content: str | None = Field(default=None, index=True)


class Post(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    published_at: datetime | None = Field(default=datetime.now(UTC))
    published: bool = Field(default=False)


class PostIn(PostBase):
    published: bool


class PostOut(PostBase):
    id: int


class PostUpdate(PostBase):
    title: str | None
    content: str | None
    published: bool | None


sqlite_file_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/post/", response_model=PostOut)
def create_post(post: PostIn, session: SessionDep):
    db_post = Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@app.get("/posts/", response_model=list[PostOut])
def read_posts(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Post]:
    posts = session.exec(select(Post).offset(offset).limit(limit)).all()
    return posts


@app.get("/posts/{post_id}", response_model=PostOut)
def read_post(post_id: int, session: SessionDep):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, session: SessionDep):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    return {"Ok": True}


@app.patch("/posts/{post_id}", response_model=PostOut)
def update_post(post_id: int, post: PostUpdate, session: SessionDep):
    post_db = session.get(Post, post_id)
    if not post_db:
        raise HTTPException(status_code=404, detail="Post not found")
    post_data = post.model_dump(exclude_unset=True)
    post_db.sqlmodel_update(post_data)
    session.add(post_db)
    session.commit()
    session.refresh(post_db)
    return post_db
