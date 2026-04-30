from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "final" / "final_presentation.pptx"
FIG_DIR = ROOT / "CS_590NN_690NN_Final_Project_Template" / "figures"

WIDE_W = Inches(13.333)
WIDE_H = Inches(7.5)

NAVY = RGBColor(29, 39, 53)
MUTED = RGBColor(94, 108, 132)
LIGHT = RGBColor(246, 248, 250)
LINE = RGBColor(217, 222, 229)
TEAL = RGBColor(20, 132, 121)
RED = RGBColor(185, 72, 70)
GOLD = RGBColor(183, 128, 33)
WHITE = RGBColor(255, 255, 255)


def add_text(slide, text, x, y, w, h, size=24, bold=False, color=NAVY,
             align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.clear()
    frame.margin_left = Inches(0.04)
    frame.margin_right = Inches(0.04)
    frame.margin_top = Inches(0.02)
    frame.margin_bottom = Inches(0.02)
    frame.vertical_anchor = valign
    p = frame.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = "Aptos"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return box


def add_bullets(slide, items, x, y, w, h, size=22, color=NAVY):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.clear()
    frame.margin_left = Inches(0.08)
    frame.margin_right = Inches(0.08)
    frame.margin_top = Inches(0.03)
    frame.margin_bottom = Inches(0.03)
    for idx, item in enumerate(items):
        p = frame.paragraphs[0] if idx == 0 else frame.add_paragraph()
        p.text = item
        p.level = 0
        p.font.name = "Aptos"
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(10)
    return box


def add_title(slide, title, subtitle=None):
    add_text(slide, title, 0.65, 0.36, 10.8, 0.58, size=29, bold=True)
    if subtitle:
        add_text(slide, subtitle, 0.68, 0.93, 10.6, 0.34, size=13, color=MUTED)
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.66), Inches(1.26), Inches(12.0), Inches(0.02)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = LINE
    line.line.fill.background()


def add_footer(slide, idx):
    add_text(slide, "CS 590NN Final Project", 0.66, 7.04, 3.2, 0.22, size=8, color=MUTED)
    add_text(slide, str(idx), 12.3, 7.04, 0.35, 0.22, size=8, color=MUTED, align=PP_ALIGN.RIGHT)


def add_card(slide, x, y, w, h, fill=LIGHT, line=LINE):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line
    shape.line.width = Pt(0.75)
    return shape


def add_metric(slide, value, label, x, y, color):
    add_text(slide, value, x, y, 2.35, 0.72, size=36, bold=True, color=color, align=PP_ALIGN.CENTER)
    add_text(slide, label, x, y + 0.73, 2.35, 0.42, size=11, color=MUTED, align=PP_ALIGN.CENTER)


def add_table(slide, rows, x, y, w, h, widths=None):
    table_shape = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(h))
    table = table_shape.table
    if widths:
        for col_idx, width in enumerate(widths):
            table.columns[col_idx].width = Inches(width)
    for r, row in enumerate(rows):
        for c, value in enumerate(row):
            cell = table.cell(r, c)
            cell.text = value
            cell.margin_left = Inches(0.05)
            cell.margin_right = Inches(0.05)
            cell.margin_top = Inches(0.03)
            cell.margin_bottom = Inches(0.03)
            para = cell.text_frame.paragraphs[0]
            para.font.name = "Aptos"
            para.font.size = Pt(12 if r else 11)
            para.font.bold = r == 0
            para.font.color.rgb = WHITE if r == 0 else NAVY
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY if r == 0 else (LIGHT if r % 2 == 1 else WHITE)
    return table_shape


def add_image_fit(slide, path, x, y, w, h):
    pic = slide.shapes.add_picture(str(path), Inches(x), Inches(y), width=Inches(w))
    scale = min(Inches(w) / pic.width, Inches(h) / pic.height)
    pic.width = int(pic.width * scale)
    pic.height = int(pic.height * scale)
    pic.left = Inches(x) + int((Inches(w) - pic.width) / 2)
    pic.top = Inches(y) + int((Inches(h) - pic.height) / 2)
    return pic


