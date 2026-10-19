"""Вспомогательные функции."""


def check_confirm(message: str = "Вы уверены?") -> bool:
    """Запрашивает подтверждение у пользователя. True — если ответ да (y/д/yes/да)."""
    answer = input(f"{message} (y/n): ").strip().lower()
    return answer in ("y", "yes", "д", "да")
