from fastapi import FastAPI, HTTPException
from openai import OpenAI
import uvicorn
from pydantic import BaseModel
from base import SessionLocal, get_db, Base, engine
from typing import List, Dict, Optional

import os
import dotenv

from pydantic_models import (
    CreateUser, UserResponse,
    CreateRole, RoleResponse,
    CreateReview, ReviewResponse,
    CreateAiApi, AiApiResponse,
    CreateAiApiModel, AiApiModelResponse,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI API Gateway", version="1.0")


#===НАЛАШТУВАННЯ DOTENV===
dotenv.load_dotenv()

OPENAI_API_KEY_VALUE = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY_VALUE:
    raise ValueError("OPENAI_API_KEY не встановлений у .env")

client = OpenAI(api_key=OPENAI_API_KEY_VALUE)


#===ЗАПИТИ ДО ШТУЧНОГО ІНТЕЛЕКТУ===
class AIRequest(BaseModel):
    query: str
    temperature: float = 0.7
    max_tokens: int = 150


class AIResponse(BaseModel):
    result: str


#===CHAT GPT===
def response_to_chatgpt(user_input: str, temperature: float, max_tokens: int) -> str:
    messages_payload: List[Dict[str, str]] = [
        {"role": "user", "content": user_input}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_payload,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Помилка під час виклику API: {e}")
        raise HTTPException(status_code=500, detail=f"Помилка OpenAI API: {str(e)}")


@app.post("/openai", response_model=AIResponse)
def run_openai(request: AIRequest):
    try:
        result = response_to_chatgpt(
            user_input=request.query,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        return AIResponse(result=result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Невідома помилка: {str(e)}")


#===CRUD ДЛЯ USERS===
def create_user(db: SessionLocal, user: CreateUser):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: SessionLocal, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: SessionLocal, user_id: int, new_data: CreateUser):
    user = get_user(db, user_id)
    if not user:
        return None
    for key, value in user.dict().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_author(db: SessionLocal, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True


if __name__ == "__main__":
    uvicorn.run(app)
