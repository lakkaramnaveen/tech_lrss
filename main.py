from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = ""
    completed: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Dummy database
tasks_db: List[Task] = []

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks_db

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    task.id = str(uuid4())
    tasks_db.append(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, updated_task: Task):
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/tasks/{task_id}", response_model=Task)
def update_partial_task(task_id: str, task_update: TaskUpdate):
    for task in tasks_db:
        if task.id == task_id:
            if task_update.title is not None:
                task.title = task_update.title
            if task_update.description is not None:
                task.description = task_update.description
            if task_update.completed is not None:
                task.completed = task_update.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    global tasks_db
    tasks_db = [task for task in tasks_db if task.id != task_id]
    return {"detail": "Task deleted"}
