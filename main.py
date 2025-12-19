from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import uvicorn
from pydantic import BaseModel

# === DB ===
from base import Base, engine, get_db
from models.models_ai import AiApi, AiApiModel
from models.models_users import User, Role, Review
from pydantic_models import (
    CreateUser, UserResponse,
    CreateRole, RoleResponse,
    CreateReview, ReviewResponse,
    CreateAiApi, AiApiResponse,
    CreateAiApiModel, AiApiModelResponse,
)

# === SERVICES ===
from services.openAi_service import OpenAiService
from services.groq_service import GroqService


app = FastAPI(title="AI API Gateway", version="1.0")


# ==================================================
# ================= STARTUP ========================
# ==================================================

@app.on_event("startup")
def startup_event():
    app.state.openai_service = OpenAiService()
    app.state.groq_service = GroqService()
    Base.metadata.create_all(bind=engine)
    print("✅ Database created / connected")


# ==================================================
# ================= OPENAI =========================
# ==================================================

class AIRequest(BaseModel):
    query: str
    temperature: float = 0.7
    max_tokens: int = 150


class AIResponse(BaseModel):
    result: str


@app.post("/openai", response_model=AIResponse)
def run_openai(request: AIRequest):
    try:
        service = app.state.openai_service
        result = service.ask(
            prompt=request.query,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return AIResponse(result=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================================================
# ================= GROQ ===========================
# ==================================================

class GroqRequest(BaseModel):
    query: str


class GroqResponse(BaseModel):
    result: str


@app.post("/groq", response_model=GroqResponse)
def run_groq(request: GroqRequest):
    try:
        service = app.state.groq_service
        result = service.ask(request.query)
        return GroqResponse(result=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================================================
# ================= USERS CRUD =====================
# ==================================================

@app.post("/users", response_model=UserResponse)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"status": "deleted"}


# ==================================================

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
