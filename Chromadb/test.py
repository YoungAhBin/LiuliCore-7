# 怎么让包作为项目的模块使用
# 第一步安装（命令行运行）： pip install chromadb
# 第二步获取模块路径（命令行运行）： python -c "import chromadb; print(chromadb.file)"。获取到的路径： "D:\anaconda3\Lib\site-packages\chromadb"
# 第三步：根据路径找到安装文件，复制安装的三个文件到项目文件夹
# 第四步：导入使用的时候，需要运行以下命令
# import sys
# sys.path.insert(0, "./")  # 让 Python 优先查找当前目录
# chromadb向量数据库项目本身就有很多依赖需要安装，所以还要安装这个项目的依赖文件requirements.txt
# chromadb默认使用自己的嵌入模型向量化，要使用默认嵌入模型，需提前自行下载，靠程序自己下载会面临ssl错误

import sys
sys.path.insert(0, "./")  # 让 Python 优先查找当前目录

import chromadb

chroma_client = chromadb.Client() # 实例化数据库对象

collection = chroma_client.create_collection(name="libin_memory", embedding_function=None) # 创建集合，embedding_function=None禁止使用默认嵌入模型，创建集合时可以传入自定义嵌入模型

from typing import Optional, Literal
from openai import OpenAI
client = OpenAI()
def embed(text: str, memory_action: Optional[Literal["add", "search", "update"]] = None):
    text = text.replace("\n", " ")
    response = client.embeddings.create(
        input=[text],  
        model="text-embedding-3-large"
    )
    return response.data[0].embedding
embed1 = embed(text="我是陕西省商洛市人，我在商州区疾病预防控制中心担任卫生应急办公室主任和预警监测科科长。")
embed2 = embed(text="我酷爱人工智能，因此我学了python编程，主要用于人工智能。")
embeddings = [embed1, embed2]

# 集合里面添加数据
collection.add(
    ids=["id1", "id2"],
    embeddings=embeddings,
    documents=["我是陕西省商洛市人，我在商州区疾病预防控制中心担任卫生应急办公室主任和预警监测科科长。", "我酷爱人工智能，因此我学了python编程，主要用于人工智能。"],
    metadatas=[{"chapter": 1, "verse": 0}, {"chapter": 1, "verse": 1}],  
)

# 查询集合里面的数据
query_embed = embed(text="我的爱好是。")
results = collection.query(
    query_embeddings=[query_embed]
)
print(results)

