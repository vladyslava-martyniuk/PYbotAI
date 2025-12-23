from pydantic import BaseModel
from typing import Optional
# ===== USERS =====
class CreateUser(BaseModel):
    username: str
    email: str
    password: str
    date_of_birth: str
    role_id: int
    session: str
    is_baned: bool


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    password: str
    age: Optional[int] = None
    role_id: int
    session: str
    is_baned: bool

    class Config:
        orm_mode = True

# ===== ROLES =====
class CreateRole(BaseModel):
    name: str


class RoleResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# ===== REVIEWS =====
class CreateReview(BaseModel):
    user_id: int
    date: str
    score: int
    ai_api_model_id: int


class ReviewResponse(BaseModel):
    id: int
    user_id: int
    date: str
    score: int
    ai_api_model_id: int

    class Config:
        orm_mode = True
