# jcon

## 1. installation
This package is only dependent on standard library of Python3.

`pip install git+https://github.com/AKARI-Inc/jcon.git`

## 2. Usage
For more detail, see [document](https://akari-inc.github.io/jcon/).
### 2.1 コンテクストマネージャで簡単にjsonパスから辞書として読み込み
```Python
from jcon import json_read


json_path = "path/to/hoge.json"
with json_read(json_path) as json_dict:
    ...
```

### 2.2 デコレータを1行追加で任意の関数をjson pathでconfig可能に
```Python
import jcon
json_path = "path/to/hoge.json"


@jcon.configurable        # この一行を追加するだけ。 encoding等を指定する場合は `@jcon.configurable(encoding=hoge)` とする(document参照)。
def hoge(*args, **krags): # 任意の関数
    ...
    
    
hoge(json_path)           # jsonのパスを入力にできる。もちろん，元々の引数もその後に入力できる。
```

### 2.3 クラスを名前で登録(新概念)することが可能になり，jsonから文字列で呼び出すことができる。
jsonの例
```Json
{
    "type": "test",
    "name": "Bob",
    "age": 16,
    "subjects": ["math", "english"]
}
```
json の type 要素から class として呼び出す
```Python
from jcon import Registrable 
json_path = "path/to/hoge.json"


class BaseCls(Registrable):        # 基底クラスは Registrable を継承する。
    def __init__(self):
        raise NotImplementedError
        
@BaseCls.register("test")          # 名前を"登録"
class SubCls(BaseCls):
    def __init__(self, name: str, age: int, subjects: List[str]):
        self.name = name
        self.age = age
        self.subjects = subjects
        

# 基底クラスの from_json メソッドでjson_pathからインスタンスを作成可能に。
instance = BaseCls.from_json(json_path)
```
