from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

FILE = "tasks.json"

app = FastAPI(title="CLI To-Do FastAPI", version="1.0")

class Task(BaseModel):
    task: str

def load_tasks():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f)

@app.get("/tasks")
def get_tasks():
    return load_tasks()

@app.post("/tasks")
def add_task(task: Task):
    tasks = load_tasks()
    tasks.append(task.task)
    save_tasks(tasks)
    return {"message": "Task added!", "task": task.task}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        removed = tasks.pop(task_id)
        save_tasks(tasks)
        return {"message": f"Removed: {removed}"}
    raise HTTPException(status_code=404, detail="Task not found")
