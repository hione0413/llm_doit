from langchain_core.tools import tool
from datetime import datetime
import pytz

@tool
def get_current_time(timezone: str = "Asia/Seoul", location: str = "서울") -> str:
    tz = pytz.timezone(timezone)
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    result = f"{location}({timezone})의 현재 시각은 {now} 입니다."
    print(f"함수 실행됨: {result}")
    return result

print("=== 1단계: Tool 객체 생성 ===")
print(f"get_current_time 타입: {type(get_current_time)}")

print("\n=== 2단계: invoke() 실행 ===")
args = {'timezone': 'Asia/Seoul', 'location': '부산'}
print(f"전달할 인자: {args}")

# invoke() 실행 - 이것만으로는 AI에게 전달되지 않음
result = get_current_time.invoke(args)
print(f"invoke() 결과: {result}")

print("\n=== 3단계: 결과 확인 ===")
print("invoke()는 단순히 함수를 실행하고 결과를 반환할 뿐입니다.")
print("AI에게 자동으로 전달되지 않습니다.")
print("개발자가 수동으로 메시지에 추가해야 합니다.")

print("\n=== 4단계: 일반 함수 호출과 비교 ===")
def normal_func(timezone: str, location: str) -> str:
    tz = pytz.timezone(timezone)
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    return f"{location}({timezone})의 현재 시각은 {now} 입니다."

# 일반 함수 호출
normal_result = normal_func(timezone="Asia/Seoul", location="부산")
print(f"일반 함수 결과: {normal_result}")

print("\n=== 결론 ===")
print("invoke()는 일반 함수 호출과 거의 같습니다.")
print("다만 Tool 객체의 표준 인터페이스로 실행하는 것뿐입니다.") 