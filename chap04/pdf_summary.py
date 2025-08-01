from openai import OpenAI
from dotenv import load_dotenv
import os
import pymupdf

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def pdf_to_txt(pdf_file_path: str):
    doc = pymupdf.open(pdf_file_path)

    header_height = 80
    footer_height = 80

    full_text = ""

    for page in doc:
        rect = page.rect

        header = page.get_text(clip=(0, 0, rect.width, header_height))
        footer = page.get_text(clip=(0, rect.height - footer_height, rect.width, rect.height))

        text = page.get_text(clip=(0, header_height, rect.width, rect.height - footer_height))

        full_text += text + '\n--------------------------------------------\n'

    pdf_file_name = os.path.basename(pdf_file_path)
    pdf_file_name = os.path.splitext(pdf_file_name)[0]

    txt_file_path = f"chap04/txt/{pdf_file_name}_summary.txt"

    # Create the txt directory if it doesn't exist
    os.makedirs(os.path.dirname(txt_file_path), exist_ok=True)

    with open(txt_file_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    return txt_file_path


def summarize_text(file_path: str):
    client = OpenAI(api_key=api_key)

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    system_prompt = f'''
        너는 다음 글을 요약하는 봇이다. 아래 글을 읽고, 저자의 문제 인식과 주장을 파악하고, 주요 내용을 요약하라.

        작성해야 하는 포맷은 다음과 같다.

        # 제목

        ## 저자의 문제 인식 및 주장 (15문장 이내)

        ## 저자 소개


        ==================== 이하 텍스트 ====================

        { text }
    '''

    print(system_prompt)
    print("--------------------------------")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        messages=[
            {"role": "system", "content": system_prompt},
        ]
    )

    return response.choices[0].message.content

def summarize_pdf(pdf_file_path: str):
    txt_file_path = pdf_to_txt(pdf_file_path)
    summary = summarize_text(txt_file_path)
    
    with open(txt_file_path, "w", encoding="utf-8") as f:
        f.write(summary)

if __name__ == "__main__":
    pdf_file_path = 'chap04/KCI_FI003103066.pdf'
    summarize_pdf(pdf_file_path, "chap04/txt/KCI_FI003103066_summary.txt")