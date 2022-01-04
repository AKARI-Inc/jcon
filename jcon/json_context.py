import json
import contextlib


@contextlib.contextmanager
def json_read(jsonpath: str, *args, **kwargs):
    """Context manager to yield ``dict`` from path in which .json is.

    Args:
        jsonpath (``str``): ``path/to/file.json``

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
