import hashlib
import os
import time

import pymysql
from flask import Flask, jsonify, request

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "database")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "login_db")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "student")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "DockerLab123!")


def password_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def connect_db():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        connect_timeout=3,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def initialize_database():
    last_error = None
    for attempt in range(30):
        try:
            connection = connect_db()
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            username VARCHAR(100) NOT NULL UNIQUE,
                            password_hash CHAR(64) NOT NULL
                        )
                    """)
                    cursor.execute(
                        "INSERT IGNORE INTO users (username, password_hash) VALUES (%s, %s)",
                        (ADMIN_USERNAME, password_hash(ADMIN_PASSWORD)),
                    )
            print("Database is ready; demo user is ensured.")
            return
        except Exception as exc:
            last_error = exc
            print(f"Waiting for database ({attempt + 1}/30): {exc}")
            time.sleep(2)
    raise RuntimeError(f"Could not initialize database: {last_error}")


@app.get("/api/health")
def health():
    try:
        connection = connect_db()
        connection.close()
        return jsonify(status="ok", database="connected")
    except Exception:
        return jsonify(status="error", database="unavailable"), 503


@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))

    if not username or not password:
        return jsonify(success=False, message="Veuillez saisir un identifiant et un mot de passe."), 400

    try:
        connection = connect_db()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT password_hash FROM users WHERE username = %s",
                    (username,),
                )
                user = cursor.fetchone()
    except Exception:
        app.logger.exception("Database query failed")
        return jsonify(success=False, message="Le service est temporairement indisponible."), 503

    if user and user["password_hash"] == password_hash(password):
        return jsonify(
            success=True,
            message="Congratulations ! Vous avez réussi à déployer les trois conteneurs Docker."
        )

    return jsonify(success=False, message="Identifiants incorrects."), 401


if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000)
