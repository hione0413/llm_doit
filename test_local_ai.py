import requests
import time
import json

def test_local_ai(model_name, prompt):
    """로컬 AI 모델 테스트"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        return response.json()["response"]
    except Exception as e:
        return f"오류: {e}"

def compare_models():
    """모델 성능 비교"""
    
    test_prompts = [
        "Python으로 간단한 계산기 함수를 작성해줘",
        "다음 코드의 버그를 찾아줘: def add(a, b): return a - b",
        "React 컴포넌트를 TypeScript로 작성해줘",
        "이 코드를 최적화해줘: for i in range(1000): print(i)"
    ]
    
    models = [
        "deepseek-coder:6.7b",
        "codellama:7b", 
        "starcoder:7b"
    ]
    
    print("=== 로컬 AI 모델 성능 테스트 ===\n")
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"테스트 {i}: {prompt}")
        print("-" * 50)
        
        for model in models:
            print(f"\n[{model}]")
            start_time = time.time()
            result = test_local_ai(model, prompt)
            end_time = time.time()
            
            print(f"응답 시간: {end_time - start_time:.2f}초")
            print(f"결과: {result[:200]}...")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    print("로컬 AI 모델 테스트를 시작합니다...")
    print("Ollama가 실행 중인지 확인하세요!")
    compare_models() 