from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from task.model import Difficulty

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    score: int = 100
    category: Optional[str] = None
    difficulty: Difficulty = Difficulty.EASY
    is_visible: bool = True

class TaskCreate(TaskBase):
    flag: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    score: Optional[int] = None
    category: Optional[str] = None
    difficulty: Optional[Difficulty] = None
    is_visible: Optional[bool] = None
    flag: Optional[str] = None

class TaskRead(TaskBase):
    id: int
    solve_count: int = 0
    solved: bool = False
    annex: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class SubmitFlag(BaseModel):
    flag: str

class AnswerResponse(BaseModel):
    correct: bool
    points: int
    msg: str
