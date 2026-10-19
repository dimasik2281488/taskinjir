"""Сохранение и загрузка задач."""
import json
import os

DEFAULT_PATH = "tasks.json"


def load_tasks(path: str = DEFAULT_PATH) -> list[dict]:
    """Загружает задачи из JSON-файла. Если файла нет или он повреждён — пустой список."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
    return data if isinstance(data, list) else []


def save_tasks(tasks: list[dict], path: str = DEFAULT_PATH) -> None:
    """Сохраняет задачи в JSON-файл."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)
