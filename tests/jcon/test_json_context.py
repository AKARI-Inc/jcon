from jcon import json_read


def test_json_read():
    with json_read("sample/simple.json") as json_dict:
        assert json_dict["name"] == "Bob"
        assert json_dict["age"] == 16
        assert json_dict["subjects"][0] == "math"
        assert json_dict["subjects"][1] == "english"
