import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 랭체인 메모리 없이 멀티턴 만들기
st.title("LangChain Simple Chat")

llm = ChatOpenAI(model="gpt-4o-mini")

# 사용자의 메시지를 처리하는 함수
def get_ai_response(messages):
    response = llm.stream(messages)

    for chunk in response:
        yield chunk

# 스트림릿 session_state 에 메시지 저장
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        SystemMessage(content="너는 챗봇이야. 사용자의 질문에 까칠하게 대답해줘."),
        AIMessage("How can I help you today?")
    ]

# 스트림릿 화면에 msg 출력
for msg in st.session_state.messages:
    if msg.content:
        if isinstance(msg, SystemMessage):
            st.write(f"System: {msg.content}")
        elif isinstance(msg, HumanMessage):
            st.write(f"User: {msg.content}")
        elif isinstance(msg, AIMessage):
            st.write(f"AI: {msg.content}")


# 사용자 입력 처리
if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st.session_state.messages.append(HumanMessage(content=prompt))

    response = get_ai_response(st.session_state["messages"])

    result = st.chat_message("ai").write_stream(response)
    st.session_state["messages"].append(AIMessage(content=result))
