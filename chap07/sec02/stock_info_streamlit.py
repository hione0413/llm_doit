from gpt_functions import tools, get_current_time, get_yf_stock_info, get_yf_stock_history, get_yf_stock_recommendation
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import streamlit as st
from collections import defaultdict

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def tool_list_to_tool_obj(tools):
    tool_calls_dict = defaultdict(lambda: {"id": None, "function": {"arguments": "", "name": None}, "type": None})

    for tool_call in tools:
        print(f"[tool_list_to_tool_obj] Tool call: {tool_call}")
        # id 가 None 이 아닌 경우 설정
        if tool_call.id is not None:
            tool_calls_dict[tool_call.index]["id"] = tool_call.id

        # 함수 이름이 None이 아닌 경우 설정
        if tool_call.function.name is not None:
            tool_calls_dict[tool_call.index]["function"]["name"] = tool_call.function.name

        # 인자 추가
        tool_calls_dict[tool_call.index]["function"]["arguments"] += tool_call.function.arguments

        # 타입이 None 이 아닌 경우 설정
        if tool_call.type is not None:
            tool_calls_dict[tool_call.index]["type"] = tool_call.type
        
    # 딕셔너리를 리스트로 변환
    tool_calls_list = list(tool_calls_dict.values())

    return {"tool_calls": tool_calls_list} # 반환
    # def tool_list_to_tool_obj end
    

def get_ai_response(messages, tools=None, stream=True) -> str:
    print(f"Sending request to OpenAI API...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        stream=stream, # stream=True 로 설정하면 메시지를 조금씩 받을 수 있음
        messages=messages,
        tools=tools,
    )

    if stream:
        for chunk in response:
            yield chunk # 생성된 응답의 내용을 yield로 순차적으로 반환
        else:
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

    # 메세지 조금씩 받는 내용 로깅
    content = ""
    tool_calls = None
    tool_calls_chunk = []

    with st.chat_message("assistant").empty(): # 스트림릿 챗 메시지 초기화
        for chunk in ai_response:
            # print(chunk)
            content_chunk = chunk.choices[0].delta.content
            if content_chunk:
                print(f"{content_chunk}", end="")
                content += content_chunk
                st.markdown(content) # 스트림릿 챗 메시지에 마크다운으로 출력

            if chunk.choices[0].delta.tool_calls:
                tool_calls_chunk += chunk.choices[0].delta.tool_calls

    print(f"Tool calls: {tool_calls_chunk}")
    tool_obj = tool_list_to_tool_obj(tool_calls_chunk)

    if tool_obj is not None:
        tool_calls = tool_obj["tool_calls"]

        if len(tool_calls) > 0: # 만약 tool_calls 가 존재하면, st.write 로 tool_calls 내용 출력
            print(f"Tool calls: {tool_calls}")
            # tool_calls 에서 function 정보만 모아서 출력
            tool_call_message = [tool_call["function"] for tool_call in tool_calls]
            st.write(tool_call_message)

    print('\n=================================')
    print(f"Assistant: {content}")

    # print('\n================================= Tool calls chunk')
    # for tool_call_chunk in tool_calls_chunk:
    #     print(f"Tool call: {tool_call_chunk}")
    # 위로 이동
    # tool_obj = tool_list_to_tool_obj(tool_calls_chunk)
    # tool_calls = tool_obj["tool_calls"]
    # print(f"Tool calls: {tool_calls}")

    # GPT 가 결과를 stream 으로 반환하게 되므로 기존과 구조가 다름
    # 즉, api_response.choices[0].message 는 구조상 사용할 수 없음
    # ai_message = ai_response.choices[0].message
    # print(f"Assistant: {ai_message}")

    # tool_calls = ai_message.tool_calls

    if tool_calls: # tool_calls 가 있을 경우
        for tool_call in tool_calls:
            # 기존 Stream 형식으로 받기 전에는 아래와 같이 받았음
            # tool_name = tool_call.function.name # 실행해야 한다고 판단한 함수명 받기
            # tool_call_id = tool_call.id     # 함수 아이디 받기
            # arguments = json.loads(tool_call.function.arguments)

            # 문자열을 딕셔너리로 변환, 즉 딕셔너리 형태에서 받기
            tool_name = tool_call["function"]["name"]
            tool_call_id = tool_call["id"]
            arguments = json.loads(tool_call["function"]["arguments"])

            print(f"Tool name: {tool_name}")

            if tool_name == "get_current_time":
                timezone = arguments["timezone"]
                function_result = get_current_time(timezone=timezone)
            elif tool_name == "get_yf_stock_info":
                ticker = arguments["ticker"]
                function_result = get_yf_stock_info(ticker=ticker)
            elif tool_name == "get_yf_stock_history":
                ticker = arguments["ticker"]
                period = arguments["period"]
                function_result = get_yf_stock_history(ticker=ticker, period=period)
            elif tool_name == "get_yf_stock_recommendation":
                ticker = arguments["ticker"]
                function_result = get_yf_stock_recommendation(ticker=ticker)
                
            st.session_state.messages.append({
                "role": "function",
                "tool_call_id": tool_call_id,
                "name": tool_name,
                "content": function_result,
            })

        # messages.append(ai_message)

        st.session_state.messages.append({"role": "system", "content": "이제 주어진 결과를 바탕으로 답변할 차례다."})
    
        ai_response = get_ai_response(st.session_state.messages, tools=tools)
        # 여기도 steam 형태로 받도록 수정
        # ai_message = ai_response.choices[0].message
        content = ""
        with st.chat_message("assistant").empty():
            for chunk in ai_response:
                content_chunk = chunk.choices[0].delta.content
                if content_chunk:
                    print(f"{content_chunk}", end="")
                    content += content_chunk
                    st.markdown(content) # 스트림릿 챗 메시지에 markdown 으로 출력

        # print(f"Assistant: {ai_message}")

    st.session_state.messages.append({
        "role": "assistant",
        # "content": ai_message.content,
        "content": content,
    })

    print(f"AI: {content}")

    # 위에서 with 문으로 이미 뿌렸으니까. 필요없어짐
    # st.chat_message("assistant").write(ai_message.content)
    