from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.databace import get_db
from app.tasks.models import Task
from app.tasks.schemas import TaskSchema, TaskUpdate
from app.users.auth import get_current_user

tasks = APIRouter(prefix="/tasks", tags=["Tasks"])


@tasks.get("/", response_model=List[TaskSchema])
async def get_tasks(db: Session = Depends(get_db), current_user: Task = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    tasks = db.query(Task).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks


@tasks.get("/{task_id}", response_model=TaskSchema, status_code=200)
async def get_task(task_id: int, db: Session = Depends(get_db), current_user: Task = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@tasks.post("/create_task", status_code=201)
async def create_task(task: TaskSchema, db: Session = Depends(get_db), current_user: Task = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status or "pending",
        time=task.time,
        user_id=task.user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@tasks.put("/tasks/{task_id}")
async def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db),
                      current_user: Task = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    existing_task = db.query(Task).filter(Task.id == task_id).first()

    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    existing_task.title = task_data.title or existing_task.title
    existing_task.description = task_data.description or existing_task.description
    existing_task.status = task_data.status or existing_task.status
    existing_task.time = task_data.time or existing_task.time

    db.commit()
    db.refresh(existing_task)

    return {"message": "Task updated successfully", "task": existing_task}


@tasks.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db), current_user: Task = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    existing_task = db.query(Task).filter(Task.id == task_id).first()

    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(existing_task)
    db.commit()

    return {"message": "Task deleted successfully"}
