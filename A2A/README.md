A2A协议主要用于智能体之间通信的通用协议。服务端借助Starlette建立可被访问的地址端口，客户端通过get和post请求与服务端发生通信，获取服务。所以，这个协议结合100-line智能体框架，可以完美实现轻量的服务器部署至云端，其它智能体生成请求的命令通过客户端访问云端公开的地址就可以。(以下内容为这个A2A小项目的注解）

# common/utils/in_memory_cache.py
## class InMemoryCache
### 定义了三个属性
_instance：内存缓存单例对象。由于它是类级对象，不是实例对象，所以它是单例。

_lock：线程锁对象。

_initialized：布尔值，表示只能初始化一次。
### def __new__(cls)函数
保证多线程下只创建一个实例，因为这是缓存，智能体初始化后全局只需要这一个缓存对象就可以。
### def __init__(self)函数
保证对象创建后只初始化一次。
### def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None函数
缓存中写入键值对，并且写入键和存储的时间+ttl表示缓存过期的时间。
### def get(self, key: str, default: Any = None) -> Any函数
通过key获取缓存值，如果找不到或者缓存过期都返回默认值，并且过期的缓存会被删除键值对和过期时间。
### def delete(self, key: str) -> bool函数
通过key找到缓存值和过期时间，并且删除缓存值和过期时间，返回true。如果key找不到缓存值，返回false。
### def clear(self) -> bool函数
清空所有缓存，返回true。

# common/utils/push_notification_auth.py 
## class PushNotificationAuth
### def _calculate_request_body_sha256(self, data: dict[str, Any])函数
把传入的请求体转化成json格式，然后计算请求体的哈希值，并返回。
## class PushNotificationSenderAuth(PushNotificationAuth)
### def __init__(self)函数
定义了两个属性，公钥列表属性和私钥属性。
### async def verify_push_notification_url(url: str) -> bool函数
验证url地址是否可以正常访问，发送一个字符串让返回回来，看是否可以正常返回。
### def generate_jwk(self)函数
利用函数生成密钥key，根据key生成公钥和密钥保存在属性中。
### def handle_jwks_endpoint(self, _request: Request)函数
返回公钥匙，用于服务端验证。
### def _generate_jwt(self, data: dict[str, Any])函数
生成载荷包的签发时间（就是请求时间），把签发时间和请求体的哈希值，以及私钥、请求头一块打包返回。
### async def send_push_notification(self, url: str, data: dict[str, Any])函数
访问服务端url，把_generate_jwt函数打包的内容发送至服务端获取回复。
## class PushNotificationReceiverAuth(PushNotificationAuth)
### def __init__(self)函数
定义了两个属性，保存请求客户端返回的公钥jwks的属性，获取公钥jwks的会话实例jwks_client。
### async def load_jwks(self, jwks_url: str)函数
传入获取客户端公钥的url，返回获取公钥的会话实例jwks_client。
### async def verify_push_notification(self, request: Request) -> bool函数
从客户端获取公钥，比对公钥和私钥，完成鉴权。对请求体从新计算哈希值，和请求体的哈希值比对，看是否请求体被修改。根据现在的时间和请求时间比对，看是否自请求发起已经超过了5秒，过时访问。

# common/client/card_resolver.py
## class A2ACardResolver
### def __init__(self, base_url, agent_card_path="/.well-known/agent.json")函数
对输入的参数进行处理，获得两个属性，这两个属性组合就是完整的get请求的url。
### def get_agent_card(self) -> AgentCard函数
组合两个属性的值，形成完整url，建立会话请求，获取agentcard。

# common/client/client.py
## class A2AClientError(Exception)
内部未定义，只是继承了父类的属性和方法。
## class RpcError(Exception)
在Exception类的基础上，增加了几个属性，增加的属性主要是为了显示JSON-RPC 的错误响应。
## class A2AClient
### def __init__(self, agent_card: AgentCard = None, url: str = None)函数
定义了两个属性，一个是服务端的url，直接传入或者从agentcard获得；另一个属性是建立了一个https请求客户端对象。
### def _generateRequestId(self)函数
构建请求id的函数，根据时间，在当前时间的基础上加1000就是请求id。
### async def _send_request(self, request: JSONRPCRequest) -> dict[str, Any]函数
发送 JSON-RPC 请求到服务器并返回解析后的 JSON 响应字典。包括日志、错误处理等。
### async def send_task(self, payload: dict[str, Any]) -> SendTaskResponse函数
调用_send_request函数发送任务，获得回复。
### async def send_task_streaming(self, payload: dict[str, Any]) -> AsyncIterable[SendTaskStreamingResponse]函数
发送流式任务，获得流式输出。
### async def get_task(self, payload: dict[str, Any]) -> GetTaskResponse函数
借用_send_request函数发送请求，获取任务状态。
### async def cancel_task(self, payload: dict[str, Any]) -> CancelTaskResponse函数
借用_send_request函数发送请求，取消任务。
### async def set_task_callback(self, payload: dict[str, Any]) -> SetTaskPushNotificationResponse函数
借用_send_request函数发送请求，设置任务推送配置。
### async def get_task_callback(self, payload: dict[str, Any]) -> GetTaskPushNotificationResponse函数
借用_send_request函数发送请求，获取任务推送配置。

# common/server/server.py
## class A2AServer
### def __init__函数
输入端口号、agent_card、任务管理器类对象。根据输入建立端口号属性、agent_card属性、任务管理器对象属性、实例化一个Starlette()服务器对象用于通信。并且建立了两个路由，增加进Starlette()对象里面，一个路由用于客户端访问获取agent_card，一个路由用于和客户端通信接受任务和返回任务结果。
### def start(self)函数
利用uvicorn.run启动服务器。
### def _get_agent_card(self, request: Request) -> JSONResponse函数
返回agent_card的信息给客户端。
### async def _create_response(self, result: Any) -> JSONResponse | EventSourceResponse函数
TaskManager 返回的结果解析生成响应返回给客户端。

# common/server/task_manager.py
## class TaskManager(ABC)
定义了任务管理器中对各种任务情况进行处理的方法接口，没有核心逻辑，核心逻辑再继承这个类的类里面实现。可以自定义，官方也给了这些方法的实际定义的类。
## class InMemoryTaskManager(TaskManager)
继承TaskManager，对里面的类的核心逻辑代码进行具体的定义。

# a2a_client.py
主要功能就是构造payload，payload需要会话id、任务id、message（包括角色、提示词，和给大模型发送的消息一样），客户端希望返回的类型。构造的payload作为A2A协议定义的客户端函数response = await client.send_task(payload)函数发送给服务端获取回复。由于实例化client时传入了url， client = A2AClient(url=agent_url)，所以直接就访问到了服务端。

# a2a_server.py
利用AgentCard类型构造AgentCard。

实例化a2a协议的服务端，server = A2AServer(agent_card=agent_card,task_manager=task_manager,host=host,port=port,)。

启动服务器，利用A2A协议的start函数，server.start()。

# task_manager.py
def _get_user_query函数提取用户文本作为智能体的输入，被async def on_send_task调用。

async def on_send_task函数获取用户提问，生成智能体对象agent_flow = create_agent_flow()，运行智能体agent_flow.run(shared_data) ，从shared_data中获取智能体输出作为结果返回。

由于客户端的请求就是send_task，所以任务管理里面也只对这个函数进行了重新定义。

# 其它就是节点、工作流、主函数的定义。

# 只需要运行以下三行代码就可以启动这个服务器，并通过客户端的输入访问。main.py只是为了测试工作流，并不是整个A2A服务的启动文件。
```python
# 环境变量
export OPENAI_API_KEY=sk-...
# 终端 A：启动服务端
python a2a_server.py --host 0.0.0.0 --port 10003
# 终端 B：启动客户端 CLI
python a2a_client.py --agent-url http://localhost:10003
```

由于a2a_server.py会一直占用进程，但不读键盘；它只是挂在 Uvicorn 里等待 HTTP 请求。a2a_client.py在 while True 里循环 click.prompt(...)，等待你输入问题。只有客户端需要持续等待键盘输入；服务端启动后就静静监听端口，不会要求你再在同一进程里打什么命令。A2A 协议天生就是“HTTP 双端”模型，所以客户端和服务端必然分进程。所以，服务端和客户端要在两个命令行窗口运行。一个agent的输出作为客户端的输入发给服务端，就完成了两个agent的沟通。只要把服务器搬到云上、开放端口，客户端把 URL 指向公网地址，A2A 链路就无缝生效；把一个 Agent 的输出作为另一个 Agent 的输入，本质上就是 A2A 协议的“任务接力”模式，额外代码改动为零。

注意;使用A2A协议的时候，客户端注意payload的构建，服务端注意AgentCard的构建。task_manager.py根据客户端请求的任务处置，构建响应的任务处置函数，并且SUPPORTED_CONTENT_TYPES要与payload的acceptedOutputModes的一致。
