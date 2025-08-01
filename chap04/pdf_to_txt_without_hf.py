import pymupdf
import os

pdf_file_path = "chap04/KCI_FI003103066.pdf"
doc = pymupdf.open(pdf_file_path)

header_height = 80
footer_height = 80

full_text = ""

for page in doc:
    # 페이지 크기 가져오기
    rect = page.rect

    header = page.get_text(clip=(0, 0, rect.width, header_height))
    footer = page.get_text(clip=(0, rect.height - footer_height, rect.width, rect.height))

    # 헤더와 푸터 제거
    text = page.get_text(clip=(0, header_height, rect.width, rect.height - footer_height))

    full_text += text + '\n--------------------------------------------\n'

pdf_file_name = os.path.basename(pdf_file_path)
pdf_file_name = os.path.splitext(pdf_file_name)[0]

txt_file_path = f"chap04/txt/{pdf_file_name}_without_hf.txt"

# Create the txt directory if it doesn't exist
os.makedirs(os.path.dirname(txt_file_path), exist_ok=True)

with open(txt_file_path, "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"PDF 파일이 성공적으로 텍스트 파일로 변환되었습니다: {txt_file_path}")