from functools import wraps
from typing import Any, Callable


def log(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Вызов функции: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Функция {func.__name__} завершилась")
        return result

    return wrapper
