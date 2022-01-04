from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import OpenTextMode

from .json_context import json_read
from functools import wraps
from typing import Optional, Callable


def configurable(
    _func: Optional[Callable] = None,
    mode: Optional[OpenTextMode] = 'r',
    buffering: Optional[int] = -1,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    newline: Optional[str] = None,
    closefd: Optional[bool] = True,
    opener: Optional[Callable] = None,
):
    """Make your function configurable by ``.json`` path.

    Args:
        func (Callable): Your arbitrary function.
        mode (Optional[OpenTextMode], optional): An argument same as `open` in stdlib. Defaults to 'r'.
        buffering (Optional[int], optional): An argument same as `open` in stdlib. Defaults to -1.
        encoding (Optional[str], optional): An argument same as `open` in stdlib. Defaults to None.
        errors (Optional[str], optional): An argument same as `open` in stdlib. Defaults to None.
        newline (Optional[str], optional): An argument same as `open` in stdlib. Defaults to None.
        closefd (Optional[bool], optional): An argument same as `open` in stdlib. Defaults to True.
        opener (Optional[Callable], optional): An argument same as `open` in stdlib. Defaults to None.

    Returns:
        Callable[[str], Callable]: Wrapped function which is input from ``.json`` path.
    """

    if _func is None:
        def _configurable(func: Callable) -> Callable[[str], Callable]:
            @wraps(func)
            def wrapper(
                json_path: str,
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

        return _configurable
    else:
        # avoid mypy error ( mypy says "None" not callable nonetheless this else scope ensure func is not None. )
        func = _func

        @wraps(func)
        def wrapper(
            json_path: str,
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
