from functools import wraps
from typing import Callable
from .json_context import json_read


def configurable(func: Callable) -> Callable[[str], Callable]:
    """Make your function configurable by ``.json`` path.

    Args:
        func (Callable): Your arbitrary function.

    Returns:
        Callable[[str], Callable]: Wrapped function which is input from ``.json`` path.
    """
    @wraps(func)
    def wrapper(json_path: str, *args, **kwargs):
        with json_read(json_path) as json_dict:
            return func(*args, **kwargs, **json_dict)

    return wrapper


if __name__ == "__main__":
    from typing import List

    @configurable
    def test_func(name: str, age: int, subjects: List[str]) -> None:
        print(f"{name} is {age}-year-old and studying {len(subjects)} subjects.")

    test_func("sample/simple.json")
