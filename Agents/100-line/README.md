## BaseNode类
__init__：里面定义了两个属性，一个参数字典属性，一个后继节点字典属性

set_params：设置参数函数，把传入的参数保存在参数字典属性

next：传入后继的节点对象和action；注册后继节点在后继节点字典属性    ⭐核心函数

prep：从shared字典中提取输入

exec：节点的核心执行逻辑

post：回写shared，返回action。负责打印、存储、日志、跳转action的功能

_exec：是exec函数的内部替代版，在内部运行都是调用的_exec函数替代exec函数，因为_exec函数调用exec函数增加了很多通用逻辑，比如报错后循环多次尝试exec函数的功能

_run：内部调用函数，把prep、_exec、post串联起来

run：调用_run函数，可以增加自己需要的功能，供外部调用

__rshift__：内部核心逻辑self.next(后继节点)，起到装饰作用，让node1 >> node2 相当于 node1.next(node2)，这是为了在调用next函数时传入的节点对象无action时适用

__sub__：借助_ConditionalTransition类，如果调用next函数时传入的参数有action时适用，让让node1 - "success" >> node2 相当于 node1.next(node2, "success")
