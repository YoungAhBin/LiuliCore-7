这是我根据pandas库的函数写的一个透视函数：
```python
# 加载数据

import pandas as pd


def read_csv(filepath) -> pd.DataFrame:
    cols_to_use = ['患者姓名', '患儿家长姓名', '有效证件号', '性别', '出生日期', '年龄', '患者工作单位', '联系电话', '现住详细地址', '人群分类', '病例分类', '发病日期', '诊断时间', '死亡日期', '疾病名称', '订正前病种', '订正前诊断时间', '订正前终审时间', '填卡医生', '医生填卡日期', '报告单位', '单位类型', '报告卡录入时间', '录卡用户', '录卡用户所属单位', '县区审核时间',]
    df = pd.read_csv(filepath, encoding='gb18030', usecols=cols_to_use, dtype={"联系电话": "object"})
    return df



# 数据预处理

def age_to_years(x):
    if pd.isna(x):
        return pd.NA
    x = str(x).strip()
    
    if "岁" in x:
        return float(x.replace("岁", ""))
    elif "月" in x:
        return float(x.replace("月", "")) / 12
    elif "天" in x:
        return float(x.replace("天", "")) / 365
    else:
        return pd.NA

def pre_deal(df: pd.DataFrame) -> pd.DataFrame:

    # 数据预处理（时间）
    df['发病日期'] = pd.to_datetime(df['发病日期'], format="%Y-%m-%d")
    df['报告卡录入时间'] = pd.to_datetime(df['报告卡录入时间'], format="%Y-%m-%d %H:%M:%S")
    
    df["发病年"] = df["发病日期"].dt.year
    df["发病月"] = df["发病日期"].dt.month
    df["发病日"] = df["发病日期"].dt.day
    df["发病周"] = df["发病日期"].dt.dayofweek  
    # df["发病时"] = df["发病日期"].dt.hour

    # 数据预处理（街道/乡镇）
    names = ["城关", "陈塬", "大赵峪", "刘湾", "腰市", "大荆", "夜村", "杨斜", "黑山", "闫村","阎村", "牧护关", "麻街", "三岔河", "杨峪河", "北宽坪", "沙河子", "金陵寺", "板桥"]
    pattern = "(" + "|".join(names) + ")"
    
    df["街道/乡镇"] = df["现住详细地址"].str.extract(pattern, expand=False).fillna("未知")
    df["街道/乡镇"] = df["街道/乡镇"].str.replace("阎村", "闫村")

    # 数据预处理（年龄）
    df["年龄"] = df["年龄"].map(age_to_years)

    return df


# 数据分析

# 筛选函数
def filter_cases(df: pd.DataFrame, conditions: list) -> pd.DataFrame:
    mask = None  # 初始为空
    
    for cond in conditions:
        col, op, val = cond["col"], cond["op"], cond["val"]
        logic = cond.get("logic", "and").lower()
        
        # 构造当前条件
        if op == "==":
            submask = (df[col] == val)
        elif op == "!=":
            submask = (df[col] != val)
        elif op == ">":
            submask = (df[col] > val)
        elif op == ">=":
            submask = (df[col] >= val)
        elif op == "<":
            submask = (df[col] < val)
        elif op == "<=":
            submask = (df[col] <= val)
        elif op == "in":
            submask = df[col].isin(val)
        elif op == "not in":
            submask = ~df[col].isin(val)
        elif op == "between":
            submask = df[col].between(val[0], val[1])
        else:
            raise ValueError(f"不支持的操作符: {op}")
        
        # 逻辑组合
        if mask is None:
            mask = submask  
        else:
            if logic == "and":
                mask &= submask
            elif logic == "or":
                mask |= submask
            else:
                raise ValueError(f"不支持的逻辑操作: {logic}")
    
    return df[mask]


# 组合函数
def group_cases(df: pd.DataFrame,
                piv_r: str,
                piv_c: str = None,
                piv_v: str = None,
                method: str = "size") -> pd.DataFrame:
    # 1) 分组
    if piv_c:
        grouped = df.groupby([piv_r, piv_c])
    else:
        grouped = df.groupby(piv_r)
    
    # 2) 聚合
    if method == "size":
        value = grouped.size().reset_index(name="size")
        colname = "size"
    elif method == "count":
        value = grouped[piv_v].count().reset_index(name="count")
        colname = "count"
    elif method == "sum":
        value = grouped[piv_v].sum().reset_index(name="sum")
        colname = "sum"
    elif method == "median":
        value = grouped[piv_v].median().reset_index(name="median")
        colname = "median"
    else:
        raise ValueError(f"不支持的 method: {method}")
    
    # 3) 透视（只有同时有行和列时才做）
    if piv_c:
        df_pivoted = value.pivot(index=piv_r, columns=piv_c, values=colname).fillna(0)
        return df_pivoted
    else:
        return value

# 透视函数
def pivotby(df: pd.DataFrame,
            rows: str,
            cols: str | None = None,
            values: str | None = None,
            method: str = "size",
            conditions: list | None = None) -> pd.DataFrame:

    df_filtered = filter_cases(df, conditions or [])
    df_pivoted = group_cases(df_filtered, rows, cols, values, method) 

    return df_pivoted
```