def build():
    prs = Presentation()
    prs.slide_width = WIDE_W
    prs.slide_height = WIDE_H
    blank = prs.slide_layouts[6]

    # 1. Title
    slide = prs.slides.add_slide(blank)
    add_text(slide, "Trajectory supervision for continual tool-use learning",
             0.72, 0.72, 8.6, 1.3, size=36, bold=True)
    add_text(slide, "Single-seed Llama 3.1 8B QLoRA pilot on API-Bank",
             0.76, 2.02, 7.6, 0.36, size=17, color=MUTED)
    add_card(slide, 8.95, 0.78, 3.55, 2.9, fill=WHITE)
    add_text(slide, "+17.7 pts", 9.25, 1.18, 2.95, 0.76, size=38, bold=True, color=TEAL, align=PP_ALIGN.CENTER)
    add_text(slide, "final exact full-call accuracy\nCondition B over A",
             9.42, 2.02, 2.6, 0.72, size=14, color=NAVY, align=PP_ALIGN.CENTER)
    add_text(slide, "A: stripped context  |  B: trajectory context",
             9.28, 3.05, 3.0, 0.32, size=11, color=MUTED, align=PP_ALIGN.CENTER)
    add_bullets(slide, [
        "Question: does preserving API-call trajectory context help continual tool-use fine-tuning?",
        "Result: B improves API selection and final exact calls, but formatting errors increase.",
        "Caveat: one seed and B has 25.1% more training tokens."
    ], 0.86, 3.22, 7.8, 1.62, size=20)
    add_text(slide, "Vishnu Vardhan Reddy B, Sagnik Chatterjee, Soumik Bhatta",
             0.78, 6.08, 8.7, 0.34, size=14, color=NAVY)
    add_text(slide, "CS 590NN / 690NN Final Project",
             0.78, 6.42, 5.4, 0.28, size=11, color=MUTED)
    add_footer(slide, 1)

    # 2. Motivation
    slide = prs.slides.add_slide(blank)
    add_title(slide, "Motivation", "Tool-use learning often discards the intermediate action trace.")
    add_bullets(slide, [
        "Many fine-tuning examples supervise the final answer or next call in isolation.",
        "Tool-use tasks naturally contain structured process traces: prior API calls, arguments, and observations.",
        "We test whether keeping that trace helps the model retain API behavior across sequential training blocks."
    ], 0.78, 1.68, 6.2, 2.1, size=22)
    add_card(slide, 7.36, 1.64, 4.95, 3.15, fill=WHITE)
    add_text(slide, "Process proxy, not hidden reasoning", 7.72, 1.98, 4.2, 0.36, size=21, bold=True)
    add_bullets(slide, [
        "Uses observable API trajectory fields.",
        "Avoids claiming access to private chain-of-thought.",
        "Compares two prompt formats under the same API-Bank split."
    ], 7.72, 2.56, 4.05, 1.58, size=17)
    add_footer(slide, 2)

    # 3. Experiment design
    slide = prs.slides.add_slide(blank)
    add_title(slide, "Experiment Design", "Four sequential API-Bank blocks; evaluate all blocks after each training stage.")
    x0 = 0.98
    for i, label in enumerate(["D1", "D2", "D3", "D4"]):
        add_card(slide, x0 + i * 2.55, 2.05, 1.65, 0.88, fill=WHITE)
        add_text(slide, label, x0 + i * 2.55, 2.22, 1.65, 0.28, size=23, bold=True, color=TEAL, align=PP_ALIGN.CENTER)
        add_text(slide, "train stage", x0 + i * 2.55, 2.55, 1.65, 0.2, size=9, color=MUTED, align=PP_ALIGN.CENTER)
        if i < 3:
            add_text(slide, ">", x0 + 1.79 + i * 2.55, 2.24, 0.45, 0.28, size=25, bold=True, color=MUTED, align=PP_ALIGN.CENTER)
    add_text(slide, "After each stage: score D1-D4", 1.15, 3.24, 9.7, 0.36, size=21, bold=True, align=PP_ALIGN.CENTER)
    add_card(slide, 0.86, 4.22, 5.55, 1.35, fill=WHITE)
    add_text(slide, "Condition A", 1.16, 4.48, 1.7, 0.28, size=19, bold=True, color=RED)
    add_text(slide, "Stripped-context next-API-call baseline.", 2.95, 4.5, 3.05, 0.27, size=16)
    add_card(slide, 6.92, 4.22, 5.55, 1.35, fill=WHITE)
    add_text(slide, "Condition B", 7.22, 4.48, 1.8, 0.28, size=19, bold=True, color=TEAL)
    add_text(slide, "Trajectory-context next-API-call format.", 9.06, 4.5, 2.95, 0.27, size=16)
    add_footer(slide, 3)

    # 4. Setup
    slide = prs.slides.add_slide(blank)
    add_title(slide, "Setup", "Same base model and scoring pipeline; B sees more prompt tokens.")
    rows = [
        ["Component", "Value"],
        ["Model", "Llama 3.1 8B Instruct"],
        ["Fine-tuning", "QLoRA, rank 32, alpha 64, 4-bit"],
        ["Data stream", "API-Bank split into D1-D4"],
        ["Seed", "42"],
        ["Full eval examples", "126, 104, 103, 107"],
        ["Train tokens", "A 1.86M, B 2.32M (+25.1%)"],
    ]
    add_table(slide, rows, 0.86, 1.62, 6.0, 3.7, widths=[2.05, 3.95])
    add_card(slide, 7.48, 1.88, 4.42, 2.74, fill=WHITE)
    add_text(slide, "Scoring", 7.82, 2.16, 3.7, 0.34, size=22, bold=True)
    add_bullets(slide, [
        "API-name accuracy",
        "Exact full-call accuracy",
        "Error buckets for wrong API, wrong args, and malformed outputs"
    ], 7.86, 2.76, 3.55, 1.34, size=17)
    add_footer(slide, 4)

    # 5. Main result
    slide = prs.slides.add_slide(blank)
    add_title(slide, "Main Result", "Trajectory context improves final exact full-call accuracy on every block.")
    add_metric(slide, "39.2%", "A mean exact", 0.92, 1.55, RED)
    add_metric(slide, "56.9%", "B mean exact", 3.02, 1.55, TEAL)
    add_metric(slide, "+17.7", "point gap", 5.12, 1.55, GOLD)
    chart_data = CategoryChartData()
    chart_data.categories = ["D1", "D2", "D3", "D4"]
    chart_data.add_series("Condition A", [35.7, 43.3, 32.0, 45.8])
    chart_data.add_series("Condition B", [57.9, 61.5, 44.7, 63.6])
    chart_shape = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(1.0),
        Inches(3.04),
        Inches(7.0),
        Inches(3.05),
        chart_data,
    )
    chart = chart_shape.chart
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.BOTTOM
    chart.value_axis.maximum_scale = 80
    chart.value_axis.minimum_scale = 0
    chart.value_axis.has_major_gridlines = True
    for series, color in zip(chart.series, [RED, TEAL]):
        series.format.fill.solid()
        series.format.fill.fore_color.rgb = color
        series.format.line.color.rgb = color
    add_card(slide, 8.6, 3.1, 3.5, 2.55, fill=WHITE)
    add_text(slide, "Interpretation", 8.92, 3.38, 2.85, 0.32, size=20, bold=True)
    add_text(slide, "B appears to retain more useful tool-call context, but this does not isolate context from token budget.",
             8.94, 3.9, 2.82, 1.06, size=16, color=NAVY)
    add_footer(slide, 5)

    # 6. Continual matrix
    slide = prs.slides.add_slide(blank)
    add_title(slide, "Continual Evaluation", "Accuracy is measured after each training block, not only at the end.")
    heatmap = FIG_DIR / "full_eval_exact_full_heatmaps_seed42.png"
    add_image_fit(slide, heatmap, 0.72, 1.55, 7.85, 4.85)
    add_card(slide, 8.92, 1.72, 3.42, 3.96, fill=WHITE)
    add_text(slide, "What to notice", 9.24, 2.04, 2.8, 0.33, size=20, bold=True)
    add_bullets(slide, [
        "The comparison uses a full held-out evaluation at each stage.",
        "B's advantage is visible across multiple trained/evaluated block pairs.",
        "The result is encouraging, not definitive."
    ], 9.22, 2.66, 2.72, 1.72, size=16)
    add_footer(slide, 6)

    # 7. Failure analysis
    slide = prs.slides.add_slide(blank)
    add_title(slide, "Failure Analysis", "Trajectory context changes the error mix.")
    rows = [
        ["Metric", "A", "B", "Direction"],
        ["Exact full-call errors", "251", "172", "B lower"],
        ["Wrong API", "102", "12", "B much lower"],
        ["Wrong arguments", "104", "59", "B lower"],
        ["Malformed / no call", "45", "101", "B higher"],
    ]
    add_table(slide, rows, 0.88, 1.62, 6.65, 3.12, widths=[2.7, 1.0, 1.0, 1.95])
    add_card(slide, 8.08, 1.72, 4.05, 3.02, fill=WHITE)
    add_text(slide, "Takeaway", 8.42, 2.05, 3.36, 0.34, size=21, bold=True)
    add_text(slide, "B is much better at choosing the right API, but its longer context can make exact output formatting less stable.",
             8.42, 2.72, 3.22, 1.18, size=18, color=NAVY)
    add_footer(slide, 7)

    # 8. Closing
    slide = prs.slides.add_slide(blank)
    add_title(slide, "Conclusion", "Trajectory supervision is promising, but the current evidence is a pilot.")
    add_card(slide, 0.88, 1.62, 3.65, 3.88, fill=WHITE)
    add_text(slide, "Novelty", 1.2, 1.96, 2.96, 0.34, size=22, bold=True, color=TEAL)
    add_bullets(slide, [
        "A controlled process-proxy comparison for continual API-call learning.",
        "Full matrix evaluation across a sequential tool-use stream."
    ], 1.2, 2.58, 2.8, 1.42, size=17)
    add_card(slide, 4.84, 1.62, 3.65, 3.88, fill=WHITE)
    add_text(slide, "Limits", 5.16, 1.96, 2.96, 0.34, size=22, bold=True, color=RED)
    add_bullets(slide, [
        "Single seed.",
        "B has more tokens.",
        "Synthetic benchmark and next-call framing."
    ], 5.16, 2.58, 2.8, 1.42, size=17)
    add_card(slide, 8.8, 1.62, 3.65, 3.88, fill=WHITE)
    add_text(slide, "Next", 9.12, 1.96, 2.96, 0.34, size=22, bold=True, color=GOLD)
    add_bullets(slide, [
        "Run multiple seeds.",
        "Token-match the conditions.",
        "Add semantic argument scoring."
    ], 9.12, 2.58, 2.8, 1.42, size=17)
    add_text(slide, "Bottom line: keeping observable trajectory context improves tool identity and final exact-call accuracy in this setup.",
             1.18, 6.08, 10.85, 0.44, size=19, bold=True, align=PP_ALIGN.CENTER)
    add_footer(slide, 8)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(OUT)


if __name__ == "__main__":
    build()
