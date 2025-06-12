"""
Central config & shared imports for RAG demo
把所有公共依赖集中到这里，其他模块只需
`from rag_config import *`
"""

# ─── 标准库 ───────────────────────────────────────────────
import re, json, os, sys, logging
from io import BytesIO
from typing import List, Dict, Any, Literal

# ─── 第三方库 ────────────────────────────────────────────
import requests, tiktoken
from pypdf import PdfReader
from docx import Document
from openai import OpenAI
from pydantic import BaseModel, field_validator

# ─── 常量 & 单例 ─────────────────────────────────────────
TOKENIZER_NAME = "o200k_base"      # 全局唯一
client = OpenAI()                  # 全局唯一

# 限定 star-import 时可见的名字
__all__ = [
    "re", "json", "BytesIO", "List", "Dict", "Any", "Literal",
    "requests", "tiktoken", "PdfReader", "Document",
    "BaseModel", "field_validator",
    "TOKENIZER_NAME", "client",
]
