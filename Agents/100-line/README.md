该框架定义了节点，定义了工作流。通过后继节点属性实现了工作流功能，通过shared工作流各个节点共享的上下文实现了节点之间结果的传递，最重要的就是prep、exec、post的定义。整个框架自由且简单，轻量方便部署。

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

## _ConditionalTransition类
内部通过__rshift__实现调用next函数时传入参数action时的DSL风格的连接

## Node类
内部重写了_exec，让节点运行的时候，如果exec运行出错，可以多次尝试运行依然报错的情况下再报错

## BatchNode类
节点的批处理类，输入给_exec函数是一个批量数据时，循环调用_exec函数批量处理

## Flow类
__init__：继承了BaseNode类的属性，定义了一个起始节点对象的属性

start：获取起始节点。传入起始节点，注册起始节点进入起始节点属性，返回起始节点

get_next_node：传入当前节点和action，从当前节点的后继节点字典属性里面通过action取出后继节点对象    ⭐核心函数

_orch：curr从起始节点属性里面获取起始节点，建立工作流的时候会传入起始节点flow = Flow(start=chat_node)；p从Flow类自BaseNode类继承的参数属性中获取参数，这个参数时工作流的参数，是传入工作流的每一个节点的静态参数，所有节点共享，通用是模型、温度等；while curr循环，curr.set_params(p)先把静态参数设置进每一个节点的参数字典属性里面，last_action = curr._run(shared)然后运行每一个节点，copy.copy(self.get_next_node(curr, last_action))最后通过get_next_node函数获得下一个要运行的节点。由于最后一个节点没有后继节点，也就是不会有self.next(后继节点)给它的后继节点字典属性里面注册后继节点执行这一段代码的时候copy.copy(self.get_next_node(curr, last_action))，get_next_node无法从最后一个节点的后继节点字典属性里面取出后继节点，循环也就中断了，工作流也就结束了；由于运行last_action = curr._run(shared)返回的last_action会影响copy.copy(self.get_next_node(curr, last_action))提取的下一个节点是什么节点，而返回last_action是由_run函数里面的post函数决定的，所以post函数可以决定下一个节点到底是什么节点。    ⭐核心函数

| 你的理解点                                                         | 是否正确 | 说明                                                                                             |
| ------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------ |
| `curr` 从 `start_node` 开始                                         | ✅      | 正确，`curr = copy.copy(self.start_node)` 是从流程入口节点开始执行                                  |
| `p` 是流程参数，传入每个节点                                          | ✅      | 是的，`p = params or self.params` 这一点你解释得很清楚，是静态参数，通常包含模型信息、温度、角色等     |
| 所有节点共享 `p`                                                     | ✅      | 正确，它在每次 `curr.set_params(p)` 中被注入到每个节点内部，用于统一配置                              |
| `_run(shared)` 执行节点并返回 `last_action`                          | ✅      | 这是流程的核心运行调用，内部实际是 `prep → exec → post` 的封装                                       |
| `get_next_node(curr, last_action)` 根据 `last_action` 决定下一个节点 | ✅      | 正确，跳转逻辑基于 `curr.successors[action]`，由上一个节点的执行结果控制                              |
| 最后一个节点没有后继 → 流程终止                                       | ✅      | 是的，最后一次调用 `get_next_node(...)` 返回 `None`，`while curr:` 终止                              |
| `post()` 决定 `last_action` → 控制流程跳转                           | ✅      | 完全正确，`post()` 的返回值即是用于控制流程的 action 标签，比如 `"yes"`、`"no"`、`"retry"` 等          |

## shared共享上下文
shared字典会在主程序调用的时候新建，传入工作流，再传入_orch，再传入节点的_run函数，由于它是主程序调用的时候新建的，而且它会传入每一个节点的_run函数里面的prep和post函数，所以它是工作流中每个节点共享的上下文，_exec传入的是prep从shared中提取的参数。

以下各个类都是上面各个类的异步重写和批处理调用，没有其它太大变化。
