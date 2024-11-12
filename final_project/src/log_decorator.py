import random
from functools import wraps
from typing import Any, Callable, Union


def log(template: Union[Callable[[Any], Any], str]) -> Callable[[Any], Any]:
    """Декоратор поддерживает два режима: @log or @log(some_template)"""
    execution_time = random.randint(1, 10)
    if isinstance(template, str):

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                print(template.format(execution_time))
                return result

            return wrapper

        return decorator
    else:

        @wraps(template)
        def wrapper(*args, **kwargs):
            result = template(*args, **kwargs)
            print(f"{template.__name__} - {execution_time}c!")
            return result

        return wrapper
