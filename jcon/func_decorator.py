from _typeshed import OpenTextMode
from .json_context import json_read
from functools import wraps
from typing import Optional, Callable


def configurable(func: Callable) -> Callable[[str], Callable]:
    """Make your function configurable by ``.json`` path.

    Args:
        func (Callable): Your arbitrary function.

    Returns:
        Callable[[str], Callable]: Wrapped function which is input from ``.json`` path.
    """
    @wraps(func)
    def wrapper(
        json_path: str,
        mode: Optional[OpenTextMode] = 'r',
        buffering: Optional[int] = -1,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        newline: Optional[str] = None,
        closefd: Optional[bool] = True,
        opener: Optional[Callable] = None,
        *args,
        **kwargs
    ):
        with json_read(
            json_path,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            closefd=closefd,
            opener=opener,
        ) as json_dict:
            return func(*args, **kwargs, **json_dict)

    return wrapper


if __name__ == "__main__":
    from typing import List

    @configurable
    def test_func(name: str, age: int, subjects: List[str]) -> None:
        print(f"{name} is {age}-year-old and studying {len(subjects)} subjects.")

    test_func("sample/simple.json")
