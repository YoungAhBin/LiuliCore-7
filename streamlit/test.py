import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ===写入===
st.title("七宝琉璃")  
st.text("测试一下")
st.markdown("这是 **st.markdown** 输出的 Markdown 文本。")
st.write("Hello, *Streamlit!* :sunglasses:") 
st.write("支持显示各种类型的数据：", 123, {"key": "value"})  

# ===组件===
st.write("请填写您的信息：")
name = st.text_input("姓名")          # 文本输入
age = st.slider("年龄", 0, 120, 25)   # 数字滑动条，默认值25
occupation = st.selectbox("职业", ["学生", "工程师", "医生", "其他"])  # 下拉选择
subscribe = st.checkbox("订阅新闻邮件")  # 复选框

# 提交按钮
if st.button("提交"):
    st.write(f"姓名：{name}")
    st.write(f"年龄：{age}")
    st.write(f"职业：{occupation}")
    st.write(f"订阅邮件：{'是' if subscribe else '否'}")

# ===表单容器===
# 在表单容器内添加部件
with st.form("my_form"):
    st.write("请填写下列信息后提交：")
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    agree = st.checkbox("我同意条款")
    # 表单提交按钮
    submitted = st.form_submit_button("提交")

# 表单提交后的处理
if submitted:
    if agree:
        st.success(f"表单已提交！欢迎，{username} 🎉")
    else:
        st.error("请同意条款后再提交。")

# ===内置绘图===
# 生成示例数据：20行3列的随机数数据框
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["产品A", "产品B", "产品C"]
)

st.line_chart(chart_data)  # 绘制折线图
st.bar_chart(chart_data)   # 绘制条形图

# ===外部绘图===
# 使用 Matplotlib 绘制示例图表
x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)
fig, ax = plt.subplots()
ax.plot(x, y, color="red", linewidth=2)
st.pyplot(fig)  # 将 Matplotlib 图表嵌入 Streamlit 页面

# ===表格===
df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五"],
    "年龄": [28, 34, 29],
    "得分": [85, 92, 78]
})

st.dataframe(df)  # 可交互的表格展示
st.table(df.head(2))  # 静态表格，仅显示前两行

# ===会话状态===
# 由于交互后，app,py脚本从被重新从头执行，所以局部变量无法得到保存，就有了会话状态，可以存储再会话状态字典，刷新后可以从会话状态中获取
# 初始化 Session State 中的变量
if "count" not in st.session_state:
    st.session_state.count = 0

# 一个按钮，每次点击使计数加1
if st.button("点击我增加计数"):
    st.session_state.count += 1

st.write(f"当前计数：{st.session_state.count}")

# ===回调函数===
# 在组件输入更改之后，页面刷新之前运行
# 定义回调函数：将 session_state 中 input_text 的值转换为大写
def convert_to_upper():
    st.session_state.output_text = st.session_state.input_text.upper()

# 创建文本输入，绑定回调
st.text_input("请输入文本：", key="input_text", on_change=convert_to_upper)
# 实时显示转换后的结果（如果 output_text 尚未设置，则显示空串）
st.write("大写转换结果：", st.session_state.get("output_text", ""))

# ---------------布局与页面结构---------------------------

# ===列布局===
col1, col2 = st.columns(2)
col1.write("这是第一列")
col2.write("这是第二列")

# 不同宽度的列，例如三列比例为3:1:1
col_a, col_b, col_c = st.columns([3, 1, 1])
col_a.write("较宽的一列")
col_b.write("较窄的一列")
col_c.write("较窄的一列")


col1, col2 = st.columns(2)
with col1:
    st.button("按钮 1")
with col2:
    st.button("按钮 2")

# ===选项卡===
# 标签页形式切换显示
tab1, tab2 = st.tabs(["选项卡1", "选项卡2"])
with tab1:
    st.write("这里是选项卡1的内容")
with tab2:
    st.write("这里是选项卡2的内容")

# ===侧边栏===
# 将组件放在侧边
st.sidebar.title("侧边栏")  # 侧边栏标题
st.sidebar.radio("页面导航", ["首页", "数据概览", "关于"])  # 单选框导航

# 或使用 with 语法
with st.sidebar:
    st.slider("全局参数调整", 0, 100, 50)
    st.checkbox("显示详细信息")


# ===折叠区===
# 防止可选说明、附加细节
with st.expander("点击展开查看更多信息"):
    st.write("这里是额外的信息，可以折叠或展开。")
    st.image("https://docs.streamlit.io/en/stable/_static/logo.png", width=100)

# ===跳转页===
# pages文件夹放置，就会自动出现在导航栏，以下是专门插入
st.page_link("pages/data.py", label="查看数据总结", icon="📊")


# ===启动代码===
@echo off
cd /d %~dp0

call venv\Scripts\activate.bat
streamlit run app.py

pause
