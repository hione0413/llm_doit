import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

st.title("LangChain Simple Chat")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        SystemMessage(content="너는 챗봇이야. 사용자의 질문에 까칠하게 대답해줘.")
    ]

# 세션별 대화 기록을 저장할 딕셔너리 대신 session_state 사용
if "store" not in st.session_state:
    st.session_state["store"] = {}


def get_session_history(session_id: str):
    if session_id not in st.session_state["store"]:
        st.session_state["store"][session_id] = InMemoryChatMessageHistory()
    return st.session_state["store"][session_id]

llm = ChatOpenAI(model="gpt-4o-mini")

# LLM 과 대화 기록을 자동으로 연결
# 새로운 메시지가 들어오면 자동으로 히스토리에 추가, AI 응답 생성 시 이전 대화 컨텍스트를 자동으로 포함
with_message_history = RunnableWithMessageHistory(llm, get_session_history)

config = {"configurable": {"session_id": "abc01"}}

for msg in st.session_state.messages:
    if msg:
        if isinstance(msg, SystemMessage):
            st.write(f"System: {msg.content}")
        elif isinstance(msg, HumanMessage):
            st.write(f"User: {msg.content}")
        elif isinstance(msg, AIMessage):
            st.write(f"AI: {msg.content}")

if prompt := st.chat_input():
    print('user:'  , prompt)
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    response = with_message_history.stream(
        [HumanMessage(content=prompt)],
        config=config
    )

    ai_response_bucket = None

    with st.chat_message("ai").empty():
        for r in response:
            if ai_response_bucket is None:
                ai_response_bucket = r
            else:
                ai_response_bucket += r
            print(r.content, end="")
            st.markdown(ai_response_bucket.content)

    msg = ai_response_bucket.content
    st.session_state.messages.append(ai_response_bucket)
    # st.chat_message("ai").write(msg) <- invoke 방식일 때 씀. stream 일 때는 반복문 안에서 markdown 으로 출력
    print('ai:'  , msg)




