"""Основные механики: создать, изменить, удалить.

Каждая функция возвращает True, если коллекция изменилась (чтобы main
сохранял файл только при реальных изменениях).
"""
import view
from utils import check_confirm

MAX_TITLE_LEN = 100


def _ask_index(collection: list[dict]) -> int | None:
    """Запрашивает номер задачи, возвращает индекс в списке или None."""
    raw = input("Введите номер задачи: ").strip()
    try:  # BUG-001: isdigit() пропускает символы вроде «²», а int() на них падает
        number = int(raw)
    except ValueError:
        view.show_message("Введите номер цифрами.")
        return None
    if not 1 <= number <= len(collection):
        view.show_message("Задачи с таким номером нет.")
        return None
    return number - 1


def _is_duplicate(collection: list[dict], title: str, skip: int | None = None) -> bool:
    """Есть ли уже задача с таким названием (без учёта регистра)."""
    low = title.casefold()
    return any(i != skip and t["title"].casefold() == low for i, t in enumerate(collection))


def _validate_title(collection: list[dict], title: str, skip: int | None = None) -> bool:
    if len(title) > MAX_TITLE_LEN:
        view.show_message(f"Название слишком длинное (максимум {MAX_TITLE_LEN} символов).")
        return False
    if _is_duplicate(collection, title, skip):  # BUG-008
        view.show_message("Такая задача уже есть.")
        return False
    return True


def create_task(collection: list[dict]) -> bool:
    title = input("Название задачи: ").strip()
    if not title:
        view.show_message("Название не может быть пустым.")
        return False
    if not _validate_title(collection, title):
        return False
    collection.append({"title": title, "done": False})
    view.show_message("Задача добавлена.")
    return True


def edited_task(collection: list[dict]) -> bool:
    """Изменяет задачу."""
    view.show_tasks(collection)
    if not collection:
        return False
    index = _ask_index(collection)
    if index is None:
        return False
    task = collection[index]
    changed = False

    new_title = input(f"Новое название [{task['title']}]: ").strip()
    if new_title and new_title != task["title"]:
        if not _validate_title(collection, new_title, skip=index):
            return False
        task["title"] = new_title
        changed = True

    answer = input("Выполнена? (y/n, Enter — без изменений): ").strip().lower()
    if answer in ("y", "д", "да"):
        changed = changed or not task["done"]
        task["done"] = True
    elif answer in ("n", "н", "нет"):
        changed = changed or task["done"]
        task["done"] = False
    elif answer:  # BUG-009
        view.show_message("Статус не распознан, оставлен прежним.")

    view.show_message("Задача изменена." if changed else "Изменений нет.")
    return changed


def deleted_task(collection: list[dict]) -> bool:
    """Удаляет задачу (с подтверждением)."""
    view.show_tasks(collection)
    if not collection:
        return False
    index = _ask_index(collection)
    if index is None:
        return False
    title = collection[index]["title"]
    if check_confirm(f"Удалить задачу «{title}»?"):
        collection.pop(index)
        view.show_message(f"Задача «{title}» удалена.")
        return True
    view.show_message("Удаление отменено.")
    return False
