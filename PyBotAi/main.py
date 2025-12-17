from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
DATABASE = "users.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)
        db.commit()

init_db()

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return jsonify({"message": "Заполни все поля"}), 400

    db = get_db()
    cur = db.cursor()

    if cur.execute(
        "SELECT id FROM users WHERE username = ?", (username,)
    ).fetchone():
        return jsonify({"message": "Пользователь уже существует"}), 409

    hashed = generate_password_hash(password)

    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed)
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"message": "Ошибка: Пользователь уже существует (Integrity Error)"}), 409
    
    return '<h1>Регистрация успешна ✅!</h1><p><a href="/">На главную</a></p>'


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return jsonify({"message": "Заполни все поля"}), 400

    db = get_db()
    cur = db.cursor()

    user = cur.execute(
        "SELECT password FROM users WHERE username = ?", (username,)
    ).fetchone()

    if user and check_password_hash(user["password"], password):
        return jsonify({"message": f"Добро пожаловать, {username}!"})
    else:
        return jsonify({"message": "Неверный логин или пароль"}), 401

@app.route("/")
def index():
    return app.send_static_file('index.html')


if __name__ == "__main__":
    app.run(debug=True)

    @app.route("/")
    def index():
        return app.send_static_file('index.html')

@app.route("/register_page") 
def register_page():
    return app.send_static_file('register.html')