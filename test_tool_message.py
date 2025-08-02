from langchain_core.tools import tool
from datetime import datetime
import pytz

@tool
def get_current_time(timezone: str = "Asia/Seoul", location: str = "서울") -> str:
    tz = pytz.timezone(timezone)
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    return f"{location}({timezone})의 현재 시각은 {now} 입니다."

print("=== Tool.invoke() 결과 확인 ===")
args = {'timezone': 'Asia/Seoul', 'location': '부산'}

# invoke() 실행
result = get_current_time.invoke(args)

print(f"결과 타입: {type(result)}")
print(f"결과 내용: {result}")
print(f"결과의 속성들: {dir(result)}")

print("\n=== 메시지 타입 확인 ===")
from langchain_core.messages import ToolMessage, HumanMessage, AIMessage

print(f"ToolMessage 타입: {type(ToolMessage(content='test'))}")
print(f"HumanMessage 타입: {type(HumanMessage(content='test'))}")
print(f"AIMessage 타입: {type(AIMessage(content='test'))}")

print("\n=== 결론 ===")
print("invoke()는 ToolMessage 객체를 반환합니다.")
print("단순한 문자열이 아니라 LangChain 메시지 객체입니다.")
print("따라서 messages.append()에 바로 추가할 수 있습니다.") 