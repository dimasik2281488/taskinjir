"""Точка входа Task Manager (версия 1.0)."""
import core
import storage
import view

__version__ = "1.0.0"


def main() -> None:
    tasks = storage.load_tasks()
    actions = {
        "1": lambda: view.show_tasks(tasks),
        "2": lambda: core.create_task(tasks),
        "3": lambda: core.edit_task(tasks),
        "4": lambda: core.delete_task(tasks),
    }
    while True:
        view.show_menu()
        choice = input("Выбор: ").strip()
        if choice == "0":
            storage.save_tasks(tasks)
            view.show_message("Задачи сохранены. До встречи!")
            break
        action = actions.get(choice)
        if action is None:
            view.show_message("Неизвестная команда.")
            continue
        action()
        storage.save_tasks(tasks)


if __name__ == "__main__":
    main()
