@echo off
cd /d "%~dp0"
if "%~1"=="" (
  echo Type your question, then press Enter:
  set /p QUESTION=^> 
) else (
  set "QUESTION=%*"
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\run_llama_cpp_windows.ps1" -Prompt "%QUESTION%"
pause
