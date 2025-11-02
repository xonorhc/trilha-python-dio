from datetime import UTC, datetime

from fastapi import FastAPI

app = FastAPI()

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


@app.get("/posts")
def read_posts(published: bool, skip: int = 0, limit: int = 10):
    return [
        post for post in fake_db[skip : skip + limit] if post["published"] is published
    ]


@app.get("/posts/{framework}")
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
