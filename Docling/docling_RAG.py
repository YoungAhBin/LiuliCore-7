# 模型配置

import os
os.environ["DOCLING_ARTIFACTS_PATH"] = r"D:\RAG_docling\models"


# 参数配置

from pathlib import Path
from langchain_core.prompts import PromptTemplate
from langchain_docling.loader import ExportType

data_folder = Path(__file__).parent / "data"
FILE_PATH = data_folder / "pdf/Docling 项目深度分析报告.pdf"
EMBED_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
GEN_MODEL_ID = "mistralai/Mixtral-8x7B-Instruct-v0.1"
EXPORT_TYPE = ExportType.DOC_CHUNKS
QUESTION = "docling的主要功能是？"
PROMPT = PromptTemplate.from_template(
    "Context information is below.\n---------------------\n{context}\n---------------------\nGiven the context information and not prior knowledge, answer the query.\nQuery: {input}\nAnswer:\n",
)
TOP_K = 3


# 文档解析 + OCR

from langchain_docling import DoclingLoader

from docling.chunking import HybridChunker

from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from transformers import AutoTokenizer

from docling.chunking import HybridChunker

LOCAL_EMBED_MODEL = r"D:\RAG_docling\models\all-MiniLM-L6-v2"
MAX_TOKENS = 64  # set to a small number for illustrative purposes

tokenizer = HuggingFaceTokenizer(
    tokenizer=AutoTokenizer.from_pretrained(LOCAL_EMBED_MODEL),
    max_tokens=MAX_TOKENS,  # optional, by default derived from `tokenizer` for HF case
)

loader = DoclingLoader(
    file_path=FILE_PATH,
    export_type=EXPORT_TYPE,
    chunker=HybridChunker(tokenizer=tokenizer),
)

docs = loader.load()

if EXPORT_TYPE == ExportType.DOC_CHUNKS:
    splits = docs
elif EXPORT_TYPE == ExportType.MARKDOWN:
    from langchain_text_splitters import MarkdownHeaderTextSplitter

    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "Header_1"),
            ("##", "Header_2"),
            ("###", "Header_3"),
        ],
    )
    splits = [split for doc in docs for split in splitter.split_text(doc.page_content)]
else:
    raise ValueError(f"Unexpected export type: {EXPORT_TYPE}")

# for d in splits[:3]:
    # print(f"- {d.page_content=}")
# print("...")

from pprint import pprint

for i, d in enumerate(splits[:3], 1):
    print(f"\n=== Split #{i} ===")
    # 只截取前 300 字做预览，避免刷屏
    text = d.page_content.replace("\n", " ")
    head = (text[:300] + "…") if len(text) > 300 else text
    print(f"text[{len(d.page_content)} chars]: {head}")
    print("metadata:")
    pprint(d.metadata, sort_dicts=True, compact=True)
print("\n...")

from rag_utils import flatten_many_for_chroma
flat_splits = flatten_many_for_chroma(splits, keep_raw_json=True)
print(flat_splits[:3])

# 嵌入生成 + 向量库存储

import json
from pathlib import Path
from tempfile import mkdtemp

from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

embedding = HuggingFaceEmbeddings(model_name=r"D:\RAG_docling\models\all-MiniLM-L6-v2")

chroma_path = r"D:\docling_test\vectorstores\chroma"
Path(chroma_path).parent.mkdir(parents=True, exist_ok=True)

vectorstore = Chroma.from_documents(
    documents=flat_splits,
    embedding=embedding,
    collection_name="docling_demo",
    persist_directory=chroma_path
)

# LLM查询

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI

retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})
llm = ChatOpenAI(
    model="qwen-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def clip_text(text, threshold=100):
    return f"{text[:threshold]}..." if len(text) > threshold else text

question_answer_chain = create_stuff_documents_chain(llm, PROMPT)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)
resp_dict = rag_chain.invoke({"input": QUESTION})

clipped_answer = clip_text(resp_dict["answer"], threshold=200)
print(f"Question:\n{resp_dict['input']}\n\nAnswer:\n{clipped_answer}")
for i, doc in enumerate(resp_dict["context"]):
    print()
    print(f"Source {i + 1}:")
    print(f"  text: {json.dumps(clip_text(doc.page_content, threshold=350), ensure_ascii=False)}")
    for key in doc.metadata:
        if key != "pk":
            val = doc.metadata.get(key)
            clipped_val = clip_text(val) if isinstance(val, str) else val
            print(f"  {key}: {clipped_val}")