# Python 类型注解与 Pydantic 教程

总的原则，python支持类型注解，也就是说，类型注解再python解释器解释的时候不影响函数执行，但并不会得到类型校验。类型校验要么自己写校验逻辑在函数内部，要么利用特定的库，要么利用Pydantic。不是注解了，就会得到校验，注解只代表你想要这样的输入输出。

## 普通注解
python支持的数据类型进行注解
```python
def greet(name: str) -> str:
    return f"Hello, {name}"
```
## 利用typing模块注解
### Optional[T]
T是一个变量，可以是任何数据类型
表示该位置既可以是类型T，也可以为None。
None不是代表可以是任何数据类型，而是代表这个变量可以不传入值，可以为空。
```python
from typing import Optional
def process_name(name: Optional[str] = None) -> None:
    if name is None:
        print("Name is missing.")
    else:
        print(name.upper())
```
### Union[X, Y]
联合类型，表示值可以是类型 X 或类型 Y 中的任意一个。
```python
from typing import Union
def double_value(x: Union[int, float]) -> float:
    return x * 2.0
```
### Literal[...]
字面量类型，限定变量的取值必须是给定的一个或几个具体值之一。
```python
from typing import Literal
def set_mode(mode: Literal["auto", "manual"]) -> None:
    if mode == "auto":
        print("Automatic mode selected.")
    else:
        print("Manual mode selected.")
```
### List[T]
列表类型，表示该变量是一个列表，列表中的元素类型为 T。
```python
from typing import List
def total_length(strings: List[str]) -> int:
    return sum(len(s) for s in strings)
```
### Any
特殊类型，表示“任意类型”。如果一个变量注解为 Any，静态类型检查基本会跳过对它的类型检查（相当于对该变量关闭了类型检查）。
```python
from typing import Any
def debug_print(data: Any) -> None:
    print("Debug:", data)
```
### Annotated[T, meta]
注解类型，用于将元数据附加到类型注解上。
## 枚举类enum
定义一组有限的常量值。
和Literal的区别是，两者有相似之处，但Literal是静态写死的常量集合，而enum是个类，可继承可扩展，定义的常量是类的属性，有属性名。
### 枚举的定义
```python
from enum import Enum

class Role(Enum):
    DEVELOPER = "developer"
    USER = "user"
    ADMIN = "admin"
```
### 枚举的类型注解用法
将枚举类型用作函数参数或数据模型的类型
```python
def set_role(role: Role) -> None:
    if role is Role.ADMIN:
        print("Grant admin privileges")
    else:
        print(f"Set role to {role.value}")
```

## Pydantic数据类型定义与校验
### BaseModel 模型与类型验证
通过定义一个继承自 BaseModel 的类来声明数据模型。模型的字段通过类属性和类型注解定义，Pydantic 会根据这些注解自动生成初始化、验证等方法。
```python
from pydantic import BaseModel, Field

class User(BaseModel):
    username: str = Field(..., min_length=3)
    age: int = Field(default=18)
```
BaseModel 的作用在于，当我们实例化 User 或使用 Pydantic 提供的解析方法时，自动执行类型检查和转换。
```python
data = {"username": "Alice", "age": "25"}
user = User(**data)
user.age
```
BaseModel 模型还可以方便地进行序列化和反序列化。每个模型实例都有 .model_dump() 方法将其转成字典， .model_dump_json() 方法转成 JSON 字符串。
```python
user.model_dump()  # 输出：{'username': 'Alice', 'age': 25}
user.model_dump_json()  #输出：'{"username":"Alice","age":25}'
```
### Field 参数详解：约束、默认值与别名
在模型定义中，我们经常使用 Field() 来为字段提供额外的验证信息或配置。常用的参数包括：

默认值（default）：
```python
age: int = Field(default=18)
```
长度约束（min_length 和 max_length ）：
类似的有，gt/ge（大于/大于等于）、lt/le（小于/小于等于）用于数值范围校验，regex 用于正则匹配。
```python
Field(min_length=3, max_length=50)  # 要求字符串长度在3到50之间
```
别名（alias）：
别名在输入解析和输出序列化时都会被识别。
```python
class Person(BaseModel):
    full_name: str = Field(alias="name")
    age: int
```
当从字典创建对象时，可以使用 name 作为键传入：Person(name="Bob", age=30)，Pydantic 会将键 name 映射到模型的 full_name 字段。在输出时，默认会使用属性名导出，如果希望导出别名，可以调用 model_dump(by_alias=True)。
```python
person = Person(name="Bob", age=30)
print(person.full_name)           # Bob
print(person.model_dump())        # {'full_name': 'Bob', 'age': 30}
print(person.model_dump(by_alias=True))  # {'name': 'Bob', 'age': 30}
```

总的来说，继承BaseModel类定义的数据类型，形成一个新的数据类，实例化这个类需要传入字典。这样可以让这个新定义的数据类型就代表一个函数或者类输入的一大堆参数，保持简洁又具有数据验证。
## 综合应用（类型分发）
### 条件数据的定义
继承 BaseModel 类定义了三个数据类型。

Literal["START"] = "START" 利用Literal定义了静态常量数据类型，这种结构不是赋值，代表是「类型注解 + 默认值」的组合，等价于：“type 这个字段的值必须是 'START'，而且默认就是 'START'。”

Union[StartEvent, EndEvent] 代表可以是这两个数据类型中的其中一个。

Field(discriminator="type") 传入约束条件，根据type字段的值自动判断使用那个数据类型。

Annotated[..., Field(...)] 表示「对某个类型额外添加元信息」——在这里，就是给 Union[...] 添加一个字段分发规则，这个字段分发规则就是给 Union[...] 这个类型添加的元信息。

代码的全意：这个值可以是 StartEvent 或 EndEvent，请根据字段 "type" 的值来自动选择用哪个类进行解析。以上信息定义了条件数据的验证蓝图，并不进行实际验证，而是设置了筛选和验证的各个模块配置。

class BaseEvent(BaseModel): 首先定义了一个数据模型基类。

```python
from typing import Annotated, Union, Literal
from pydantic import BaseModel, Field

# 定义基础类和若干子类，每个子类都包含判别字段并用 Literal 固定其值
class BaseEvent(BaseModel):
    type: str  # 判别字段

class StartEvent(BaseEvent):
    type: Literal["START"] = "START"
    detail: str

class EndEvent(BaseEvent):
    type: Literal["END"] = "END"
    result: str

# 定义判别联合类型，指定 discriminator 为 "type"
Event = Annotated[Union[StartEvent, EndEvent], Field(discriminator="type")]
```
### 条件数据的解析
Event是一个复杂的数据类型定义（判别联合类型），就是一个数据类型）。

TypeAdapter(Event)：创建一个数据类型验证器，理解类型结构，生成对数据类型的验证代码。万能验证器生成器，可以生成任何数据类型的验证器。

.validate_python(data)：使用适验证器对原始 Python 数据进行类型校验 + 转换。
```python
# ✅ 输入数据（字典形式），包含 type 字段
data = {"type": "START", "detail": "Processing begins"}
# ✅ 使用 Pydantic v2 推荐的 TypeAdapter 接口进行验证和类型自动分发
event = TypeAdapter(Event).validate_python(data)
# 输出验证结果
print(event)          
print(type(event))
```
