import pytest

import jcon
from typing import List


def test_configurable():
    """test function for ``configurable`` in ``jcon/func_decoretor.py``"""
    @jcon.configurable
    def func1(name: str, age: int, subjects: List[str]) -> None:
        print(f"{name} is {age}-year-old and studying {len(subjects)} subjects.")

    @jcon.configurable
    def func2(name: str, age: int, food: str) -> None:
        print(f"{name} is {age}-year-old and eating {food}.")

    @jcon.configurable
    def func3(name: str, age: int, food: str = "Apple", **kwargs) -> None:
        print(f"{name} is {age}-year-old and eating {food}.")

    json_path = "sample/simple.json"
    assert func1(json_path) is None
    with pytest.raises(TypeError):
        func2(json_path, name="Jason", food="Apple")
    assert func3(json_path, food="Banana") is None
    assert func3(json_path, **{"food": "Chocolate"}) is None
