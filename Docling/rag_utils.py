from __future__ import annotations
from typing import Any, Dict, Iterable, List
from pathlib import Path
from langchain_core.documents import Document
import json
import os

# —— 小工具 —— #
def _to_str_path(p: Any) -> str | None:
    if p is None:
        return None
    return str(p).replace("\\", "/")  # 统一路径风格，便于查重/展示

def _first(x: List[Any] | None) -> Any | None:
    return x[0] if isinstance(x, list) and x else None

def _json_safe(v: Any):
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    if isinstance(v, (list, tuple, set)):
        return [_json_safe(x) for x in v]
    if isinstance(v, dict):
        return {str(k): _json_safe(v2) for k, v2 in v.items()}
    return str(v)

# —— 核心：一次性扁平化为 Chroma 友好元数据 —— #
def flatten_docling_for_chroma(
    d: Document,
    keep_raw_json: bool = True,    # 是否把原始 dl_meta 以字符串保留
) -> Document:
    meta: Dict[str, Any] = dict(d.metadata or {})
    dl = meta.pop("dl_meta", {}) or {}

    # 解析 docling 结构
    origin = dl.get("origin", {}) or {}
    doc_items: List[Dict[str, Any]] = dl.get("doc_items", []) or []
    headings: List[str] = dl.get("headings", []) or []

    # 页码集合
    pages = sorted({
        prov.get("page_no")
        for it in doc_items
        for prov in (it.get("prov") or [])
        if isinstance(prov, dict) and "page_no" in prov
    })
    page_start = pages[0] if pages else None
    page_end = pages[-1] if pages else None

    # 第一个块的 bbox（常用于定位/可视化）
    first_bbox = None
    for it in doc_items:
        provs = it.get("prov") or []
        if provs and isinstance(provs[0], dict):
            first_bbox = provs[0].get("bbox")
            break

    # 标签
    labels = [it.get("label") for it in doc_items if "label" in it]
    label_primary = _first(labels)
    labels_csv = ",".join(map(str, labels)) if labels else None

    # 关键信息“白名单” + 规范化为标量
    source = meta.get("source") or origin.get("filename")
    source = _to_str_path(source)  # Path/WindowsPath -> str

    flat: Dict[str, Any] = {
        # 源信息
        "source": source,
        "filename": origin.get("filename") or (os.path.basename(source) if source else None),
        "mimetype": origin.get("mimetype"),
        "heading": " > ".join(headings) if headings else None,

        # 页码（标量 + 字符串范围，兼容 where 过滤）
        "page_start": page_start,
        "page_end": page_end,
        "pages_csv": (str(page_start) if page_start == page_end and page_start is not None
                      else (f"{page_start}-{page_end}" if page_start and page_end else None)),

        # 位置（全部标量）
        "bbox_l": first_bbox.get("l") if first_bbox else None,
        "bbox_r": first_bbox.get("r") if first_bbox else None,
        "bbox_t": first_bbox.get("t") if first_bbox else None,
        "bbox_b": first_bbox.get("b") if first_bbox else None,

        # 语义层 & 标签（标量/CSV）
        "content_layer": doc_items[0].get("content_layer") if doc_items else None,
        "label": label_primary,
        "labels_csv": labels_csv,
    }

    # 把原 meta 里其余简单字段带上（复杂的一律字符串化）
    for k, v in meta.items():
        if k in flat:  # 避免覆盖
            continue
        if isinstance(v, (str, int, float, bool)) or v is None:
            flat[k] = v
        elif isinstance(v, Path):
            flat[k] = _to_str_path(v)
        else:
            flat[k] = str(v)

    # 可选：保留完整原始 dl_meta 为字符串（便于回溯/调试）
    if keep_raw_json and dl:
        flat["dl_meta_json"] = json.dumps(_json_safe(dl), ensure_ascii=False)

    # 最终兜底：确保所有值都是 Chroma 接受的类型（str/int/float/bool/None）
    for k, v in list(flat.items()):
        if not isinstance(v, (str, int, float, bool, type(None))):
            flat[k] = str(v)

    return Document(page_content=d.page_content, metadata=flat)

def flatten_many_for_chroma(docs: Iterable[Document], keep_raw_json: bool = True) -> List[Document]:
    return [flatten_docling_for_chroma(d, keep_raw_json=keep_raw_json) for d in docs]

