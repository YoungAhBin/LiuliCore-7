
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).parent
env = Environment(
    loader=FileSystemLoader(ROOT / "prompts"),
    undefined=StrictUndefined,        # 缺变量就抛错，调试更安全
    trim_blocks=True,
    lstrip_blocks=True,
    autoescape=False                  # 生成纯文本 Prompt
)

# 自定义过滤器：示例把 **markdown** 转成上下包围符号
def markdown(text: str, mark="**"):
    return f"{mark}{text}{mark}"
env.filters["markdown"] = markdown

# -------- 1. 载入 YAML（多文档） ---------------------------------
with open(ROOT / "prompts" / "system_messages.yaml", encoding="utf-8") as f:
    docs = list(yaml.safe_load_all(f))

meta, prompt_cfg, *_ = docs      # 这里只演示第二份文档

# -------- 2. 取模板 & 变量 ---------------------------------------
template = env.get_template("base_prompt.jinja2")
context = {
    "user_query": "咳嗽需要做核酸吗？",
    "history": [
        {"role": "assistant", "content": "您好，有什么可以帮您？"},
        {"role": "user", "content": "我咳嗽了一周，需要做核酸吗？"}
    ],
    "messages": prompt_cfg["messages"]
}

# -------- 3. 渲染并输出 ------------------------------------------
rendered_prompt = template.render(**context)
print("="*30)
print(rendered_prompt)
print("="*30)
