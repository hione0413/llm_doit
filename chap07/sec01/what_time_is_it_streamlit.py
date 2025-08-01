from gpt_functions import tools, get_current_time
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import streamlit as st

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


st.title("Chatbot, What time is it?")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant that can answer questions and help with tasks."},
    ]

for message in st.session_state.messages:
    if message["role"] == "user" or message["role"] == "assistant":
        st.chat_message(message["role"]).write(message["content"])
        
if user_input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    ai_response = get_ai_response(st.session_state.messages, tools)
    ai_message = ai_response.choices[0].message
    print(f"Assistant: {ai_message}")

    tool_calls = ai_message.tool_calls
    if tool_calls: # tool_calls 가 있을 경우
        for tool_call in tool_calls:
            tool_name = tool_call.function.name # 실행해야 한다고 판단한 함수명 받기
            tool_call_id = tool_call.id     # 함수 아이디 받기
            
            arguments = json.loads(tool_call.function.arguments)

            print(f"Tool name: {tool_name}")

            if tool_name == "get_current_time":
                timezone = arguments["timezone"]
                st.session_state.messages.append({
                    "role": "function", # role 을 function 으로 설정
                    "tool_call_id": tool_call_id,
                    "name": tool_name,
                    "content": get_current_time(timezone=timezone), # 함수 실행 결과를 content 로 설정
                })

        # messages.append(ai_message)

        st.session_state.messages.append({"role": "system", "content": "이제 주어진 결과를 바탕으로 답변할 차례다."})
    
        ai_response = get_ai_response(st.session_state.messages, tools=tools)
        ai_message = ai_response.choices[0].message

        # print(f"Assistant: {ai_message}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_message.content,
    })

    print(f"Assistant: {ai_message.content}")
    st.chat_message("assistant").write(ai_message.content)
    