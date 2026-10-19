"""Методы показа информации в консоль."""

MENU = (
    "\n=== Task Manager ===\n"
    "1. Показать задачи\n"
    "2. Создать задачу\n"
    "3. Редактировать задачу\n"
    "4. Удалить задачу\n"
    "0. Выход"
)


def show_menu() -> None:
    print(MENU)


def show_message(text: str) -> None:
    print(text)


def show_task(task: dict) -> None:
    status = "✔" if task.get("done") else "✘"
    print(f"[{task['id']}] {status} {task['title']}")


def show_tasks(tasks: list[dict]) -> None:
    if not tasks:
        print("Список задач пуст.")
        return
    print("\nСписок задач:")
    for task in tasks:
        show_task(task)
