from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0.9, # 언어의 무작위성 0(안정) ~ 1(창의적)
    messages=[
        {"role": "system", "content": "너는 유치원생이야. 유치원생처럼 답변해 줘"},
        {"role": "user", "content": "참새"},
        {"role": "assistant", "content": "쨱쨱"},
        {"role": "user", "content": "오리"},
        {"role": "assistant", "content": "꽥꽥"},
        {"role": "user", "content": "호랑이"},
    ]
)

print(response)

print('-------------')
print(response.choices[0].message.content)