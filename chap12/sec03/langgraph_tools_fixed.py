#!/usr/bin/env python3
"""
LangGraph Tools with corrected node naming
"""

# 환경 변수 설정 (경고 해결을 위해)
import os
os.environ['USER_AGENT'] = 'LangGraph-Tools-Bot/1.0'

# 언어 모델 선정하기
from langchain_openai import ChatOpenAI

# 모델 초기화
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.01)

# 상태 설정하기
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    State 클래스는 TypedDict 를 상속 받습니다.

    속성:
        messages (Annotated[list[str], add_messages]): 메시지들은 'list'타입을 가집니다.
        'add_messages' 함수는 이 상태 키가 어떻게 업데이트 되어야 하는지를 정의합니다.
        (이 경우, 메시지를 덮어쓰는 대신 리스트에 추가합니다)
    """
    messages: Annotated[list[str], add_messages]

# StateGraph 클래스를 사용하여 State 타입의 그래프 생성
graph_builder = StateGraph(State)

# 도구 등록하기
from langchain_core.tools import tool
from datetime import datetime
import pytz
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

import bs4
from langchain_community.document_loaders import WebBaseLoader

# 도구 함수 정의
@tool
def get_current_time(timezone: str, localtion: str) -> str:
    """현재 시각을 반환하는 함수"""
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return f"현재 시각: {now.strftime('%Y-%m-%d %H:%M:%S')} {timezone}({localtion})"
    except pytz.UnknownTimeZoneError:
        return f"알 수 없는 타임존: {timezone}"

@tool
def get_web_search(query: str, search_period: str='m') -> str:
    """
    웹 검색을 수행하는 함수.

    Args:
        query (str): 검색할 키워드
        search_period (str): 검색 기간 (m: 1개월, d: 1일, h: 1시간)

    Returns:
        str: 검색 결과
    """

    wrapper = DuckDuckGoSearchAPIWrapper(
        # region="kr-kr",
        time=search_period,
    )

    print('\n---------- WEB SEARCH ----------\n')
    print(f'검색 키워드: {query}')
    print(f'검색 기간: {search_period}')

    search = DuckDuckGoSearchResults(
        api_wrapper=wrapper,
        results_separator=';\n'
    )

    searched = search.invoke(query)

    for i, result in enumerate(searched.split(';\n')):
        print(f'{i + 1}. {result}')

    return searched

# 도구 바인딩
tools = [get_current_time, get_web_search]

# 언어 모델에 .bind_tools 로 사용할 도구 연결하기
model_with_tools = model.bind_tools(tools) # GPT 언어 모델에 도구 연결

def generate(state: State):
    """
    주어진 상태를 기반으로 챗봇의 응답 메시지를 생성합니다.

    매개변수:
        state (State): 현재 대화 상태를 나타내는 객체로, 이전 메시지들이 포함되어 있습니다.

    반환값:
        dict: 모델이 생성한 응답 메시지를 포함하는 딕셔너리.
            형식은 {"messages": [응답 메시지]} 입니다.
    """
    return {"messages": [model_with_tools.invoke(state["messages"])]}

graph_builder.add_node("generate", generate)

# 도구를 사용하는 노드 클래스 생성하기
import json
from langchain_core.messages import ToolMessage

class BasicToolNode:
    """
    도구를 실행하는 노드 클래스입니다. 마지막 AIMessage 에서 요청된 도구를 실행합니다.
    Attributes:
        tools_by_name (dict): 도구 이름을 키로 하고 도구 객체를 값으로 가지는 사전입니다.
    Methods:
        __init__: 도구 객체들의 리스트를 받아서 초기화합니다.
        __call__: 입력 메시지를 받아서 도구를 싱행하고 결과 메시지를 반환합니다.
    """
    """A node that runs the tools requested by the last AIMessage"""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            # inputs 에 messages 가 있으면 messages 를 가져오고 없으면 빈 리스트 가져오기
            message = messages[-1]
        else:
            raise ValueError("No message found in inputs")
        outputs = []

        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": messages + outputs}

tool_node = BasicToolNode(tools)
# 노드 이름을 "tools"로 변경하여 route_tools 함수와 일치시킴
graph_builder.add_node("tools", tool_node)

# 라우터 설정하기
# 언어 모델이 도구 사용 여부를 판단하도록 라우터 설정하기
def route_tools(state: State):
    """
    마지막 메시지에 도구 호출이 있는 경우 ToolNode 로 라우팅하고,
    그렇지 않은 경우 끝으로 라우팅하기 위해 conditional_edges 에서 사용합니다.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No message found in inputs: {state}")

    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END

graph_builder.add_edge(START, "generate")

# generate 에서 route_tools 함수 결과에 따라 분기
graph_builder.add_conditional_edges(
    "generate", 
    route_tools,
    {"tools": "tools", END: END}
)

# 도구가 호출될 때마다 다음 단계를 결정하기 위해 챗봇으로 돌아감
graph_builder.add_edge("tools", "generate")
graph = graph_builder.compile()

print("그래프가 성공적으로 컴파일되었습니다!")
print("USER_AGENT 환경 변수가 설정되어 경고가 발생하지 않습니다.") 