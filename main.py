from contextlib import contextmanager


from pydantic import BaseModel, Field
from fastapi import FastAPI, Depends
from typing import Generator
from fastapi.middleware.cors import CORSMiddleware
from models import init_db, async_session, User, Task
import requests as rq


#------------------------------------#
@asynccontextmanager
async def lifespan(app: FastAPI) -> Generator:
    await init_db()
    yield



#------------------------------------#

app = FastAPI(title="Task Manager API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/tasks/{tg_id}")
async def tasks(tg_id:int):
    user = await rq.add_user(tg_id)
    return await rq.get_tasks(user.id)

@app.get("/api/main/{tg_id}")
async def profile(tg_id: int):
    user = await rq.add_user(tg_id)
    completed_tasks_count = await rq.get_completed_tasks_count(user.id)
    return {"completed_tasks_count": completed_tasks_count}