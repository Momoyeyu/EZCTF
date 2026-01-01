from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Session, select
from task.model import Task, Solved
from task.schema import TaskCreate, TaskUpdate
from common import erri

def create_task(session: Session, task_create: TaskCreate) -> Task:
    db_task = Task.model_validate(task_create)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def get_task(session: Session, task_id: int) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise erri.not_found("Task not found")
    return task

def get_tasks(session: Session, offset: int = 0, limit: int = 100, category: Optional[str] = None) -> List[Task]:
    statement = select(Task)
    if category:
        # Match category name or integer value if possible
        # Since category is str in model but used as enum often.
        # Let's assume input is string name like "WEB" or "2"
        # If model stores string "WEB", we match directly.
        # If model stores int 2, we cast.
        # Current model: category: Optional[str] = None. 
        # But test used category="WEB".
        # Let's just filter by exact string match for now.
        statement = statement.where(Task.category == category)
        
    return session.exec(statement.offset(offset).limit(limit)).all()

def update_task(session: Session, task_id: int, task_update: TaskUpdate) -> Task:
    db_task = get_task(session, task_id)
    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def delete_task(session: Session, task_id: int):
    db_task = get_task(session, task_id)
    session.delete(db_task)
    session.commit()

def submit_flag(session: Session, task_id: int, flag: str, user_id: int) -> bool:
    task = get_task(session, task_id)
    
    # Check if already solved
    existing_solved = session.exec(select(Solved).where(Solved.task_id == task_id, Solved.user_id == user_id)).first()
    if existing_solved:
        raise erri.bad_request("Task already solved")

    if task.flag == flag:
        # Correct flag
        solved = Solved(
            user_id=user_id,
            task_id=task_id,
            answer_time=datetime.now(timezone.utc)
        )
        session.add(solved)
        
        # Update user score
        from user.model import User
        user = session.get(User, user_id)
        if user:
            user.score += task.score
            user.last_answer_time = datetime.now(timezone.utc)
            session.add(user)
            
            # Update team score
            if user.team_id:
                from team.model import Team
                team = session.get(Team, user.team_id)
                if team:
                    team.score += task.score
                    session.add(team)
        
        # Update task solve count
        task.solve_count += 1
        session.add(task)
            
        session.commit()
        return True
    else:
        return False
