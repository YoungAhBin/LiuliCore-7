# 该文件夹使用说明
1.该文件夹是对openai模型使用案例RAG的整理，把该rag定义的函数分类放在了不同的py文件中，最终自定义了一个rag_tool函数，把所有的函数进行的调用，运行这一个函数就有实现了该RAG定义的全部功能，该函数放在rag_main.py文件中。也就是说，要使用这个RAG只需要调用这一个函数作为工具函数就可以了

2.该RAG是对文档进行拆分成块，然后检索可以用来回答问题的块，对检索到的块可以进行多次拆分，拆分后再次进行检索，得到合适的引用块，并根据检索的块回答问题。最后还会验证回答是否是根据检索到的块进行回答，及检索到的块对回答问题的有效性评级结果

3.以下函数说明，部分说明不能完全对应，因为这是我最开始的简要说明，未做整理，仅供参考

# 安装必要的包
1.%pip install tiktoken pypdf nltk openai pydantic --quiet

# load_document函数说明
1.下载 NLTK 的句子分割模型 punkt_tab，该模型是英文分句模型，适合于英文，中文要导入jieba库，是最流行的中文分句库

2.定义函数 load_document，它接收一个 PDF 下载地址，返回 PDF 提取出的全部文本内容

3.打印提示信息，说明正在从指定 URL 下载 PDF 文件

4.使用 requests.get 发送 GET 请求，获取 PDF 的二进制内容

5.response.raise_for_status()收集请求返回的状态，如果返回异常会抛出错误，并终止程序

6.response.content是PDF文件的二进制数据内容，BytesIO将下载的二进制数据模拟成一个文件对象存储在内存中，相当于读取一个本地pdf文件生成的对象with open("file.pdf", "rb") as f:

7.PdfReader(pdf_bytes)是实例化了一个PdfReader对象，它会解析pdf文件，构建一个pdf文档结构

8.初始化一个空字符串，用于逐页拼接提取出的文本

9.设置一个页数上限为 920 页，超过部分不再处理（如附录、图纸等）

10.使用 enumerate 遍历 PDF 中的每一页，并记录当前页号 i 和页面对象 page

11.如果当前页号超过最大页数上限，则立即跳出循环

12.调用 extract_text() 方法提取当前页的文字内容，并追加到 full_text 变量中，因为pdf文档结构里面有标识符标识文字、图片等结构，所以，这个函数可以解析这些结构，根据结构标识提取文字

14.使用正则表达式匹配文本中的所有英文单词，统计词汇总数

15.选择 GPT-4o 所使用的 tiktoken 分词模型 "o200k_base"，这个模型安装了这个包，就会下载在本地的包中，这里实例化了一个分词对象

16.将全部文本编码为 token 列表，并统计 token 总数

17.打印提取结果，包括页数、词数、token 数量等统计信息

18.返回所有提取出的文本字符串供后续使用

19.定义变量 tbmp_url，为美国专利商标局 TBMP 文件的在线 PDF 地址

20.调用 load_document 函数，下载并提取该 PDF 的文本内容

21.打印分隔线和提示信息，表示即将输出预览内容

22.打印预览区域的分隔符线

23.打印提取文本的前 500 个字符作为文档内容预览

24.再次打印分隔线，标识预览内容结束

# split_into_20_chunks函数说明
1.这段代码主要依靠from nltk.tokenize import sent_tokenize导入的这个函数sent_tokenize把文本划分为一个一个的句子列表

2.for sentence in sentences:循环判断当前片段是否大于最小token数且再增加这个句子就大于2倍的最大token数，就结束当前片段，开启新的片段

3.if current_chunk_sentences:就是给块的列表里面把最后一个不满足一个块的放进块列表里面

4.if len(chunks) > 20:如果最终分的块超过20个，就把所有的句子放在一起，然后平均分配到20个块中

# route_chunks函数说明
1.该段代码通过4.1模型挑选能够用来回答问题的块，及借助便签薄工具生成并记录挑选理由

2.构建系统提示词

3.把用户问题，挑选理由便签薄，20个文本块打包成用户问题

4.tools定义了一个工具，这个工具的输入参数就要求把挑选理由作为参数提供给这个函数

5.text_format定义了输出格式

6.messages定义第一次大模型提问的输入消息，包含系统提示，用户提示

7.大模型调用生成第一次回复

8.把传入的挑选理由便签薄进行赋值，这样这个函数被循环调用，就可以持续记录多次调用的挑选理由

