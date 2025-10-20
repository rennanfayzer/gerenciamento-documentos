@echo off
echo Iniciando servidor gest�o de documentos...

REM Ativar ambiente virtual (est� uma pasta acima do manage.py)
call "C:\Users\rennan.monteiro\Desktop\gerenciamento documento novo\ambiente\Scripts\activate"

REM Mudar para a pasta onde est� o manage.py (n�vel certo do projeto)
cd /d "C:\Users\rennan.monteiro\Desktop\gerenciamento documento novo\documentos"

REM Rodar o servidor via waitress usando o m�dulo wsgi
python -c "from waitress import serve; from documentos.wsgi import application; serve(application, host='0.0.0.0', port=5000, threads=50)"

pause
