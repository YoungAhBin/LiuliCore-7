## 向量数据库的本地部署

使用这个向量数据库，只需要pip安装，就可以import导入，然后使用。

test.py 文件里面进行了简答的测试，和如何本地部署到自己的项目中的方法。

embedding_store.py 是直接复制的mem0项目的向量存储方法接口的封装方法，直接借助这个封装好的对向量数据库的增删改查的方法操作chromadb数据库。官方教程文档：  https://docs.trychroma.com/docs/overview/getting-started

openai_embedding.py 是对openai嵌入模型接口的封装，便于调用。

test_embedding_store.py 是对embedding_store.py中全部方法的调用测试。

chromadb数据库的github仓库可以下载该项目需要的配置文件requirements.txt：  https://github.com/chroma-core/chroma/tree/main

使用的时候要确定存储的向量数据库是在本地还是在内存中。