9.for tool_call in response.output:解析模型输出的函数调用参数，就可以提取挑选理由，记录在便签薄中

10.第二次构建模型消息，进行提问，让模型挑选用来回答问题的块

11.if response_chunks.output_text:根据模型输出的块id，再提取块的句子

12.构建最终输出，包含挑选理由和挑选的块

13.多次循环，并且可以看到前面的挑选理由，就形成了推理过程，可以不断更新挑选理由

# navigate_to_paragraphs函数说明
1.split_into_20_chunks函数就是把整篇文本分割成小于等于20个块，每个块有一个id，每个块的句子进行了合并

2.route_chunks函数就是在给定的块中挑选能够用来回答问题的块组成新的列表，里面传入了最大深度参数，传入的最大深度是为了在便签薄中可以准确记录时第几次调用route_chunks函数挑选合适的块

3.navigate_to_paragraphs函数的逻辑：

3.1.建立路径字符串列表，记录块的路径字符串

3.2.for循环，根据最大深度，对文本进行多次拆分和挑选

3.2.1. 第一次循环都要进行两次挑选，先对以500为最小token拆分的块进行一次挑选，未达最大深度再进行以200为最小token的拆分

3.2.2. 新的一次循环，开始先进行挑选，如果还是未达最大深度，再以最小200token进行拆分，再进入循环进行挑选

4.最终挑选出来的是块，并不是自然段落

# generate_answer函数说明
1.调用navigate_to_paragraphs函数对输入文档进行多轮拆分挑选，打印出结果

2.@field_validator('citations')是 Pydantic 2.x 中的字段验证装饰器，被装饰的这个函数validate_citations会在数据模型LegalAnswer创建或者赋值时自动触发，验证字段 citations的合法性，保证必须输出合法的字段，不合法时抛出错误

3.generate_answer函数里面的代码response.output_parsed._valid_citations = valid_citations代表强行给模型的回复输出里面注入_valid_citations字段

4.info.data 是 Pydantic 2.x 中 ValidationInfo 提供的字段访问入口，而info.data 包含的是模型实例中所有字段值，所以可以通过info.data.get('_valid_citations', [])提取

5.所以存在一个问题，只有运行这段代码response.output_parsed._valid_citations = valid_citations传入_valid_citations才能验证，而触发验证在response = client.responses.parse，而传入字段在后，所以验证的时候没传入字段，无法进行验证。

# verify_answer函数说明
1.从所有被选中的段落中，筛选出被模型回答实际引用的段落，并将这些引用段落打印展示出来，供用户参考

2.这段代码会输出在挑选出来的段落中，那些段落被用于回答这次的问题。被用于回答问题的段被存储在一个列表中，但具体有没有不是被挑选的段落倍引用来回答问题，说不清

3.构建了一个规范模型输出的数据类型。is_accurate: 回答是否准确，布尔值；explanation: 解释验证结论的原因（由 GPT 写出）；confidence: 可信等级，限定为 high、medium、low 之一。使用 Literal[...] 限制可能的值，避免拼写错误。

4.验证回答，用模型验证回答，输入上方代码生成的从引用段落筛选出来存在于被挑选的段落中的段落组成的列表cited_paragraphs，输入用户的问题，输入针对问题generate_answer函数产生的回答

5.在verify_answer函数内部通过模型，比对cited_paragraphs和上方模型生成的回复中的citations等，只用 GPT 自己引用的段落来验证 GPT 回答是否真的引用得当、内容准确，并通过结构化返回 是否准确 + 解释 + 信心等级

6.所以这一块完成了验证，而不是上方的 @field_validator('citations')

# rag_tool函数说明
1.该函数是对上面所有函数的调用，一个函数把上面定义的所有函数功能组织到了一块，运行一个函数实现所有功能

# 导入库的说明
1.导入 requests 模块，用于从网络请求下载 PDF 文件（二进制内容）

2.导入 BytesIO，用于将下载的二进制数据包装成内存中文件对象，供 PDF 解析器使用

3.导入 PdfReader，用于读取 PDF 文件结构，并支持逐页提取文本

4.导入正则表达式模块（re），用于匹配所有英文单词，实现词数统计

5.导入 tiktoken 模块，用于对文本进行分词并统计 token 数量（适用于 GPT 模型）

6.导入 sent_tokenize，用于英文分句（此处未实际使用）

7.导入 nltk 自然语言处理工具包，用于下载句子分割模型等

8.导入 Python 类型注解模块（当前函数未使用，但方便未来函数参数说明）
