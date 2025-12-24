from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from pydantic import BaseModel
from utils.auth_utils import create_token
from services.openAi_service import OpenAiService
from services.groq_service import GroqService
from services.gemini_service import GeminiService
from base import Base, engine, get_db
from models.models_users import User
from dotenv import load_dotenv

load_dotenv()

# === FastAPI setup ===
app = FastAPI(title="PyBotAi")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
Base.metadata.create_all(bind=engine)

COOKIE_NAME = "access_token"
@app.on_event("startup")
def startup():
    app.state.openai_service = OpenAiService()
    app.state.groq_service = GroqService()
    app.state.gemini_service = GeminiService()
# ==================== MODELS ====================
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str
    age: int = 18

# ==================== INDEX ====================
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ==================== REGISTER ====================
@app.post("/register")
def register_user(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        return JSONResponse(status_code=400, content={"message": "Користувач вже існує"})
    hashed = generate_password_hash(data.password)
    user = User(
        username=data.username,
        password=hashed,
        email=data.email,
        age=data.age,
        role_id=1
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_token(user.username)
    response = JSONResponse({"message": f"Користувача {data.username} створено"})
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        secure=False
    )
    return response

# ==================== LOGIN ====================
@app.post("/login")
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not check_password_hash(user.password, data.password):
        raise HTTPException(status_code=401, detail="Неправильний логін або пароль")
    token = create_token(user.username)
    response = JSONResponse({"message": f"Вхід успішний, {data.username}"})
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        secure=False
    )
    return response

# ==================== LOGOUT ====================
@app.get("/logout")
def logout():
    response = JSONResponse({"message": "Вихід виконано"})
    response.delete_cookie(COOKIE_NAME)
    return response


# ==================== CRUD USERS ====================
@app.post("/users")
def create_user_crud(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """
    Створення користувача через CRUD API.

    Args:
        username (str): Ім'я користувача
        password (str): Пароль
        db (Session): Сесія бази даних

    Returns:
        dict: ID та ім'я користувача або повідомлення про помилку
    """
    if db.query(User).filter(User.username == username).first():
        return JSONResponse(status_code=400, content={"message": "Користувач вже існує"})
    hashed = generate_password_hash(password)
    user = User(username=username, password=hashed, email=f"{username}@test.com", age=18, role_id=1)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}

@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    """
    Отримати список всіх користувачів.

    Args:
        db (Session): Сесія бази даних

    Returns:
        list[dict]: Список користувачів з ID та username
    """
    users = db.query(User).all()
    return [{"id": u.id, "username": u.username} for u in users]

@app.get("/users/{user_id}")
def get_user_crud(user_id: int, db: Session = Depends(get_db)):
    """
    Отримати користувача за ID.

    Args:
        user_id (int): ID користувача
        db (Session): Сесія бази даних

    Returns:
        dict: Інформація про користувача або HTTPException
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    return {"id": user.id, "username": user.username}

@app.put("/users/{user_id}")
def update_user_crud(user_id: int, password: str = Form(...), db: Session = Depends(get_db)):
    """
    Оновити пароль користувача.

    Args:
        user_id (int): ID користувача
        password (str): Новий пароль
        db (Session): Сесія бази даних

    Returns:
        dict: Повідомлення про успішне оновлення
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    user.password = generate_password_hash(password)
    db.commit()
    return {"message": "Пароль оновлено"}

@app.delete("/users/{user_id}")
def delete_user_crud(user_id: int, db: Session = Depends(get_db)):
    """
    Видалити користувача за ID.

    Args:
        user_id (int): ID користувача
        db (Session): Сесія бази даних

    Returns:
        dict: Повідомлення про видалення користувача
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    db.delete(user)
    db.commit()
    return {"message": "Користувача видалено"}

# ==================== CHAT ====================
class AIRequest(BaseModel):
    """Запит для AI-сервісів"""
    query: str
    service: str
    temperature: float = 0.7
    max_tokens: int = 150

class AIResponse(BaseModel):
    """Відповідь від AI-сервісів"""
    result: str

@app.post("/send_message", response_model=AIResponse)
def send_message_ai(request: AIRequest):
    """
    Надіслати повідомлення до обраного AI-сервісу.

    Args:
        request (AIRequest): Параметри запиту (query, service, temperature, max_tokens)

    Returns:
        AIResponse: Результат відповіді від сервісу
    """
    service_map = {
        "openai": app.state.openai_service,
        "groq": app.state.groq_service,
        "gemini": app.state.gemini_service
    }
    service = service_map.get(request.service.lower())
    if not service:
        return AIResponse(result="Невідомий сервіс")
    result = service.ask(request.query)
    return AIResponse(result=f"PyBotAi [{request.service.upper()}]: {result}")

# ==================== REVIEW ====================
class ReviewRequest(BaseModel):
    """Запит на додавання відгуку для AI-сервісу"""
    service: str   # openai / groq / gemini
    score: int     # 1-5

@app.post("/review")
def add_review(data: ReviewRequest, db: Session = Depends(get_db)):
    """
    Додати відгук користувача для конкретного AI-сервісу.

    Args:
        data (ReviewRequest): Дані відгуку (service, score)
        db (Session): Сесія бази даних

    Returns:
        dict: {"status": "ok"} або {"status": "ignored"}
    """
    ai_model = db.query(AiApiModel).filter(AiApiModel.name == data.service.lower()).first()
    if not ai_model:
        return {"status": "ignored"}
    review = Review(user_id=1, ai_api_model_id=ai_model.id, date=date.today(), score=data.score)
    db.add(review)
    db.commit()
    return {"status": "ok"}

# ==================== RUN ====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
