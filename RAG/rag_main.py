import requests
from io import BytesIO
from pypdf import PdfReader
import re
import tiktoken
# from nltk.tokenize import sent_tokenize
# import nltk
from typing import List, Dict, Any
from docx import Document
from openai import OpenAI
import json
from typing import List, Dict, Any
from typing import List, Dict, Any
from pydantic import BaseModel, field_validator
from typing import List, Dict, Any, Literal
from pydantic import BaseModel

from rag_doc_deal import load_docx
from rag_retrieval import split_into_20_chunks
from rag_retrieval import navigate_to_paragraphs
from rag_answer import generate_answer
from rag_verification import verify_answer

# Global tokenizer name to use consistently throughout the code
TOKENIZER_NAME = "o200k_base"
# Initialize OpenAI client
client = OpenAI()

def rag_tool(local_path: str, question: str):
    # Load the document
    # tbmp_url = "https://www.uspto.gov/sites/default/files/documents/tbmp-Master-June2024.pdf"
    document_text = load_docx(local_path)
    
    # Show the first 500 characters
    print("\n文档预览（前500个字符）:")
    print("-" * 50)
    print(document_text[:500])
    print("-" * 50)

    # Split the document into 20 chunks with minimum token size
    document_chunks = split_into_20_chunks(document_text, min_tokens=500)

    # Run the navigation for a sample question
    question = question
    navigation_result = navigate_to_paragraphs(document_text, question, max_depth=2)
    
    # Sample retrieved paragraph
    print("\n==== 前三个检索到的段落 ====")
    for i, paragraph in enumerate(navigation_result["paragraphs"][:3]):
        display_id = paragraph.get("display_id", str(paragraph["id"]))
        print(f"\nPARAGRAPH {i+1} (ID: {display_id}):")
        print("-" * 40)
        print(paragraph["text"])
        print("-" * 40)

    # Generate an answer
    answer = generate_answer(question, navigation_result["paragraphs"], 
                           navigation_result["scratchpad"])

    cited_paragraphs = []
    for paragraph in navigation_result["paragraphs"]:
        para_id = str(paragraph.get("display_id", str(paragraph["id"])))
        if para_id in answer.citations:
            cited_paragraphs.append(paragraph)
        
    
    # Display the cited paragraphs for the audience
    print("\n==== 被引用的段落 ====")
    for i, paragraph in enumerate(cited_paragraphs):
        display_id = paragraph.get("display_id", str(paragraph["id"]))
        print(f"\nPARAGRAPH {i+1} (ID: {display_id}):")
        print("-" * 40)
        print(paragraph["text"])
        print("-" * 40)

    # Verify the answer using only the cited paragraphs
    verification = verify_answer(question, answer, cited_paragraphs)
    
    # Display final result with verification
    print("\n==== 最终验证的答案 ====")
    print(f"Verification: {'PASSED' if verification.is_accurate else 'FAILED'} | Confidence: {verification.confidence}")
    print("\nAnswer:")
    print(answer.answer)
    print("\nCitations:")
    for citation in answer.citations:
        print(f"- {citation}")
        
local_path = r"E:\2023手足口\陕西省水痘防控方案new(1).docx"
question = "水痘病例需要居家隔离多长时间，才可以入校。"

rag_tool(local_path, question)