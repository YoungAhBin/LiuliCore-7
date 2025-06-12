from rag_config import *

# Download nltk data if not already present
# nltk.download('punkt')
def sent_tokenize(text):
    pattern = r'(?<=[。！？])'
    sentences = re.split(pattern, text)
    return [s.strip() for s in sentences if s.strip()]

def load_document(url: str) -> str:
    """Load a document from a URL and return its text content."""
    print(f"Downloading document from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    pdf_bytes = BytesIO(response.content)
    pdf_reader = PdfReader(pdf_bytes)
    
    full_text = ""
    

    max_page = 920  # Page cutoff before section 1000 (Interferences)
    for i, page in enumerate(pdf_reader.pages):
        if i >= max_page:
            break
        full_text += page.extract_text() + "\n"
    
    # Count words and tokens
    word_count = len(re.findall(r'\b\w+\b', full_text))
    
    tokenizer = tiktoken.get_encoding("o200k_base")
    token_count = len(tokenizer.encode(full_text))
    
    print(f"Document loaded: {len(pdf_reader.pages)} pages, {word_count} words, {token_count} tokens")
    return full_text

def load_docx(path: str) -> str:
    """加载本地的 .docx Word 文档并返回其文本内容。"""
    doc = Document(path)
    full_text = "\n".join([para.text for para in doc.paragraphs])

    # Count words and tokens
    word_count = len(re.findall(r'\b\w+\b', full_text))
    
    tokenizer = tiktoken.get_encoding("o200k_base")
    token_count = len(tokenizer.encode(full_text))
    
    print(f"已加载的文档： {word_count} words, {token_count} tokens")
    return full_text