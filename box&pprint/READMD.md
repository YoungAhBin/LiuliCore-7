box和pprint两个库组合，方便json数据格式的写入和清晰的展示：
```python
from box import Box
from pprint import pprint

# 初始化 Box
store = Box(default_box=True)

# ==== 写入数据 ====
store.pipeline.step1.result.score = 0.93
store.pipeline.step1.result.status = "ok"
store.pipeline.step2.config.lr = 0.01
store.pipeline.step2.config.epochs = 10

# ==== 读取数据 ====
print("Step1 Score:", store.pipeline.step1.result.score)
print("Learning Rate:", store.pipeline.step2.config.lr)

# ==== 打印结构 ====
print("\n完整结构 (pprint)：")
pprint(store.to_dict(), width=100, indent=2)
```
