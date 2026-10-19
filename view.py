"""Методы показа информации в консоль."""

MAX_TITLE_VIEW = 40  # длиннее — обрезаем в таблице (BUG-007)

MENU = (
    "\n=== Task Manager ===\n"
    "1 - Показать задачи\n"
    "2 - Добавить задачу\n"
    "3 - Изменить задачу\n"
    "4 - Удалить задачу\n"
    "0 - Выход"
)


def show_menu() -> None:
    print(MENU)


def show_message(text: str) -> None:
    print(text)


def _short(title: str) -> str:
    if len(title) <= MAX_TITLE_VIEW:
        return title
    return title[: MAX_TITLE_VIEW - 1] + "…"


def show_tasks(collection: list[dict]) -> None:
    """Выводит список задач таблицей."""
    if not collection:
        print("Список задач пуст.")
        return
    titles = [_short(t["title"]) for t in collection]
    width = max(max(len(t) for t in titles), len("Название"))
    line = "-" * (width + 20)
    print(line)
    print(f"{'№':<4}{'Название':<{width}}  Статус")
    print(line)
    for i, (task, title) in enumerate(zip(collection, titles), start=1):
        status = "выполнена" if task["done"] else "в работе"
        print(f"{i:<4}{title:<{width}}  {status}")
    print(line)
