from pydantic import BaseModel

# ===== AI APIS =====
class CreateAiApi(BaseModel):
    name: str
    url: str


class AiApiResponse(BaseModel):
    id: int
    name: str
    url: str

    class Config:
        orm_mode = True

# ===== AI API MODELS =====
class CreateAiApiModel(BaseModel):
    ai_api_id: int
    name: str


class AiApiModelResponse(BaseModel):
    id: int
    ai_api_id: int
    name: str

    class Config:
        orm_mode = True