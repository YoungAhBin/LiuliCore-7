以下是利用该库，我最喜欢的外形格式示例：
```python
import matplotlib.pyplot as plt

def plot(df: pd.DataFrame, disease: str):
    # 数据准备
    cond = [
        {"col": "疾病名称", "op": "==", "val": disease},
    ]
    tbl_ph = pivotby(df, rows="发病月", cols="发病年", method="size", conditions=cond)
    
    now = pd.Timestamp.today()
    cur_year, cur_month = now.year, now.month
    if cur_year in tbl_ph.columns:
        tbl_ph.loc[tbl_ph.index > cur_month, cur_year] = pd.NA
    
    plt.rcParams['font.sans-serif'] = ['SimHei']  
    plt.rcParams['axes.unicode_minus'] = False

    # 绘图
    fig, ax = plt.subplots(figsize=(8, 3))
    
    for year in tbl_ph.columns:
        ax.plot(tbl_ph.index, tbl_ph[year], marker="o", label=str(year))
    
    ax.set_xlabel("月份", rotation=0, labelpad=15)
    ax.set_ylabel("病\n例\n数", rotation=0, labelpad=15)
    
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # ax.legend(loc="right")

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),
        ncol=7
    )
        
    return fig
```
