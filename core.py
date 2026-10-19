"""Основные механики: создать, редактировать, удалить."""
import view
from utils import check_confirm


def _find_task(tasks: list[dict], task_id: int) -> dict | None:
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def _ask_id() -> int | None:
    raw = input("Введите id задачи: ").strip()
    if not raw.isdigit():
        view.show_message("Некорректный id.")
        return None
    return int(raw)


def create_task(tasks: list[dict]) -> None:
    title = input("Название задачи: ").strip()
    if not title:
        view.show_message("Название не может быть пустым.")
        return
    new_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({"id": new_id, "title": title, "done": False})
    view.show_message(f"Задача #{new_id} создана.")


def edit_task(tasks: list[dict]) -> None:
    task_id = _ask_id()
    if task_id is None:
        return
    task = _find_task(tasks, task_id)
    if task is None:
        view.show_message("Задача не найдена.")
        return
    new_title = input(f"Новое название [{task['title']}]: ").strip()
    if new_title:
        task["title"] = new_title
    done = input("Выполнена? (y/n, Enter — без изменений): ").strip().lower()
    if done in ("y", "да", "д"):
        task["done"] = True
    elif done in ("n", "нет", "н"):
        task["done"] = False
    view.show_message("Задача обновлена.")


def delete_task(tasks: list[dict]) -> None:
    task_id = _ask_id()
    if task_id is None:
        return
    task = _find_task(tasks, task_id)
    if task is None:
        view.show_message("Задача не найдена.")
        return
    if check_confirm(f"Удалить задачу «{task['title']}»?"):
        tasks.remove(task)
        view.show_message("Задача удалена.")
    else:
        view.show_message("Удаление отменено.")
