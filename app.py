from fastapi import FastAPI
from openai import OpenAI
import uvicorn
from base import SessionLocal, get_db, Base, engine

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

app = FastAPI()

client = OpenAI()

#===НАЛАШТУВАННЯ DOTENV===
dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = [os.getenv("JWT_ALGORITHM", "HS512")]

if not OPENAI_API_KEY:
    raise ValueError("JWT_SECRET_KEY не встановлений")


#===ЗАПИТИ ДО ШТУЧНОГО ІНТЕЛЕКТУ===
#//////////////
#===CHAT GPT===
#\\\\\\\\\\\\\\
def response_to_chatgpt(user_input: str, temperature: float, max_tokens: int):
    """
        Отправляет запрос на генерацию текста модели GPT-4.1.

        :param user_input: Запрос пользователя (содержимое чата).
        :param temperature: Уровень креативности (от 0.0 до 2.0).
        :param max_tokens: Максимальное количество токенов в ответе.
        :return: Сгенерированный текст.
        """
    messages_payload = [
        {"role": "user", "content": user_input}
        ]
    try:
        response = client.responses.create(
            model="GPT-4.1",
            messages=messages_payload,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.output_text
    except Exception as e:
        print(f"Помилка під час виклику API: {e}")
        return "Відбулася помилка при отриманні відповіді"


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
