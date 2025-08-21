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