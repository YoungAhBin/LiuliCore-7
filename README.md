# LiuliCore-7
self-AI Knowledge Base.

![](知识图谱.png)

## RAG
说明：  借用的是OpenAI的4.1模型使用案例，通过对文档的多次拆分→模型挑选，选出回答问题的文本块，并对文本块对问题回答的支持情况做出评级，并且通过后验确保回答问题依据的是挑选出来的文本块

使用方法：  在rag_main.py文件里面定义的rag_tool函数，调用了所有功能函数，实现了该RAG的全部功能，直接调用这个函数就可以。里面的模型使用的是4.1模型，可以用合适的模型替代

引用地址：  https://cookbook.openai.com/examples/partners/model_selection_guide/model_selection_guide#adaptation-decision-tr

## Graphviz
说明： Graphviz里面是Graphviz的python库生成该库首页说明文档制图图谱示意图的完整代码，该代码已经实现了常用的大部分功能

使用方法： 根据该知识图谱示意图的示例代码、示例代码的说明文档、Graphviz官方的示例代码和Graphviz的python库的示例代码，就可以编码自己的图。由于Graphviz的python库只是通过这个框架写出dot代码，启动渲染引擎渲染，所以要正常使用，必须先安装Graphviz，即先安装引擎

怎么安装： Graphviz官网下载zip压缩包，解压到合适位置就算安装好了，把bin文件的路径添加到环境变量的path里面。如"D:\Graphviz-13.0.0-win64\bin"

官方案例地址：  https://graphviz.org/Gallery/directed/psg.html

Graphviz的python库的案例地址：  https://graphviz.readthedocs.io/en/stable/examples.html

## Docker
说明：在wsl子系统中准备操作系统、系统依赖、项目依赖、项目源码、设置环境变量，测试，在wsl中测试完全没有问题后，就可以打包成镜像上传到云服务器，因为是docker镜像，所以云服务器也要安装docker，才能打开镜像运行起来。由于要打包成镜像，所以在wsl子系统中最开始配置环境的时候就要先建立一个docker容器，后面才能使用docker commit和docker save保存成镜像。

使用方法：根据cocker文件夹里面的说明文件，一步一步测试建立，这个就实现了在本地一步一步测试建立可以正常运行后再打包成镜像。安装的过程中出错可以随时纠正，能够明显的显示错误。

## Agents
官方Github仓库地址： https://github.com/The-Pocket/PocketFlow/tree/main

## MCP
官方Github仓库地址： https://github.com/modelcontextprotocol/python-sdk

## A2A
包含协议底层代码的案例地址： https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-a2a

## database
SQLAlchemy官方地址： https://docs.sqlalchemy.org/en/20/

## auto
官方Github仓库地址： https://github.com/asweigart

## exec
python的内置函数，用于执行代码，官方地址：https://docs.python.org/3/library/functions.html#exec

## Time_Series_Analysis
SARIMA参考仓库： https://github.com/ajitsingh98/Time-Series-Analysis-and-Forecasting-with-Python

神经网络模型用于时间序列预测的模型TimeFM: https://github.com/google-research/timesfm
有一个模型微调的jupyter文件，把这个学会就可以了，这个文件里面导入的模块都在scr文件夹里面

## Data_analysis_AI
抽取pandasai核心： https://github.com/sinaptik-ai/pandas-ai
主要参考内容在pandasai文件夹的core文件夹，提示词的构建最为重要

## mapreduce
利用100——line这个agents框架的批处理节点实现map功能，mapreduce的核心就是先把数据分块，每个块分配一个键，把键值对给map函数进行处理，map函数之后可以对每个map的输出进行排序、合并等整理，最后经过reduce对每个map函数的输出统一进行排序、合并等整理并输出。100_line的批处理节点是对普通节点的_exec_函数调用，用_exec_函数循环处理一批一批的数据，返回所有批的处理结果，实现了数据的批处理，而prep函数和post函数并没有变，prep函数实现数据的分块和键值对的定义，post函数对所有批的结果进行统一处理相当于reduce函数，最后都存入shared字典。

## Digital humans

## flux(ComfyUI)

## 视频生成(ComfyUI)

## deep research

## LangGraph

## Flutter
