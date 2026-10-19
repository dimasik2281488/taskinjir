"""Сохранение и загрузка задач в txt-файл.

Формат строки: ``статус;название`` (1 — выполнена, 0 — в работе).
Файл лежит рядом с модулем, поэтому не зависит от папки запуска (BUG-005).
"""
import os
import sys
from pathlib import Path

DEFAULT_PATH = str(Path(__file__).resolve().parent / "tasks.txt")


def _warn(text: str) -> None:
    print(f"[Предупреждение] {text}", file=sys.stderr)


def load_tasks(path: str = DEFAULT_PATH) -> list[dict]:
    """Загружает задачи. Битые строки пропускаются, битый файл уходит в .bak."""
    collection: list[dict] = []
    skipped = 0
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        return collection
    except UnicodeDecodeError:  # BUG-003
        backup = path + ".bak"
        os.replace(path, backup)
        _warn(f"Файл задач повреждён (не UTF-8). Копия сохранена: {backup}")
        return collection

    for line in lines:
        if not line.strip():
            continue
        status, sep, title = line.partition(";")
        title = title.strip()
        if not sep or status not in ("0", "1") or not title:  # BUG-002
            skipped += 1
            continue
        collection.append({"title": title, "done": status == "1"})
    if skipped:
        _warn(f"Пропущено повреждённых строк в файле: {skipped}")
    return collection


def save_tasks(collection: list[dict], path: str = DEFAULT_PATH) -> None:
    """Сохраняет задачи атомарно: сначала во временный файл, потом замена (BUG-010)."""
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        for task in collection:
            f.write(f"{1 if task['done'] else 0};{task['title']}\n")
    os.replace(tmp_path, path)
