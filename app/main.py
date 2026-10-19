import json
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI(title="Notes API")

NOTES_FILE = "/home/dissy/1cc/notes.json"


@app.get("/notes")
@app.get("/api/notes")
def get_notes(id_user: Optional[str] = Query(default=None)):
    if id_user is not None:
        try:
            int(id_user)
        except ValueError:
            return JSONResponse(
                status_code=400,
                content={"error": "Параметр id_user должен быть целым числом"},
            )

    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return JSONResponse(status_code=500, content={"error": "Файл с заметками не найден"})
