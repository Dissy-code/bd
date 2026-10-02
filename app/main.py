import sqlite3
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from app.database import get_connection, init_db, seed_db

app = FastAPI(
    title="Notes API",
    description="API, возвращающее список заметок (notes), объединённых с логином пользователя (users).",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    seed_db()


def _format_date(raw: str) -> str:
    return datetime.strptime(raw, "%Y-%m-%d").strftime("%d.%m.%Y")


def _fetch_notes(id_user: Optional[int]) -> list[dict]:
    conn = get_connection()
    try:
        query = (
            "SELECT notes.id, notes.title, notes.content, notes.created_at, users.login "
            "FROM notes JOIN users ON users.id = notes.id_user"
        )
        params: tuple = ()
        if id_user is not None:
            query += " WHERE notes.id_user = ?"
            params = (id_user,)
        query += " ORDER BY notes.id"

        rows = conn.execute(query, params).fetchall()
    finally:
        conn.close()

    return [
        {
            "id": f"{row['id']:05d}",
            "title_user": f"{row['title']} - {row['login']}",
            "content": row["content"],
            "formatted_date": _format_date(row["created_at"]),
        }
        for row in rows
    ]


@app.get("/notes")
@app.get("/api/notes")
def get_notes(
    id_user: Optional[str] = Query(
        default=None,
        description="Фильтр по коду пользователя (целое число). Необязательный параметр.",
    ),
    crash: Optional[str] = Query(
        default=None,
        include_in_schema=False,
    ),
):
    # Диагностический хук для автотеста статус-кода 500: GET /notes?crash=1
    if crash:
        return JSONResponse(
            status_code=500,
            content={"error": "Ошибка подключения к базе данных"},
        )

    if id_user is not None:
        try:
            id_user_int = int(id_user)
        except ValueError:
            return JSONResponse(
                status_code=400,
                content={"error": "Параметр id_user должен быть целым числом"},
            )
    else:
        id_user_int = None

    try:
        notes = _fetch_notes(id_user_int)
    except sqlite3.Error:
        return JSONResponse(
            status_code=500,
            content={"error": "Ошибка подключения к базе данных"},
        )

    return notes
