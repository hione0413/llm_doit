@echo off
echo === 온라인 백업 스크립트 ===

REM 백업 폴더 생성
set BACKUP_DIR=D:\offline_packages
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

echo 백업 폴더: %BACKUP_DIR%

REM 1. Ollama 모델 다운로드
echo 1. Ollama 모델 다운로드 중...
ollama pull deepseek-coder:6.7b
ollama pull codellama:7b
ollama pull starcoder:7b

REM 2. 모델 파일 백업
echo 2. 모델 파일 백업 중...
if exist "%USERPROFILE%\.ollama" (
    xcopy "%USERPROFILE%\.ollama" "%BACKUP_DIR%\ollama_models" /E /I /H /Y
    echo 모델 백업 완료
)

REM 3. Cursor 설정 백업
echo 3. Cursor 설정 백업 중...
if exist "%APPDATA%\Cursor" (
    xcopy "%APPDATA%\Cursor" "%BACKUP_DIR%\cursor_settings" /E /I /H /Y
    echo Cursor 설정 백업 완료
)

REM 4. Ollama 설치 파일 다운로드
echo 4. Ollama 설치 파일 다운로드 중...
powershell -Command "Invoke-WebRequest -Uri 'https://ollama.ai/download/windows' -OutFile '%BACKUP_DIR%\ollama_installer.exe'"

REM 5. 설정 파일 생성
echo 5. 설정 파일 생성 중...
echo {> "%BACKUP_DIR%\cursor_settings.json"
echo   "ai.local.enabled": true,>> "%BACKUP_DIR%\cursor_settings.json"
echo   "ai.local.endpoint": "http://localhost:11434",>> "%BACKUP_DIR%\cursor_settings.json"
echo   "ai.local.model": "deepseek-coder:6.7b",>> "%BACKUP_DIR%\cursor_settings.json"
echo   "ai.local.provider": "ollama">> "%BACKUP_DIR%\cursor_settings.json"
echo }>> "%BACKUP_DIR%\cursor_settings.json"

REM 6. README 파일 생성
echo 6. README 파일 생성 중...
echo 오프라인 설치 가이드 > "%BACKUP_DIR%\README.txt"
echo. >> "%BACKUP_DIR%\README.txt"
echo 1. ollama_installer.exe 실행하여 Ollama 설치 >> "%BACKUP_DIR%\README.txt"
echo 2. offline_setup.bat 실행하여 설정 복원 >> "%BACKUP_DIR%\README.txt"
echo 3. Cursor 실행 >> "%BACKUP_DIR%\README.txt"

echo === 백업 완료 ===
echo 백업 위치: %BACKUP_DIR%
echo 이 폴더를 오프라인 환경으로 복사하세요.
pause 