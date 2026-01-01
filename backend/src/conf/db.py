from sqlmodel import create_engine, SQLModel
from conf.config import DATABASE_URL

# echo=True for debugging, set to False in production
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    from sqlmodel import Session
    with Session(engine) as session:
        yield session
