from functools import wraps
from typing import Any, Callable, Optional


def _write_log(message: str, filename: Optional[str]) -> None:
    """
    Записывает сообщение в файл или выводит в консоль.

    :param message: Текст сообщения для логирования.
    :param filename: Имя файла для записи. Если None, вывод идет в консоль.
    """
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функций.

    Логирует имя функции, результат при успехе или тип ошибки и входные данные при сбое.

    :param filename: Имя файла для записи логов. Если не указано, логи выводятся в консоль.
    :return: Обернутая функция.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                msg = f"{func.__name__} ok"
                _write_log(msg, filename)
                return result
            except Exception as e:
                # Формируем сообщение об ошибке с типом исключения и аргументами
                msg = (
                    f"{func.__name__} error: {type(e).__name__}. "
                    f"Inputs: {args}, {kwargs}"
                )
                _write_log(msg, filename)
                # Пробрасываем исключение дальше, чтобы поведение функции не менялось
                raise

        return wrapper

    return decorator
