from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone
from enum import IntEnum
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from user.model import User

class TaskType(IntEnum):
    MISC = 0
    CRYPTO = 1
    WEB = 2
    REVERSE = 3
    PWN = 4

class Difficulty(IntEnum):
    EASY = 0
    MEDIUM = 1
    HARD = 2

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(unique=True, index=True)
    description: Optional[str] = None
    src: Optional[str] = None
    annex: Optional[str] = None
    hint: Optional[str] = None
    flag: str
    difficulty: Difficulty = Field(default=Difficulty.EASY)
    score: int = Field(default=100)
    category: Optional[str] = None
    solve_count: int = Field(default=0)
    is_visible: bool = Field(default=True)
    
    # Relationships
    solved_records: list["Solved"] = Relationship(back_populates="task")

class Solved(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    task_id: int = Field(foreign_key="task.id")
    answer_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relationships
    user: "User" = Relationship(back_populates="solved_records")
    task: "Task" = Relationship(back_populates="solved_records")
