from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import os
import dotenv

dotenv.load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
COOKIE_NAME = "access_token"

if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY не встановлений")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=60*3)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
