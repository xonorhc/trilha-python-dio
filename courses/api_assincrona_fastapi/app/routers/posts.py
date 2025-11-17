from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from app.db import SessionDep
from app.models import Post, PostCreate, PostPublic, PostUpdate

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=PostPublic)
async def create_post(
    post: PostCreate,
    session: SessionDep,
):
    db_post = Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@router.get("/", response_model=list[PostPublic])
async def read_posts(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Post]:
    posts = session.exec(select(Post).offset(offset).limit(limit)).all()
    return posts


@router.get("/{post_id}", response_model=PostPublic)
async def read_post(post_id: int, session: SessionDep):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.delete("/{post_id}")
async def delete_post(post_id: int, session: SessionDep):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    return {"Ok": True}


@router.patch("/{post_id}", response_model=PostPublic)
async def update_post(post_id: int, post: PostUpdate, session: SessionDep):
    post_db = session.get(Post, post_id)
    if not post_db:
        raise HTTPException(status_code=404, detail="Post not found")
    post_data = post.model_dump(exclude_unset=True)
    post_db.sqlmodel_update(post_data)
    session.add(post_db)
    session.commit()
    session.refresh(post_db)
    return post_db
