@echo off
call %~dp0\setenv.bat
echo Current Directory: %cd%
cd %PROJECT_DIR%
echo New Current Directory: %cd%
pip install -e .
timeout /t 0.25 >nul
cls
ophrase "What is the past tense of 'write'?" %*
