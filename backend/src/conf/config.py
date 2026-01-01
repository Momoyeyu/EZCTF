import os

def _getenv(name: str, default: str) -> str:
    value = os.getenv(name)
    return value if value not in (None, "") else default

DATABASE_URL = _getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost/ezctf",
)

SECRET_KEY = _getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = _getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(_getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
