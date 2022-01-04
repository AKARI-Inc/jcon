# test for github actions
import json
import contextlib


@contextlib.contextmanager
def json_read(jsonpath: str, *args, **kwargs):
    """Context manager to yield ``dict`` from path in which .json is.

    Args:
        jsonpath (``str``): ``path/to/file.json``
        mode (Optional[OpenTextMode], optional): An argument same as `open` in stdlib. Defaults to 'r'.
        buffering (Optional[int], optional): An argument same as `open` in stdlib. Defaults to -1.
        encoding (Optional[str], optional): An argument same as `open` in stdlib. Defaults to None.
        errors (Optional[str], optional): An argument same as `open` in stdlib. Defaults to None.
        newline (Optional[str], optional): An argument same as `open` in stdlib. Defaults to None.
        closefd (Optional[bool], optional): An argument same as `open` in stdlib. Defaults to True.
        opener (Optional[Callable], optional): An argument same as `open` in stdlib. Defaults to None.

    Yields:
        ``dict``: return ``dict`` read from ``jsonpath``
    """
    json_file = open(jsonpath, *args, **kwargs)
    try:
        yield json.load(json_file)
    finally:
        json_file.close()


if __name__ == "__main__":
    with json_read("sample/simple.json") as json_dict:
        print(json_dict)
