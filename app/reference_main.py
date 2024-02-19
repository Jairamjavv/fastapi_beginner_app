from typing import Optional
from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()


# request method:GET route:/
@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Running FastAPI."}


# request method:GET route:/posts
@app.get("/posts")
def get_posts():
    pass


class PostModel(BaseModel):
    title: str
    description: str
    # if provided then updates the value else takes the default value
    published: bool = True
    # Optional takes a datatype and if provided updates it or remains optional as
    rating: Optional[int] = None


# request method:GET route:/posts
@app.post("/posts/create")
def create_posts(post_payload: PostModel) -> dict[str, dict[str, str]]:
    """
    Request: JSON Body Params from client
    API: /posts
    Response: returns a json object of post details alone with the request

    """
    print_pydantic_payload(post_payload)
    return {
        "data": {
            "post_id": "p01",
            "title": post_payload.title,
            "description": post_payload.description,
        }
    }


def print_pydantic_payload(post_payload: PostModel) -> None:
    print(38, post_payload.model_dump())  # python dictionary format
    print(39, post_payload.model_dump_json())  # universal json format
