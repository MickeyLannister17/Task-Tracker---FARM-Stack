from fastapi import FastAPI, HTTPException, status

from fastapi.middleware.cors import CORSMiddleware

from model import Todo

app = FastAPI()


from database import (
    fetch_all_todos,
    fetch_one_todo,
    create_todo,
    remove_todo,
    update_todo,
)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"ping": "pong"}


@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response


@app.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_id(title):
    response = await fetch_one_todo()
    if response:
        return response
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        reason="There is no TODO item with title {}".format(title),
    )


@app.post("/api/todo/", response_model=Todo)
async def post_todo(todo: Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, reason="Something went wrong"
    )


@app.put("/api/todo/{title}/", response_model=Todo)
async def update_todo(title: str, desc: str):
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        reason="There is no TODO item with title {}".format(title),
    )


@app.delete("/api/todo/{title}")
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return "Item succesfully deleted from the TODO !"

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        reason="There is no TODO item with title {}".format(title),
    )
