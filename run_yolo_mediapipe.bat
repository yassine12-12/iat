@echo off
REM Activate the virtual environment and run the YOLO+MediaPipe script
call .venv\Scripts\activate.bat
python src/yolo_mediapipe_test.py
pause
             