from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

llm = ChatOpenAI(model="gpt-4o-mini")

messages = [
    SystemMessage(content="너는 챗봇이야. 사용자의 질문에 대답해줘."),
]

while True:
    user_input = input("사용자: ")
    if user_input.lower() == "종료":
        break
    messages.append(HumanMessage(content=user_input))
    ai_response = llm.invoke(messages)
    messages.append(ai_response)
    print(f"AI: {ai_response.content}")