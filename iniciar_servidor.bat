@echo off
echo Iniciando servidor gestão de documentos...

REM Ativar ambiente virtual (está uma pasta acima do manage.py)
call "C:\Users\rennan.monteiro\Desktop\gerenciamento documento novo\ambiente\Scripts\activate"

REM Mudar para a pasta onde está o manage.py (nível certo do projeto)
cd /d "C:\Users\rennan.monteiro\Desktop\gerenciamento documento novo\documentos"

REM Rodar o servidor via waitress usando o módulo wsgi
python -c "from waitress import serve; from documentos.wsgi import application; serve(application, host='0.0.0.0', port=5000, threads=50)"

pause
