from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from conf.alembic_runner import upgrade_head

# Import models to register them with SQLModel
from user import model as user_model
from team import model as team_model
from task import model as task_model
from message import model as message_model

from middleware.auth import setup_jwt_middleware
from user.router import router as user_router
from team.router import router as team_router
from task.router import router as task_router
from common.erri import BusinessError

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Try to run migrations if DB is available
    # upgrade_head()
    yield

app = FastAPI(title="EZCTF Backend", lifespan=lifespan)

@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

app.include_router(user_router)
app.include_router(team_router)
app.include_router(task_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to EZCTF Backend"}

setup_jwt_middleware(app)
