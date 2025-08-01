from gpt_functions import tools, get_current_time
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_response(messages, tools=None) -> str:
    print(f"Sending request to OpenAI API...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
    )
    print(f"Received response from OpenAI API. {response}")
    return response

messages = [
    {"role": "system", "content": "You are a helpful assistant that can answer questions and help with tasks."},
]

while True:
    user_input = input("사용자: ")

    if user_input == 'exit':
        break

    messages.append({"role": "user", "content": user_input})

    ai_response = get_ai_response(messages, tools)
    ai_message = ai_response.choices[0].message
    print(f"Assistant: {ai_message}")

    tool_calls = ai_message.tool_calls
    if tool_calls: # tool_calls 가 있을 경우
        for tool_call in tool_calls:
            tool_name = tool_call.function.name # 실행해야 한다고 판단한 함수명 받기
            tool_call_id = tool_call.id     # 함수 아이디 받기
            
            arguments = json.loads(tool_call.function.arguments)
            timezone = arguments["timezone"]

            print(f"Tool name: {tool_name}")
            print(f"Tool call id: {tool_call_id}")
            print(f"Arguments: {arguments}")
            print(f"Timezone: {timezone}")

            if tool_name == "get_current_time":
                messages.append({
                    "role": "function", # role 을 function 으로 설정
                    "tool_call_id": tool_call_id,
                    "name": tool_name,
                    "content": get_current_time(timezone=timezone), # 함수 실행 결과를 content 로 설정
                })

        # messages.append(ai_message)

        messages.append({"role": "system", "content": "이제 주어진 결과를 바탕으로 답변할 차례다."})
    
        ai_response = get_ai_response(messages, tools=tools)
        ai_message = ai_response.choices[0].message

        print(f"Assistant: {ai_message}")

    # print(f"Assistant: {ai_message.content}")
    