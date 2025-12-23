from fastapi import FastAPI, Form, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from pydantic import BaseModel
from datetime import date

from base import Base, engine, get_db
from models.models_users import User, Review
from models.models_ai import AiApi, AiApiModel

# === Сервіси ШІ ===
from services.openAi_service import OpenAiService
from services.groq_service import GroqService
from services.gemini_service import GeminiService

# === FastAPI ===
app = FastAPI(title="PyBotAi")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Статика та шаблони
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# === База ===
Base.metadata.create_all(bind=engine)

# ==================== Startup ====================
@app.on_event("startup")
def startup_event():
    # Ініціалізація ШІ
    app.state.openai_service = OpenAiService()
    app.state.groq_service = GroqService()
    app.state.gemini_service = GeminiService()

    # Ініціалізація AiApi та AiApiModel
    db: Session = next(get_db())
    try:
        if db.query(AiApi).count() == 0:
            openai_api = AiApi(name="OpenAI", url="https://api.openai.com")
            groq_api = AiApi(name="Groq", url="https://api.groq.com")
            gemini_api = AiApi(name="Gemini", url="https://api.gemini.com")
            db.add_all([openai_api, groq_api, gemini_api])
            db.commit()

            # Додаємо моделі
            db.add_all([
                AiApiModel(name="openai", ai_api_id=openai_api.id),
                AiApiModel(name="groq", ai_api_id=groq_api.id),
                AiApiModel(name="gemini", ai_api_id=gemini_api.id)
            ])
            db.commit()
    finally:
        db.close()

# ==================== INDEX ====================
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ==================== REGISTER ====================
@app.post("/register")
def register_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        return JSONResponse(status_code=400, content={"message": "Користувач вже існує"})

    hashed = generate_password_hash(password)
    user = User(username=username, password=hashed, email=f"{username}@test.com", age=18, role_id=1)
    db.add(user)
    db.commit()
    db.refresh(user)
    return JSONResponse({"message": "Користувача створено"})

# ==================== LOGIN ====================
@app.post("/login")
def login_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not check_password_hash(user.password, password):
        return JSONResponse(status_code=400, content={"detail": "Неправильний логін або пароль"})
    return JSONResponse({"message": "Вхід успішний", "username": username})

# ==================== CRUD USERS ====================
@app.post("/users")
def create_user_crud(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
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
    users = db.query(User).all()
    return [{"id": u.id, "username": u.username} for u in users]

@app.get("/users/{user_id}")
def get_user_crud(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    return {"id": user.id, "username": user.username}

@app.put("/users/{user_id}")
def update_user_crud(user_id: int, password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    user.password = generate_password_hash(password)
    db.commit()
    return {"message": "Пароль оновлено"}

@app.delete("/users/{user_id}")
def delete_user_crud(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    db.delete(user)
    db.commit()
    return {"message": "Користувача видалено"}

# ==================== CHAT ====================
class AIRequest(BaseModel):
    query: str
    service: str
    temperature: float = 0.7
    max_tokens: int = 150

class AIResponse(BaseModel):
    result: str

@app.post("/send_message", response_model=AIResponse)
def send_message_ai(request: AIRequest):
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
    service: str   # openai / groq / gemini
    score: int     # 1-5

@app.post("/review")
def add_review(data: ReviewRequest, db: Session = Depends(get_db)):
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
