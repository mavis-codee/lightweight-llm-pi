@echo off
cd /d "%~dp0"
echo Starting Lightweight LLM chat...
echo Wait for the ^> prompt, then type your question.
echo Type /exit to quit.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\run_llama_cpp_windows.ps1" -Chat
pause
