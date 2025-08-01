from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

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

if __name__ == "__main__":
    file_path = "chap04/txt/KCI_FI003103066_without_hf.txt"
    summary = summarize_text(file_path)
    print(summary)

    with open("chap04/txt/summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)