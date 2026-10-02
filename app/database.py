import sqlite3
from datetime import date
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "notes.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    conn = get_connection()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                login TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                id_user INTEGER NOT NULL REFERENCES users(id),
                created_at TEXT NOT NULL
            );
            """
        )
        conn.commit()
    finally:
        conn.close()


def seed_db() -> None:
    conn = get_connection()
    try:
        cur = conn.execute("SELECT COUNT(*) FROM notes")
        if cur.fetchone()[0] > 0:
            return

        conn.executemany(
            "INSERT INTO users (id, login) VALUES (?, ?)",
            [
                (1, "user25"),
                (2, "user42"),
                (3, "admin01"),
            ],
        )
        conn.executemany(
            "INSERT INTO notes (id, title, content, id_user, created_at) VALUES (?, ?, ?, ?, ?)",
            [
                (1, "Конференция ИТ", "Обсуждение планов на 2027 год", 1, "2027-03-15"),
                (2, "Совещание по проекту", "Статус разработки API", 2, "2027-04-02"),
                (3, "Ревью кода", "Замечания по модулю интеграции", 3, "2027-04-10"),
                (4, "Планёрка", "Еженедельный синк команды", 1, "2027-04-18"),
                (5, "Релиз v1.0", "Выпуск первой версии продукта", 2, "2027-05-01"),
            ],
        )
        conn.commit()
    finally:
        conn.close()
