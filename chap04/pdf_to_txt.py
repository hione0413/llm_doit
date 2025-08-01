import pymupdf
import os

pdf_file_path = "chap04/KCI_FI003103066.pdf"
doc = pymupdf.open(pdf_file_path)

full_text = ""

for page in doc:
    text = page.get_text()
    full_text += text

pdf_file_name = os.path.basename(pdf_file_path)
pdf_file_name = os.path.splitext(pdf_file_name)[0]

txt_file_path = f"chap04/txt/{pdf_file_name}.txt"

# Create the txt directory if it doesn't exist
os.makedirs(os.path.dirname(txt_file_path), exist_ok=True)

with open(txt_file_path, "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"PDF 파일이 성공적으로 텍스트 파일로 변환되었습니다: {txt_file_path}")