from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Cookie, FastAPI, Header, Response, status
from schemas.post import PostIn
from views.post import PostOut

router = APIRouter(prefix="/posts")

fake_db = [
    {
        "title": f"Criando uma aplicacao com Django",
        "date": datetime.now(UTC),
        "published": False,
    },
    {
        "title": f"Criando uma aplicacao com FastAPI",
        "date": datetime.now(UTC),
        "published": True,
    },
    {
        "title": f"Criando uma aplicacao com Flask",
        "date": datetime.now(UTC),
        "published": True,
    },
    {
        "title": f"Criando uma aplicacao com Startlett",
        "date": datetime.now(UTC),
        "published": True,
    },
]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostOut)
def create_post(post: PostIn):
    fake_db.append(post.model_dump())
    return post


@router.get("/", response_model=list[PostOut])
def read_posts(
    response: Response,
    published: bool = True,
    skip: int = 0,
    limit: int = 10,
    ads_id: Annotated[str | None, Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
):
    response.set_cookie(key="user", value="email@mail.com")
    print(f"Cookie: {ads_id}")
    print(f"User-agent: {user_agent}")
    return [
        post for post in fake_db[skip : skip + limit] if post["published"] is published
    ]


@router.get("/{framework}", response_model=PostOut)
def read_framework_posts(framework: str):
    return {
        "posts": [
            {
                "title": f"Criando uma aplicacao com {framework}",
                "date": datetime.now(UTC),
            },
            {
                "title": f"Internacionalizando uma app {framework}",
                "date": datetime.now(UTC),
            },
        ]
    }
