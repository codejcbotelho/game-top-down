@echo off
REM Script para compilar e preparar o jogo para distribuição no Windows
REM Autor: Claude
REM Data: %date%

REM Configurações
set NOME_JOGO=game-top-down
set PROJETO_DIR=%cd%
set DIST_DIR=%PROJETO_DIR%\dist
set BUILD_DIR=%PROJETO_DIR%\build

REM Cores para mensagens (Windows 10+)
set VERDE=[92m
set AMARELO=[93m
set VERMELHO=[91m
set AZUL=[94m
set RESET=[0m

echo %AZUL%[BUILD]%RESET% Iniciando build do jogo: %NOME_JOGO%

REM Verificar dependências
echo %AZUL%[BUILD]%RESET% Verificando dependências...

REM Verificar Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo %VERMELHO%[ERRO]%RESET% Python não encontrado. Por favor, instale o Python.
    exit /b 1
)

REM Verificar pip
pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo %VERMELHO%[ERRO]%RESET% pip não encontrado. Por favor, instale o pip.
    exit /b 1
)

REM Verificar PyInstaller
pip show pyinstaller >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo %AMARELO%[AVISO]%RESET% PyInstaller não encontrado. Instalando...
    pip install pyinstaller
    if %ERRORLEVEL% NEQ 0 (
        echo %VERMELHO%[ERRO]%RESET% Falha ao instalar PyInstaller.
        exit /b 1
    )
)

REM Verificar pygame
pip show pygame >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo %AMARELO%[AVISO]%RESET% pygame não encontrado. Instalando...
    pip install pygame
    if %ERRORLEVEL% NEQ 0 (
        echo %VERMELHO%[ERRO]%RESET% Falha ao instalar pygame.
        exit /b 1
    )
)

echo %VERDE%[SUCESSO]%RESET% Todas as dependências estão instaladas.

REM Limpar diretórios de build anteriores
echo %AZUL%[BUILD]%RESET% Limpando diretórios de build anteriores...

if exist "%DIST_DIR%" (
    rmdir /s /q "%DIST_DIR%"
)

if exist "%BUILD_DIR%" (
    rmdir /s /q "%BUILD_DIR%"
)

REM Remover arquivos .pyc e __pycache__
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc >nul 2>&1

echo %VERDE%[SUCESSO]%RESET% Diretórios de build limpos.

REM Verificar arquivos do jogo
echo %AZUL%[BUILD]%RESET% Verificando arquivos do jogo...

python check_game_files.py
if %ERRORLEVEL% NEQ 0 (
    echo %VERMELHO%[ERRO]%RESET% Falha ao verificar arquivos do jogo.
    exit /b 1
)

echo %VERDE%[SUCESSO]%RESET% Arquivos do jogo verificados.

REM Compilar o jogo
echo %AZUL%[BUILD]%RESET% Compilando o jogo...

pyinstaller --name="%NOME_JOGO%" ^
            --onedir ^
            --windowed ^
            --add-data="assets;assets" ^
            --add-data="config;config" ^
            --add-data="maps;maps" ^
            main.py

if %ERRORLEVEL% NEQ 0 (
    echo %VERMELHO%[ERRO]%RESET% Falha ao compilar o jogo.
    exit /b 1
)

echo %VERDE%[SUCESSO]%RESET% Jogo compilado com sucesso.

REM Criar pacote de distribuição
echo %AZUL%[BUILD]%RESET% Criando pacote de distribuição...

set PACOTE_DIR=%DIST_DIR%\%NOME_JOGO%-pacote
mkdir "%PACOTE_DIR%" 2>nul

REM Copiar arquivos para o pacote
xcopy /e /i /y "%DIST_DIR%\%NOME_JOGO%" "%PACOTE_DIR%"
copy README.md "%PACOTE_DIR%" >nul 2>&1
copy LICENSE "%PACOTE_DIR%" >nul 2>&1

REM Criar arquivo de instruções
echo %NOME_JOGO% > "%PACOTE_DIR%\LEIA-ME.txt"
echo ==================== >> "%PACOTE_DIR%\LEIA-ME.txt"
echo. >> "%PACOTE_DIR%\LEIA-ME.txt"
echo Instruções de Instalação: >> "%PACOTE_DIR%\LEIA-ME.txt"
echo 1. Extraia todos os arquivos deste pacote >> "%PACOTE_DIR%\LEIA-ME.txt"
echo 2. Execute o arquivo '%NOME_JOGO%.exe' para iniciar o jogo >> "%PACOTE_DIR%\LEIA-ME.txt"
echo. >> "%PACOTE_DIR%\LEIA-ME.txt"
echo Requisitos: >> "%PACOTE_DIR%\LEIA-ME.txt"
echo - Sistema operacional: Windows >> "%PACOTE_DIR%\LEIA-ME.txt"
echo - Resolução mínima: 800x600 >> "%PACOTE_DIR%\LEIA-ME.txt"
echo. >> "%PACOTE_DIR%\LEIA-ME.txt"
echo Controles: >> "%PACOTE_DIR%\LEIA-ME.txt"
echo - Setas: Movimentação >> "%PACOTE_DIR%\LEIA-ME.txt"
echo - Espaço: Interagir com objetos >> "%PACOTE_DIR%\LEIA-ME.txt"
echo - ESC: Pausar/Menu >> "%PACOTE_DIR%\LEIA-ME.txt"
echo. >> "%PACOTE_DIR%\LEIA-ME.txt"
echo Em caso de problemas, verifique se todos os arquivos foram extraídos corretamente. >> "%PACOTE_DIR%\LEIA-ME.txt"
echo. >> "%PACOTE_DIR%\LEIA-ME.txt"
echo Divirta-se! >> "%PACOTE_DIR%\LEIA-ME.txt"

REM Criar arquivo ZIP do pacote (usando PowerShell)
cd "%DIST_DIR%"
powershell -command "Compress-Archive -Path '%NOME_JOGO%-pacote' -DestinationPath '%NOME_JOGO%-%date:~6,4%%date:~3,2%%date:~0,2%.zip' -Force"

if %ERRORLEVEL% NEQ 0 (
    echo %VERMELHO%[ERRO]%RESET% Falha ao criar pacote ZIP.
    exit /b 1
)

echo %VERDE%[SUCESSO]%RESET% Pacote de distribuição criado em: %DIST_DIR%\%NOME_JOGO%-%date:~6,4%%date:~3,2%%date:~0,2%.zip

REM Finalização
echo %VERDE%[SUCESSO]%RESET% Build concluído com sucesso!
echo %AZUL%[BUILD]%RESET% O jogo está pronto para distribuição em: %DIST_DIR%\%NOME_JOGO%-%date:~6,4%%date:~3,2%%date:~0,2%.zip

pause 