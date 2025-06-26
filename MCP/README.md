MCP主要用于大模型调用工具的通用接口协议。通信方式分为管道通信和SSE通信，这里以管道通信的方式连接客户端与服务端。整个过程是在大模型function calling的基础之上，通过自动化注册工具，生成工具说明信息，通道通信把服务端提供的工具的说明传递给大模型，大模型根据需要生成function calling的调用信息，提取整理工具调用信息，再通过管道通信传递给服务端，运行函数，返回结果给大模型。

## 服务端
通过装饰器快速定义工具。
```python
from fastmcp import FastMCP

# Create a named server
mcp = FastMCP("Math Operations Server")

# Define mathematical operation tools
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b
```

## 客户端
StdioServerParameters接口指定如何启动服务端子进程，因为客户端是主进程，已经启动了，和服务端不是一个进程，所以服务端才需要另外启动

stdio_client(...)接口启动子进程，并和子进程建立管道通信，返回读和写两个函数对象。管道通信使用的是JSON-RPC 2.0 协议，有固定的数据结构，就是json格式的几个键是固定的。建立管道背后运行的是以下代码，启动子进程服务，创建服务端和客户端的缓存区，建立专门的管道联通两个缓存区，客户端和服务端的读写都是在自己的缓存区读写，通过flush() 把自己缓存区的发送到对面的缓存区，供对方读取。
```python
import subprocess
server = subprocess.Popen(
    ["python", "server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
```

ClientSession()传入两个读和写函数，创建会话对象。ClientSession()是个会话管理器。

list_tools()方法可以从服务端获取工具说明
```python
