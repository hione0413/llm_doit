@echo off
echo === 오프라인 Cursor + AI 설정 스크립트 ===

REM Ollama 설치 확인
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo Ollama가 설치되지 않았습니다.
    echo offline_packages 폴더에서 Ollama 설치 파일을 실행하세요.
    pause
    exit /b 1
)

REM 모델 복원
echo 모델 파일 복원 중...
if exist "D:\ollama_backup" (
    xcopy "D:\ollama_backup" "%USERPROFILE%\.ollama" /E /I /H /Y
    echo 모델 복원 완료
) else (
    echo 백업 폴더를 찾을 수 없습니다: D:\ollama_backup
)

REM Cursor 설정 복원
echo Cursor 설정 복원 중...
if exist "D:\cursor_backup" (
    xcopy "D:\cursor_backup" "%APPDATA%\Cursor" /E /I /H /Y
    echo Cursor 설정 복원 완료
) else (
    echo 백업 폴더를 찾을 수 없습니다: D:\cursor_backup
)

REM Ollama 서비스 시작
echo Ollama 서비스 시작 중...
ollama serve

echo === 설정 완료 ===
echo 이제 Cursor를 실행하고 로컬 AI 기능을 사용할 수 있습니다.
pause 