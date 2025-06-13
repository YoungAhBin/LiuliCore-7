Graphviz的python库类似于langgraph，先实例化一个对象，然后不断地给这个实例化对象中增加节点和边，最后经过渲染器渲染就成为需要的图了。

## 实例化对象
```python
g = graphviz.Digraph('AI-G')
```

## 设置图属性、节点属性、边属性
```python
g.attr(rankdir='LR', fontname='Microsoft YaHei', dpi='600')
g.attr('node', fontname='Microsoft YaHei')
g.attr('edge', fontname='Microsoft YaHei')
```

## 子图的生成（包括子图属性、子图节点属性、子图节点定义）
```python
with g.subgraph(name='cluster_0') as c:
    c.attr(label='工具链', color='blue')
    c.node_attr.update(color='black')
    c.node('knowledge-ts', shape = "box", label='')
```

## 利用html-like语言生成复杂的节点label
```python
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
```

## 节点的定义
```python
g.node('api-f', shape = "Mrecord", label = '对外 api 服务: FastAPI')
```

## 边的定义
```python
g.edge('agents-f', 'api-f', label='')
```

## 依次定义多个边
```python
g.edges([('knowledge-ts', 'agents-f'), 
         ('generative-ts', 'agents-f'),
         ('operational-ts', 'agents-f'),
         ('programming-ts', 'agents-f'),
         ('auxiliary-ts', 'agents-f'),
         ('local-ts', 'agents-f'),])
```

## html-like定义的label内端口的引用
端口引用连接的节点，shape不能是Mrecord
```python
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
```




