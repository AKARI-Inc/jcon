from typing import List

from jcon import Registrable, json_read

PATH = "sample/registration.json"


def test_registrable():

    class BaseCls(Registrable):
        def __init__(self):
            raise NotImplementedError

    @BaseCls.register("test")
    class SubCls(BaseCls):
        def __init__(self, name: str, age: int, subjects: List[str]):
            self.name = name
            self.age = age
            self.subjects = subjects

    with json_read(PATH) as json_dict:
        instance = BaseCls.from_json(PATH)
        assert isinstance(instance, SubCls)
        assert json_dict['name'] == instance.name
        assert json_dict['age'] == instance.age
        assert json_dict['subjects'] == instance.subjects

        instance = BaseCls.from_dict(json_dict)
        assert json_dict['name'] == instance.name
        assert json_dict['age'] == instance.age
        assert json_dict['subjects'] == instance.subjects
        assert 'type' in json_dict.keys()


def test_registrable_argument():
    class BaseCls(Registrable):
        def __init__(self):
            raise NotImplementedError

    @BaseCls.register("test")
    class SubCls(BaseCls):
        def __init__(self, name: str, age: int, subjects: List[str]):
            self.name = name
            self.age = age
            self.subjects = subjects

    with json_read(PATH, encoding="utf-8") as json_dict:
        instance = BaseCls.from_json(PATH)
    assert isinstance(instance, SubCls)
    assert json_dict['name'] == instance.name
    assert json_dict['age'] == instance.age
    assert json_dict['subjects'] == instance.subjects
