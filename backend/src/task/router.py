from typing import List
import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import Session, select

from conf.db import get_session
from user.model import User
from user.deps import get_current_user, get_current_superuser
from task.schema import TaskCreate, TaskRead, TaskUpdate, SubmitFlag, AnswerResponse
from task import service as task_service
from task.model import Solved

router = APIRouter(prefix="/api/v1/task", tags=["task"])

CHALLENGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "challenges")

@router.post("/", response_model=TaskRead)
def create_task(
    task_create: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_superuser)
):
    return task_service.create_task(session, task_create)

@router.get("/", response_model=List[TaskRead])
def get_tasks(
    category: str = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    tasks = task_service.get_tasks(session, category=category)
    
    solved_statement = select(Solved.task_id).where(Solved.user_id == current_user.id)
    solved_task_ids = set(session.exec(solved_statement).all())
    
    result = []
    for task in tasks:
        if not task.is_visible and not current_user.is_superuser:
            continue
            
        task_read = TaskRead.model_validate(task)
        task_read.solved = task.id in solved_task_ids
        result.append(task_read)
        
    return result

@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = task_service.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not task.is_visible and not current_user.is_superuser:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_read = TaskRead.model_validate(task)
    solved_entry = session.exec(select(Solved).where(Solved.task_id == task_id, Solved.user_id == current_user.id)).first()
    task_read.solved = True if solved_entry else False
    
    return task_read

@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_superuser)
):
    return task_service.update_task(session, task_id, task_update)

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_superuser)
):
    task_service.delete_task(session, task_id)
    return {"message": "Successfully deleted task"}

@router.post("/{task_id}/submit", response_model=AnswerResponse)
def submit_flag(
    task_id: int,
    submit: SubmitFlag,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    success = task_service.submit_flag(session, task_id, submit.flag, current_user.id)
    return AnswerResponse(correct=success, points=0, msg="Correct!" if success else "Wrong flag")

@router.get("/{task_id}/attachment")
def download_attachment(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = task_service.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if not task.annex:
        raise HTTPException(status_code=404, detail="No attachment for this task")
        
    file_path = os.path.join(CHALLENGE_DIR, task.annex)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Attachment file not found on server")
        
    return FileResponse(file_path, filename=task.annex)

@router.post("/{task_id}/container")
def create_container(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Mock implementation for frontend compatibility
    # In a real scenario, this would spin up a Docker container
    task = task_service.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    # Check if task type supports container (Web/Pwn)
    # Using hardcoded check for now or based on category
    # Assuming Web=2, Pwn=4
    # if task.category not in ["Web", "Pwn"]: ...
    
    import random
    port = random.randint(20000, 30000)
    return {"host": "127.0.0.1", "port": port}

@router.delete("/{task_id}/container")
def delete_container(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Mock implementation
    return {"message": "Container destroyed"}
