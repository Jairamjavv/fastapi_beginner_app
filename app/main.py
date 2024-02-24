"""a social media post management CRUD application"""

from fastapi import status, FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import Any, Optional
from random import randint

# from app.db_connection import get_db_connection
from db_connection import get_db_connection

"""
TODO: create post/s
    TODO: fetch details from user
    TODO: validate the details
    TODO: store the details in db
TODO: read all posts
TODO: read post using post_id
TODO: update existing post using post_id 
{PUT: pass entire information to update}
{PATCH: pass certain information to update}
TODO: delete all posts
TODO: delete a post using post_id
"""

app = FastAPI()

# in memory storage of posts
posts = {}

conn = get_db_connection()
print(30, conn)


class PostModel(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False


def store_post(post: PostModel) -> int:
    id_ = randint(1, len(posts) + 1)
    posts[id_] = {
        "title": post.title,
        "content": post.content,
        "published": post.published,
    }
    return id_


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post_payload: PostModel) -> dict[str, Any]:
    id_ = store_post(post_payload)
    return {"message": f"Post with id:{id_} created.", "status_code": 200}


@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts() -> dict:
    return posts


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)  # path parameter
def get_post(id: int, response: Response) -> dict[str, Any]:
    for k, v in posts.items():
        if k == id:
            return v
    """
        Below can be used as an alternative to HTTPException in a detailed way
        response.status_code = status.HTTP_404_NOT_FOUND
        response.body = f"No post with id:{id} found.".encode("utf-8")
        return response
    """
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id:{id} found."
    )


@app.patch("/posts/{id}", status_code=status.HTTP_206_PARTIAL_CONTENT)
def update_post(id: int, update_post: PostModel) -> Response:
    if id in posts.keys():
        posts[id]["title"] = (
            update_post.title if update_post.title else posts[id]["title"]
        )
        posts[id]["content"] = (
            update_post.content if update_post.content else posts[id]["content"]
        )
        posts[id]["published"] = (
            update_post.published if update_post.published else posts[id]["published"]
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id:{id} found."
        )
    return Response(
        status_code=status.HTTP_200_OK, content=f"Updated post with id:{id}"
    )


@app.delete("/posts/all", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_posts() -> None:
    global posts
    if posts:
        posts = {}


# whenever we delete anything, we should use 204 and the response should not return any message
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int) -> Response:
    if id in posts.keys():
        del posts[id]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id:{id} does not exist.",
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
