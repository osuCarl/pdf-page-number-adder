import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

def add_page_number(input_pdf, startNumber):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    num_pages = len(reader.pages)

    for i, page in enumerate(reader.pages):
        packet = BytesIO()
        
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)
        # 创建页码, 使用页面自身尺寸
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))
        # 页码从 startNumber 开始
        number = i + startNumber

        print(f"正在处理文件：{input_pdf} 页 {i+1}/{num_pages}: 添加页码 {number}")
        if number % 2 == 1:
            position = (page_width - 50, 35)  # 右下角
        else:
            position = (35, 35)  # 左下角
        print(f"页面尺寸: ({page_width}, {page_height}), position位置：{position}")
        can.drawString(*position, f"- {number} -")  # 页码位置可调整
        can.save()
        packet.seek(0)

        # 叠加页码到原页面
        from PyPDF2 import PdfReader as PR
        overlay = PR(packet)
        page.merge_page(overlay.pages[0])
        writer.add_page(page)
    
    return writer


# pdf_folder = "1-2 每百名学生拥有县级以上骨干教师数/"
# 遍历文件夹中的所有PDF文件并添加页码
# pdf_files= [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

def process_pdfs(pdf_paths):
    split = False
    if len(pdf_paths) < 1:
        print("PDF 列表为空！")
        return
    

    startNumber = 1
    if (split):
        for f in pdf_paths:
            file = f
            out_name = f"numbered_{f}"
            writer = add_page_number(file, startNumber)
            startNumber += len(PdfReader(file).pages)
            with open(out_name, "wb") as f_out:
                writer.write(f_out)
            print(f"已处理 {f}，输出为 {out_name}")

    else:
        merged_file = "merged_output.pdf"
        with open(merged_file, "wb") as f_out:
            writer = PdfWriter()
            for file in pdf_paths:
                added = add_page_number(file, startNumber)
                startNumber += len(PdfReader(file).pages)
                for page in added.pages:
                    writer.add_page(page)
            writer.write(f_out)
        print(f"已生成合并文件 {merged_file}")

