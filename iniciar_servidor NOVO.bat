@echo off
setlocal
chcp 65001 >nul

echo Iniciando servidor de Gestao de Documentos...

REM === Paths (ajuste se precisar) ===
set "VENV_DIR=C:\Users\rennan.monteiro\Desktop\gerenciamento documento novo\ambiente"
set "PROJ_DIR=C:\Users\rennan.monteiro\Desktop\gerenciamento documento novo\documentos"

REM === Ativar ambiente virtual ===
call "%VENV_DIR%\Scripts\activate"
if errorlevel 1 (
    echo [ERRO] Falha ao ativar o ambiente virtual em "%VENV_DIR%".
    pause
    exit /b 1
)

REM === Ir para a pasta do manage.py ===
cd /d "%PROJ_DIR%"
if errorlevel 1 (
    echo [ERRO] Nao foi possivel acessar "%PROJ_DIR%".
    pause
    exit /b 1
)

REM === Coletar estaticos (necessario para producao) ===
echo Coletando arquivos estaticos...
python manage.py collectstatic --noinput
if errorlevel 1 (
    echo [ERRO] collectstatic falhou. Verifique STATIC_ROOT/permissions.
    pause
    exit /b 1
)

REM (Opcional) Aplicar migracoes
REM echo Aplicando migracoes...
REM python manage.py migrate --noinput
REM if errorlevel 1 (
REM     echo [ERRO] migrate falhou.
REM     pause
REM     exit /b 1
REM )

REM === Subir servidor com waitress (usa documentos.wsgi) ===
echo Subindo servidor com waitress na porta 5000...
python -c "from waitress import serve; from documentos.wsgi import application; serve(application, host='0.0.0.0', port=5000, threads=50)"
if errorlevel 1 (
    echo [ERRO] Falha ao iniciar o waitress.
    pause
    exit /b 1
)

echo Servidor finalizado.
pause
