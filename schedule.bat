@echo off
title SayangAI - Auto Start
echo Menjalankan Ollama Serve...
start /min cmd /c "ollama serve"
timeout /t 2 >nul
echo Menjalankan AI Agent...
start "" "D:\Ragah Mujahidin\kampus\git\ai-agent-sederhana\schedule.exe"
exit