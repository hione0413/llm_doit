@echo off
echo Setting up Speaker Diarization Environment...

REM Activate virtual environment if it exists
if exist "..\.venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "..\.venv\Scripts\activate.bat"
) else (
    echo Virtual environment not found. Please create one first.
    pause
    exit /b 1
)

echo Installing missing packages...
pip install huggingface_hub[hf_xet]
pip install hf_xet
pip install numpy==1.26.4

echo Setting environment variables...
set HF_HUB_DISABLE_SYMLINKS_WARNING=1

echo.
echo Setup complete! You can now run the speaker diarization script.
echo.
echo To run the fixed version:
echo python speaker_diarization_fixed.py
echo.
pause 