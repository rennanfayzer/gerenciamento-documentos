@echo off
REM ativa seu virtualenv, se precisar:
call "C:\Users\rennan.monteiro\Desktop\gerenciamento documento novo\ambiente\Scripts\activate.bat"

REM roda o script Python
python "%~dp0\list_static.py"

pause
