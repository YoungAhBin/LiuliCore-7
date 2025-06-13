import graphviz

g = graphviz.Digraph('AI-G')

g.attr(rankdir='LR', fontname='Microsoft YaHei', dpi='600')
g.attr('node', fontname='Microsoft YaHei')
g.attr('edge', fontname='Microsoft YaHei')

with g.subgraph(name='cluster_0') as c:
    c.attr(label='工具链', color='blue')
    c.node_attr.update(color='black')
    c.node('knowledge-ts', shape = "box",
           label='''<
    <table border="0" cellborder="0" cellpadding="3" bgcolor="white">
      <tr>
        <td bgcolor="black" align="center" colspan="2">
          <font color="white">知识类工具</font>
        </td>
      </tr>
      <tr>
        <td align="left" port="r1">(1) RAG：本地知识库</td>
        <td bgcolor="red" align="right">完</td>
      </tr>
      <tr>
        <td align="left" port="r2">(2) 深度研究：联网搜索+推理</td>
        <td bgcolor="grey" align="right">完</td>
      </tr>
      <tr>
        <td align="left" port="r3">(3) SQLite：结构化只是存储</td>
        <td bgcolor="grey" align="right">完</td>
      </tr>
    </table>
    >''')
    c.node('generative-ts', shape = "box", 
           label='''<
    <table border="0" cellborder="0" cellpadding="3" bgcolor="white">
      <tr>
        <td bgcolor="black" align="center" colspan="2">
          <font color="white">生成类工具</font>
        </td>
      </tr>
      <tr>
        <td align="left" port="r4">(1) Dify：低代码 AI 应用平台</td>
        <td bgcolor="grey" align="right">完</td>
      </tr>
      <tr>
        <td align="left" port="r5">(2) ComfyUI：图像生成、视频生成、数字人</td>
        <td bgcolor="grey" align="right">完</td>
      </tr>
    </table>
    >''')
    c.node('operational-ts', shape = "box", 
           label='''<
    <table border="0" cellborder="0" cellpadding="3" bgcolor="white">
      <tr>
        <td bgcolor="black" align="center" colspan="2">
          <font color="white">操作类工具</font>
        </td>
      </tr>
      <tr>
        <td align="left" port="r6">(1) pyautogui：本地操作自动化</td>
        <td bgcolor="grey" align="right">完</td>
      </tr>
      <tr>
        <td align="left" port="r7">(2) Openai 计算机使用代理</td>
        <td bgcolor="grey" align="right">完</td>
      </tr>
    </table>
    >''')
    c.node('programming-ts', shape = "box", 
           label='''<
    <table border="0" cellborder="0" cellpadding="3" bgcolor="white">
      <tr>
        <td bgcolor="black" align="center" colspan="2">
          <font color="white">编程类工具</font>
        </td>
      </tr>
      <tr>
        <td align="left" port="r8">(1) Python REPL：本地安全沙盒环境</td>
        <td bgcolor="grey" align="right">完</td>
      </tr>
      <tr>
        <td align="left" port="r9">(2) codex：代码生成 → 沙盒运行 → 报错修复</td>
        <td bgcolor="grey" align="right">完</td>
      </tr>
    </table>
    >''')
    c.node('auxiliary-ts', shape = "box", 
           label='''<
    <table border="0" cellborder="0" cellpadding="3" bgcolor="white">
      <tr>
        <td bgcolor="black" align="center" colspan="2">
          <font color="white">辅助类工具</font>
        </td>
      </tr>
      <tr>
        <td align="left" port="r10">(1) Graphviz：图形可视化工具包</td>
        <td bgcolor="grey" align="right">完</td>
      </tr>
      <tr>
        <td align="left" port="r11">(2) hengen：数字人</td>
        <td bgcolor="grey" align="right">完</td>
      </tr>
      <tr>
        <td align="left" port="r12">(3) Docker：工作流的云端部署</td>
        <td bgcolor="grey" align="right">完</td>
      </tr>
    </table>
    >''')
    c.node('local-ts', shape = "box", 
           label='''<
    <table border="0" cellborder="0" cellpadding="3" bgcolor="white">
      <tr>
        <td bgcolor="black" align="center" colspan="2">
          <font color="white">本地工具</font>
        </td>
      </tr>
      <tr>
        <td align="left" port="r13">(1) MCP：连接本地工具</td>
        <td bgcolor="grey" align="right">完</td>
      </tr>
    </table>
    >''')

g.node('agents-f', shape = "Mrecord", 
       label='''<
<table border="0" cellborder="0" cellpadding="3" bgcolor="white">
  <tr>
    <td bgcolor="black" align="center" colspan="2">
      <font color="white">智能体框架</font>
    </td>
  </tr>
  <tr>
    <td align="left" port="f1">(1) OpenAI Agents</td>
    <td bgcolor="grey" align="right">完</td>
  </tr>
  <tr>
    <td align="left" port="f2">(2) LangGraph</td>
    <td bgcolor="grey" align="right">完</td>
  </tr>
</table>
>''')

g.node('api-f', shape = "Mrecord", label = '对外 api 服务: FastAPI')

g.node('app-f', shape = "Mrecord", 
       label='''<
<table border="0" cellborder="0" cellpadding="3" bgcolor="white">
  <tr>
    <td bgcolor="black" align="center" colspan="2">
      <font color="white">前端框架</font>
    </td>
  </tr>
  <tr>
    <td align="left" port="f3">(1) Tkinter: 桌面应用程序</td>
    <td bgcolor="grey" align="right">完</td>
  </tr>
  <tr>
    <td align="left" port="f4">(2) Flutter: 移动端应用集成</td>
    <td bgcolor="grey" align="right">完</td>
  </tr>
</table>
>''')

'''
g.edges([('knowledge-ts:r1', 'agents-f'), 
         ('knowledge-ts:r2', 'agents-f'),
         ('knowledge-ts:r3', 'agents-f'),
         ('generative-ts:r4', 'agents-f'),
         ('generative-ts:r5', 'agents-f'),
         ('operational-ts:r6', 'agents-f'),
         ('operational-ts:r7', 'agents-f'),
         ('programming-ts:r8', 'agents-f'),
         ('programming-ts:r9', 'agents-f'),
         ('auxiliary-ts:r10', 'agents-f'),
         ('auxiliary-ts:r11', 'agents-f'),
         ('auxiliary-ts:r12', 'agents-f'),
         ('local-ts:r13', 'agents-f'),])
'''

g.edges([('knowledge-ts', 'agents-f'), 
         ('generative-ts', 'agents-f'),
         ('operational-ts', 'agents-f'),
         ('programming-ts', 'agents-f'),
         ('auxiliary-ts', 'agents-f'),
         ('local-ts', 'agents-f'),])

g.edge('agents-f', 'api-f')
g.edge('api-f', 'app-f')

g.render(filename='grapyoutput/通用', 
         view=False, 
         cleanup=True, 
         format='png', 
         renderer=None,
         outfile=None, 
         engine=None)
