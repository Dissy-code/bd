import json  # Библиотека для работы с JSON-файлами (чтение и запись)
from typing import Optional  # Нужен, чтобы указать, что параметр может быть равен None
from fastapi import FastAPI, Query  # FastAPI для создания API, а Query — для настройки параметров запроса
from fastapi.responses import JSONResponse  # Специальный класс, чтобы красиво возвращать JSON-ответы с кодами ошибок

# Создаем само приложение FastAPI и даем ему понятное название
app = FastAPI(title="Notes API")

# Путь к файлу, в котором физически лежат наши заметки на сервере
NOTES_FILE = "/home/dissy/1cc/notes.json"


# Прописываем сразу два адреса (эндпоинта), по которым можно будет получить заметки
@app.get("/notes")
@app.get("/api/notes")
def get_notes(id_user: Optional[str] = Query(default=None)):
    """Функция, которая срабатывает при GET-запросе и возвращает список заметок."""

    # Проверяем: если пользователь вообще передал в запросе id_user...
    if id_user is not None:
        try:
            # ...пытаемся превратить его из строки в целое число
            int(id_user)
        except ValueError:
            # Если не получилось (например, передали буквы "abc"), отдаем ошибку 400 (Плохой запрос)
            return JSONResponse(
                status_code=400,
                content={"error": "Параметр id_user должен быть целым числом"},
            )

    try:
        # Пытаемся открыть наш файл с заметками в режиме чтения ("r") и с правильной кодировкой текста
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            # Читаем JSON-данные из файла и сразу же отдаем их пользователю
            return json.load(f)
    except FileNotFoundError:
        # Если файла физически нет по указанному пути, отдаем ошибку сервера 500
        return JSONResponse(
            status_code=500, content={"error": "Файл с заметками не найден"}
        )
