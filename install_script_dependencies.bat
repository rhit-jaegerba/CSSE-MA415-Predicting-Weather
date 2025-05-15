@echo off
cd /d "%~dp0"
python.exe -m pip install --upgrade pip
pip install json
pip install requests