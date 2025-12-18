import sqlite3
import os
from ai_logic import AIHandleService 
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash


# 1. Ініціалізація Flask з пошуком файлів у поточній директорії
app = Flask(__name__, template_folder=".", static_folder=".")

DATABASE = "user.db" # База даних з твого скріншоту

# 2. Ініціалізація сервісу ШІ (Abstraction layer)
ai_service = AIHandleService()

# 3. Робота з базою даних
def init_db():
    """Створює таблицю користувачів при старті програми"""
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                username TEXT UNIQUE, 
                password TEXT
            )
        """)
    print("База даних перевірена/створена.")

init_db()

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# 4. Основні маршрути для HTML сторінок
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register_page")
def register_page():
    return render_template("register.html")

# 5. Маршрут для статики (CSS, JS, зображення)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(".", filename)

# 6. Логіка реєстрації
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    
    if not username or not password:
        return "Заповніть усі поля", 400
        
    hashed_pw = generate_password_hash(password)
    try:
        with get_db() as db:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
            db.commit()
        return "Реєстрація успішна ✅"
    except sqlite3.IntegrityError:
        return "Такий користувач вже існує", 409

# 7. Логіка авторизації
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    with get_db() as db:
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    
    if user and check_password_hash(user["password"], password):
        return jsonify({"message": f"Вітаю, {username}!"})
    
    return jsonify({"message": "Невірний логін або пароль"}), 401

# 8. Логіка відправки повідомлення ШІ
@app.route("/send_message", methods=["POST"])
def send_message():
    message = request.form.get("message")
    
    if not message:
        return jsonify({"status": "error", "message": "Повідомлення порожнє"}), 400

    # Використовуємо абстракцію сервісу (AIHandleService)
    answer = ai_service.process_message(message)
    
    return jsonify({
        "status": "success", 
        "response": answer
    })

# 9. Запуск на порту 1488
if __name__ == "__main__":
    app.run(debug=True, port=1488)