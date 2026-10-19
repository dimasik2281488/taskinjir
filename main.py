"""Task Manager — консольный менеджер задач.

История улучшений по версиям (подробнее — в BACKLOG.md, баги — в BUGFIX.md):

0.0.1 — каркас приложения: приветствие, ввод названия задачи через input.
0.0.2 — задачи хранятся в списке, добавление новых задач.
0.0.3 — вывод списка задач циклом for с нумерацией.
0.0.4 — главное меню и цикл while, выход из программы.
0.0.5 — обработка пунктов меню через match/case.
0.0.6 — функции edited_task и deleted_task вынесены из цикла,
        вызываются в case "3" и case "4".
0.0.7 — сохранение и загрузка задач из txt-файла, цикл перенесён в main(),
        форматированный вывод списка задач таблицей.
0.0.8 — проверка вводимых данных: номер задачи, пустое название.
0.0.9 — разделение на модули: view (вывод), utils (check_confirm),
        core (создать/изменить/удалить), storage (сохранение/загрузка).
0.1.0 — исправление найденных багов (см. BUGFIX.md): устойчивость к
        неверному вводу и повреждённому файлу, запуск только через
        __main__, путь к файлу не зависит от папки запуска, защита от
        дубликатов и длинных названий, атомарное сохранение, корректный
        выход по Ctrl+C / Ctrl+D, сохранение только при изменениях.
"""
import core
import storage
import view

__version__ = "0.1.0"


def main() -> None:
    collection = storage.load_tasks()
    try:
        while True:
            view.show_menu()
            choice = input("Выбор: ").strip()
            match choice:
                case "1":
                    view.show_tasks(collection)
                case "2":
                    changed = core.create_task(collection)
                case "3":
                    changed = core.edited_task(collection)
                case "4":
                    changed = core.deleted_task(collection)
                case "0":
                    break
                case _:
                    view.show_message("Неизвестная команда.")
                    continue
            if choice in ("2", "3", "4") and changed:
                storage.save_tasks(collection)
    except (EOFError, KeyboardInterrupt):  # BUG-006
        view.show_message("\nВвод прерван.")
    storage.save_tasks(collection)
    view.show_message(f"Задачи сохранены в {storage.DEFAULT_PATH}. До встречи!")


if __name__ == "__main__":  # BUG-004
    main()
