@echo off
cd /d %~dp0

:: Qbit completion
timeout /t 10 

:: Execute code
py -3.5 run.py %*

exit