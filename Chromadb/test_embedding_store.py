import time
from embedding_store import ChromaDB
from openai_embedding import embed

def test_chromadb():
    collection_name = f"test_collection_{int(time.time())}"  # 避免重名
    db = ChromaDB(collection_name)

    print(f"\n[1] 当前所有集合：")
    print(db.list_cols())

    # 插入数据
    texts = ["hello world", "openai embedding test", "vector database"]
    vectors = [embed(text) for text in texts]
    ids = [f"vec_{i}" for i in range(len(texts))]
    payloads = [{"text": text} for text in texts]
    db.insert(vectors=vectors, payloads=payloads, ids=ids)

    print(f"\n[2] 插入后集合信息：")
    print(db.col_info())

    print(f"\n[3] 查询测试：")
    query_vector = embed("hello openai")
    results = db.search(query="hello openai", vectors=[query_vector], limit=2)
    for res in results:
        print(res)

    print(f"\n[4] 单个向量读取 get(id)：")
    result = db.get(ids[0])
    print(result)

    print(f"\n[5] 更新向量（payload）测试：")
    db.update(vector_id=ids[0], payload={"text": "updated text"})
    updated = db.get(ids[0])
    print(updated)

    print(f"\n[6] list(filters=None)：")
    all_vectors = db.list()
    for vec in all_vectors:
        print(vec)

    print(f"\n[7] 删除向量测试：")
    db.delete(vector_id=ids[1])
    try:
        deleted = db.get(ids[1])
    except Exception as e:
        print(f"已删除向量无法获取: {e}")

    print(f"\n[8] 重置集合测试（delete + recreate）：")
    db.reset()
    print("集合已重置后再次查看：")
    print(db.col_info())

    print(f"\n[9] 删除整个集合测试：")
    db.delete_col()
    print("集合删除完成。")

if __name__ == "__main__":
    test_chromadb()
