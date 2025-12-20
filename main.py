from fastapi import FastAPI, Form, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from pydantic import BaseModel

from base import Base, engine, get_db
from models.models_users import User

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

# === Startup: ініціалізація ШІ ===
@app.on_event("startup")
def startup_event():
    app.state.openai_service = OpenAiService()
    app.state.groq_service = GroqService()
    app.state.gemini_service = GeminiService()


# ================= INDEX =================
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ================= REGISTER =================
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


# ================= LOGIN =================
@app.post("/login")
def login_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not check_password_hash(user.password, password):
        return JSONResponse(status_code=400, content={"detail": "Неправильний логін або пароль"})
    return JSONResponse({"message": "Вхід успішний", "username": username})


# ================= CRUD USERS =================
# CREATE
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

# READ ALL
@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "username": u.username} for u in users]

# READ ONE
@app.get("/users/{user_id}")
def get_user_crud(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    return {"id": user.id, "username": user.username}

# UPDATE
@app.put("/users/{user_id}")
def update_user_crud(user_id: int, password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    user.password = generate_password_hash(password)
    db.commit()
    return {"message": "Пароль оновлено"}

# DELETE
@app.delete("/users/{user_id}")
def delete_user_crud(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    db.delete(user)
    db.commit()
    return {"message": "Користувача видалено"}


# ================= CHAT (OpenAI / Groq / Gemini) =================
class AIRequest(BaseModel):
    query: str
    service: str  # openai / groq / gemini
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

