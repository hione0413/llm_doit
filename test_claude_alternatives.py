import requests
import time
import json

def test_model(model_name, prompt):
    """모델 테스트"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        return response.json()["response"]
    except Exception as e:
        return f"오류: {e}"

def compare_with_claude():
    """Claude 대안 모델들 비교"""
    
    # Claude와 유사한 작업들
    test_prompts = [
        "다음 코드를 리팩토링해줘: def calculate_sum(numbers): total = 0; for num in numbers: total += num; return total",
        "Python으로 REST API를 FastAPI로 구현하는 방법을 설명해줘",
        "다음 에러를 해결해줘: 'list' object has no attribute 'append'",
        "React에서 상태 관리를 위한 최적의 방법을 제안해줘"
    ]
    
    # Claude 대안 모델들
    models = [
        "llama3.1:8b",
        "mistral:7b", 
        "qwen2.5:7b",
        "phi3:3.8b"
    ]
    
    print("=== Claude 3.5 Sonnet 대안 모델 테스트 ===\n")
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"테스트 {i}: {prompt}")
        print("-" * 60)
        
        for model in models:
            print(f"\n[{model}]")
            start_time = time.time()
            result = test_model(model, prompt)
            end_time = time.time()
            
            print(f"응답 시간: {end_time - start_time:.2f}초")
            print(f"결과: {result[:300]}...")
        
        print("\n" + "="*80 + "\n")

def test_coding_specific():
    """코딩 특화 테스트"""
    
    coding_tasks = [
        "Python으로 이진 검색 알고리즘을 구현해줘",
        "JavaScript에서 Promise를 사용한 비동기 함수를 작성해줘",
        "SQL에서 JOIN을 사용한 복잡한 쿼리를 작성해줘",
        "HTML/CSS로 반응형 카드 레이아웃을 만들어줘"
    ]
    
    coding_models = [
        "deepseek-coder:6.7b",
        "codellama:7b",
        "starcoder:7b"
    ]
    
    print("=== 코딩 특화 모델 테스트 ===\n")
    
    for i, task in enumerate(coding_tasks, 1):
        print(f"코딩 테스트 {i}: {task}")
        print("-" * 50)
        
        for model in coding_models:
            print(f"\n[{model}]")
            start_time = time.time()
            result = test_model(model, task)
            end_time = time.time()
            
            print(f"응답 시간: {end_time - start_time:.2f}초")
            print(f"결과: {result[:250]}...")
        
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    print("Claude 대안 모델 테스트를 시작합니다...")
    print("Ollama가 실행 중인지 확인하세요!")
    
    # 일반 AI 모델 테스트
    compare_with_claude()
    
    # 코딩 특화 모델 테스트
    test_coding_specific() 