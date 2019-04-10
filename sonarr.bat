@echo off
cd /d %~dp0

:: Qbit completion
timeout /t 10 

:: Execute code
python notify.py "350166" "Goblin Slayer" "09"

pause