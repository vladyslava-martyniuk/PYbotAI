import os
from dotenv import load_dotenv
load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
COOKIE_NAME = os.getenv("COOKIE_NAME", "access_token")

if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not set")