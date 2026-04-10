@echo off
set SCRIPT_DIR=%~dp0..
python -m venv "%SCRIPT_DIR%\.venv"
call "%SCRIPT_DIR%\.venv\Scripts\activate.bat"
pip install Pillow
