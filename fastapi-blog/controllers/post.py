from database import database
from fastapi import APIRouter, Response, status
from models.post import posts
from schemas.post import PostIn
from views.post import PostOut

router = APIRouter(prefix="/posts")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostOut)
def create_post(post: PostIn):
    return post


@router.get("/", response_model=list[PostOut])
def read_posts(
    response: Response,
    published: bool = True,
    skip: int = 0,
    limit: int = 10,
):
    query = posts.select()
    return database.fetch_all(query)
