from datetime import datetime
import pytz
import yfinance as yf

def get_current_time(timezone: str = "Asia/Seoul"):
    tz = pytz.timezone(timezone)
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    now_timezone = f'{now} {timezone}'
    print(f"Current time: {now_timezone}")

    return now_timezone


def get_yf_stock_info(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info
    print(f"Stock info: {info}")
    return str(info)


def get_yf_stock_history(ticker: str, period: str = "1d"):
    stock = yf.Ticker(ticker)
    history = stock.history(period=period)
    history_md = history.to_markdown()
    print(f"Stock history markdown: {history_md}")
    return history_md


def get_yf_stock_recommendation(ticker: str):
    stock = yf.Ticker(ticker)
    recommendation = stock.recommendations
    recommendations_md = recommendation.to_markdown()
    print(f"Stock recommendation markdown: {recommendations_md}")
    return recommendations_md


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current time",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {"type": "string", "description": "현재 날짜와 시간을 반환할 타임존을 입력하세요. (예: Asia/Seoul)"}
                },
                "required": ["timezone"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_yf_stock_info",
            "description": "해당 종목의 Yahoo Finance 정보를 반환합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Yahoo Finance 정보를 반환할 종목의 티커를 입력하세요. (예: AAPL)"}
                },
                "required": ["ticker"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_yf_stock_history",
            "description": "해당 종목의 Yahoo Finance 주식 가격 정보를 반환합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Yahoo Finance 주식 가격 정보를 반환할 종목의 티커를 입력하세요. (예: AAPL)"},
                    "period": {"type": "string", "description": "주식 가격 정보를 반환할 기간을 입력하세요. (예: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)"}
                },
                "required": ["ticker", "period"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_yf_stock_recommendation",
            "description": "해당 종목의 Yahoo Finance 추천 정보를 반환합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Yahoo Finance 추천 정보를 반환할 종목의 티커를 입력하세요. (예: AAPL)"}
                },
                "required": ["ticker"]
            }
        }
    }
]


if __name__ == "__main__":
    # get_current_time()
    # info = get_yf_stock_info("AAPL")
    history = get_yf_stock_history("AAPL", period="1d")
    print('-----------------')
    recommendation = get_yf_stock_recommendation("AAPL")