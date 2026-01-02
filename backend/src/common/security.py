import hashlib
import time
from typing import Any, Dict

from jwt import PyJWT, PyJWTError

from common import erri
from conf.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Use configurations from config.py
JWT_SECRET = SECRET_KEY
JWT_ALGORITHM = ALGORITHM
JWT_EXPIRE_SECONDS = ACCESS_TOKEN_EXPIRE_MINUTES * 60
PASSWORD_SALT = "ezctf_salt"  # You might want to move this to config or env

def get_password_hash(password: str) -> str:
    # Using SHA512 with salt as per legacy/demo reference
    return hashlib.sha512((password + PASSWORD_SALT).encode("utf-8")).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password) == hashed_password

def create_access_token(subject: Any) -> str:
    now = int(time.time())
    payload = {
        "sub": str(subject),
        "iat": now,
        "exp": now + JWT_EXPIRE_SECONDS
    }
    return PyJWT().encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token: str) -> Dict[str, Any]:
    try:
        decoded = PyJWT().decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded
    except PyJWTError:
        raise erri.unauthorized("Invalid token")
