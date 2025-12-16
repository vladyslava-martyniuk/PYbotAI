from pydantic import BaseModel


#===USERS===
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
    date_of_birth: str
    role_id: int
    session: str
    is_baned: bool

    class Config:
        orm_mode = True


#===ROLES===
class CreateRole(BaseModel):
    name: str


class RoleResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


#===REVIEWS===
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


#===AI APIS===
class CreateAiApi(BaseModel):
    name: str
    url: str


class AiApiResponse(BaseModel):
    id: int
    name: str
    url: str

    class Config:
        orm_mode = True


#===AI API MODELS===
class CreateAiApiModel(BaseModel):
    ai_api_id: int
    name: str


class AiApiModelResponse(BaseModel):
    id: int
    ai_api_id: int
    name: str

    class Config:
        orm_mode = True



