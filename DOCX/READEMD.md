这个是建立word文档的开源库，可以创建文档，插入内容，并且进行自动排版的功能。

以下是我在jupyter上测试过的案例
```python
# 分为段落和运行两级，标题也是段落。运行是段落中的一部分文字，可以对这一部分文字设置下划线、加粗等设置。

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt
from docx.shared import RGBColor
from docx.enum.text import WD_TAB_ALIGNMENT, WD_ALIGN_PARAGRAPH, WD_UNDERLINE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Inches

# 设置变量（全文报告基于8月份，所以设置的全局变量）
month_number = 8
month = "2025-08"
diseases = ["流行性感冒", "水痘", "手足口病", "新型冠状病毒感染", "其他感染性腹泻病"]
chinese_numbers = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
df = data

# 因为docx里面只能辨别出英文字体，使用英文字体需要设置这个qn('w:eastAsia')
def set_chinese_font_for_style(style, font_name='仿宋'):
    rPr = style._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), font_name)

# 创建空白文档
doc = Document()

# 创建数据分析实例
analyzer = DiseaseAnalyzer(df=df, diseases=diseases, month=month)

# 仿宋 三号
style_main = doc.styles.add_style('MyMainStyle', WD_STYLE_TYPE.PARAGRAPH)
style_main.base_style = doc.styles['Normal']
style_main.font.name = '仿宋'
style_main.font.size = Pt(16)
style_main.font.bold = False
set_chinese_font_for_style(style_main, '仿宋')

# 仿宋 小二
style_heading = doc.styles.add_style('MyHeadingStyle', WD_STYLE_TYPE.PARAGRAPH)
style_heading.base_style = doc.styles['Normal']
style_heading.font.name = '仿宋'
style_heading.font.size = Pt(18)
style_heading.font.bold = True
set_chinese_font_for_style(style_heading, '仿宋')

# 宋体 五号
style_heading = doc.styles.add_style('MyGraghHeadingStyle', WD_STYLE_TYPE.PARAGRAPH)
style_heading.base_style = doc.styles['Normal']
style_heading.font.name = '宋体'
style_heading.font.size = Pt(10.5)
style_heading.font.bold = True
set_chinese_font_for_style(style_heading, '仿宋')

# 方正小标宋 简体 标题
style_title = doc.styles.add_style('MyTitleStyle', WD_STYLE_TYPE.PARAGRAPH)
style_title.base_style = doc.styles['Normal']
style_title.font.name = '方正小标宋简体'
style_title.font.size = Pt(22)
style_title.font.bold = False
style_title.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
set_chinese_font_for_style(style_title, '方正小标宋简体')

# 提示1
para_hint_one = doc.add_paragraph('☆内部资料')
para_hint_one.style = 'MyMainStyle'
para_hint_one.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
para_hint_one.paragraph_format.right_indent = Pt(28.2)

# 提示2
para_hint_two = doc.add_paragraph('☆妥善保管')
para_hint_two.style = 'MyMainStyle'
para_hint_two.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
para_hint_two.paragraph_format.right_indent = Pt(28.2)

# 空行
doc.add_paragraph()

# 创建文章标题
headingmain = doc.add_paragraph(f'商州区突发公共卫生事件及需关注的\n传染病{month_number}月风险评估报告')
headingmain.style = 'MyTitleStyle'
headingmain.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

# 两个标注说明：自定义的字体只能给段落用，下一级的运行需通过设置属性。下划线也只能给运行添加，段落没有下划线属性。
# 标注1
note_one = doc.add_paragraph()
note_one.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

note_one_run = note_one.add_run(f'2025年第{month_number}期')
note_one_run.font.name = '仿宋'
note_one_run.font.size = Pt(18)
note_one_run._element.rPr.rFonts.set(qn('w:eastAsia'), '仿宋')

# 标注2
note_two = doc.add_paragraph()

note_two_run = note_two.add_run(f'\t商州区疾病预防控制中心\t\t\t2025年{month_number}月1号\t')
note_two_run.font.name = '仿宋'
note_two_run.font.size = Pt(16)
note_two_run.font.underline = True
note_two_run._element.rPr.rFonts.set(qn('w:eastAsia'), '仿宋')

# 空行
doc.add_paragraph()

# 一级标题1
heading1 = doc.add_paragraph('一、商州区近期重点疫情概况')
heading1.style = 'MyHeadingStyle'
heading1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
heading1.paragraph_format.left_indent = Pt(28.2)

for i, disease in enumerate(diseases):
    # 中文序号
    section_number = chinese_numbers[i]  # '一', '二', ...
    # 图编号（从1开始）
    graph_number = i + 1

    # 二级标题
    heading = doc.add_paragraph(f'（{section_number}）{disease}')
    heading.style = 'MyMainStyle'
    heading.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    heading.paragraph_format.left_indent = Pt(28.2)

    # 正文
    result = analyzer.summarize_disease_for_month(disease=disease, month=month)
    text = doc.add_paragraph(f'{result["value"]}')
    text.style = 'MyMainStyle'
    text.paragraph_format.first_line_indent = Pt(28.2)
    text.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    text.paragraph_format.line_spacing = 1.3

    # 插图
    img_stream = analyzer.plot_monthly_trend(disease_name=disease, month=month)
    doc.add_picture(img_stream, width=Inches(6))
    
    # 图标题
    graph_heading = doc.add_paragraph(f'图{graph_number} 商州区{disease}报告发病分布情况')
    graph_heading.style = 'MyGraghHeadingStyle'
    graph_heading.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

# 一级标题2
heading1 = doc.add_paragraph('二、风险评估结果及建议')
heading1.style = 'MyHeadingStyle'
heading1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
heading1.paragraph_format.left_indent = Pt(28.2)

# 二级标题2.1
month_summary = analyzer.summarize_all_diseases_in_month(month)
month_summary_text = doc.add_paragraph(f'{month_summary["value"]}')
month_summary_text.style = 'MyMainStyle'
month_summary_text.paragraph_format.first_line_indent = Pt(28.2)
month_summary_text.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
month_summary_text.paragraph_format.line_spacing = 1.3

# 二级标题2.2
# analysis_summary_text = doc.add_paragraph(f'目前，{my_doc_paragraph}')
# analysis_summary_text.style = 'MyMainStyle'
# analysis_summary_text.paragraph_format.first_line_indent = Pt(28.2)
# analysis_summary_text.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
# analysis_summary_text.paragraph_format.line_spacing = 1.3

# 保存文档
doc.save('demo.docx')

# 展示文章链接可供下载
import IPython
IPython.display.FileLink('demo.docx')
```
