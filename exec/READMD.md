# exec函数（python内置函数）

python的内置函数，所以使用的时候不用导入任何库，用于执行python代码。

exec(source, /, globals=None, locals=None, *, closure=None)

## source 输入方式（字符串、代码文件、代码对象）
```python
code_str = """
for i in range(3):
    print("执行第", i + 1, "次")
"""

exec(code_str)
```
```python
with open(r"C:\Users\传防科电脑\Desktop\test.py", "r", encoding="utf-8") as f:
    file_code = f.read()

exec(file_code)
```
```python
code_obj = compile("""
total = 0
for i in range(5):
    total += i
print("总和为：", total)
""", filename="<string>", mode="exec")

exec(code_obj)

# compile() 将字符串编译为“代码对象（code object）。filename 是调试用的名字（可以写 <string>）。
# 注意传给exec()函数的代码外部不能有返回值，也就是说你不能传入一个函数，你可以传入一段代码，这段代码里面包含的函数可以有返回值。因为exec()本身是没有返回值的。
# 所以这块compile的mode是exec，是语句；如果是表达式，如3+5，则模式是eval,eval函数有返回值。
```

## globals 和 locals
### 不传 globals 和 locals（代码在当前作用域中执行）
当前作用域等于在exec所在的代码块的作用域，可以利用exec的外部定义的变量，生成的y变量外部也可以调用。
```python
x = 10

exec("y = x + 5")

print(y)  # 输出 15，因为 exec() 使用的是当前作用域，直接创建了变量 y
```
### 只传 globals，它会同时管理“全局变量 + 局部变量”
globals作为全局变量的管理字典，在exec内传入这个字典，exec内运行的代码的全部变量全部会保存在这个字典中。
```python
global_scope = {'x': 100}
exec("y = x + 50", global_scope)

print(global_scope['y'])  # 输出 150
```
### 同时传 globals 和 locals（两套作用域）,全局变量和局部变量分开管理
```python
g = {'x': 100}
l = {}

exec("y = x + 1", g, l)

print("全局 g:", g)
print("局部 l:", l)

# 输出   全局 g: {'x': 100, '__builtins__': <builtins module>}
# 输出   局部 l: {'y': 101}
```
### 通过手动指定 __builtins__，可以控制 exec() 能访问的内建函数
```python
restricted_globals = {
    '__builtins__': {'print': print}  # 禁止除了 print 之外的内建函数
}

exec("print('我可以打印')", restricted_globals)  # ✅ OK
exec("open('file.txt', 'w')", restricted_globals)  # ❌ 报错：open 不存在
```
