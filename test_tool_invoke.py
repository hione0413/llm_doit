from langchain_core.tools import tool
from datetime import datetime
import pytz

# 일반 함수
def normal_get_time(timezone: str = "Asia/Seoul", location: str = "서울") -> str:
    tz = pytz.timezone(timezone)
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    return f"{location}({timezone})의 현재 시각은 {now} 입니다."

# @tool 데코레이터 적용된 함수
@tool
def tool_get_time(timezone: str = "Asia/Seoul", location: str = "서울") -> str:
    tz = pytz.timezone(timezone)
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    return f"{location}({timezone})의 현재 시각은 {now} 입니다."

print("=== 일반 함수 실행 ===")
# 일반 함수는 직접 호출
result1 = normal_get_time(timezone="Asia/Seoul", location="부산")
print(f"일반 함수 결과: {result1}")

print("\n=== Tool 객체 실행 ===")
# Tool 객체는 .invoke() 메서드 사용
args = {'timezone': 'Asia/Seoul', 'location': '부산'}
result2 = tool_get_time.invoke(args)
print(f"Tool 객체 결과: {result2}")

print("\n=== 타입 확인 ===")
print(f"일반 함수 타입: {type(normal_get_time)}")
print(f"Tool 객체 타입: {type(tool_get_time)}")

print("\n=== 사용 가능한 메서드 확인 ===")
print(f"Tool 객체의 메서드들: {[method for method in dir(tool_get_time) if not method.startswith('_')]}") 