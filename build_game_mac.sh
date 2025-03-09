#!/bin/bash

# Script para compilar e preparar o jogo para distribuição no macOS
# Autor: Claude
# Data: $(date +%d/%m/%Y)

# Cores para mensagens
VERDE='\033[0;32m'
AMARELO='\033[1;33m'
VERMELHO='\033[0;31m'
AZUL='\033[0;34m'
RESET='\033[0m'

# Diretório do projeto
PROJETO_DIR="$(pwd)"
DIST_DIR="$PROJETO_DIR/dist"
BUILD_DIR="$PROJETO_DIR/build"

# Nome do jogo
NOME_JOGO="game-top-down"
APP_NAME="$NOME_JOGO.app"

# Função para exibir mensagens
mensagem() {
    echo -e "${AZUL}[BUILD]${RESET} $1"
}

mensagem_sucesso() {
    echo -e "${VERDE}[SUCESSO]${RESET} $1"
}

mensagem_aviso() {
    echo -e "${AMARELO}[AVISO]${RESET} $1"
}

mensagem_erro() {
    echo -e "${VERMELHO}[ERRO]${RESET} $1"
}

# Função para verificar dependências
verificar_dependencias() {
    mensagem "Verificando dependências..."
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        mensagem_erro "Python 3 não encontrado. Por favor, instale o Python 3."
        exit 1
    fi
    
    # Verificar pip
    if ! command -v pip3 &> /dev/null; then
        mensagem_erro "pip3 não encontrado. Por favor, instale o pip3."
        exit 1
    fi
    
    # Verificar PyInstaller
    if ! pip3 list | grep -q PyInstaller; then
        mensagem_aviso "PyInstaller não encontrado. Instalando..."
        pip3 install pyinstaller
        if [ $? -ne 0 ]; then
            mensagem_erro "Falha ao instalar PyInstaller."
            exit 1
        fi
    fi
    
    # Verificar pygame
    if ! pip3 list | grep -q pygame; then
        mensagem_aviso "pygame não encontrado. Instalando..."
        pip3 install pygame
        if [ $? -ne 0 ]; then
            mensagem_erro "Falha ao instalar pygame."
            exit 1
        fi
    fi
    
    # Verificar create-dmg (opcional)
    if ! command -v create-dmg &> /dev/null; then
        mensagem_aviso "create-dmg não encontrado. Instalando com Homebrew..."
        if command -v brew &> /dev/null; then
            brew install create-dmg
            if [ $? -ne 0 ]; then
                mensagem_aviso "Não foi possível instalar create-dmg. O DMG não será criado."
                CREATE_DMG=false
            else
                CREATE_DMG=true
            fi
        else
            mensagem_aviso "Homebrew não encontrado. O DMG não será criado."
            CREATE_DMG=false
        fi
    else
        CREATE_DMG=true
    fi
    
    mensagem_sucesso "Todas as dependências estão instaladas."
}

# Função para limpar diretórios de build anteriores
limpar_diretorios() {
    mensagem "Limpando diretórios de build anteriores..."
    
    if [ -d "$DIST_DIR" ]; then
        rm -rf "$DIST_DIR"
    fi
    
    if [ -d "$BUILD_DIR" ]; then
        rm -rf "$BUILD_DIR"
    fi
    
    # Remover arquivos .pyc e __pycache__
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -name "*.pyc" -delete
    
    mensagem_sucesso "Diretórios de build limpos."
}

# Função para verificar arquivos do jogo
verificar_arquivos_jogo() {
    mensagem "Verificando arquivos do jogo..."
    
    # Executar o script de verificação
    python3 check_game_files.py
    
    if [ $? -ne 0 ]; then
        mensagem_erro "Falha ao verificar arquivos do jogo."
        exit 1
    fi
    
    mensagem_sucesso "Arquivos do jogo verificados."
}

# Função para compilar o jogo
compilar_jogo() {
    mensagem "Compilando o jogo para macOS..."
    
    # Criar o executável com PyInstaller
    pyinstaller --name="$NOME_JOGO" \
                --onedir \
                --windowed \
                --add-data="assets:assets" \
                --add-data="config:config" \
                --add-data="maps:maps" \
                --icon="assets/images/icon.icns" \
                --osx-bundle-identifier="com.yourgame.$NOME_JOGO" \
                main.py
    
    if [ $? -ne 0 ]; then
        mensagem_erro "Falha ao compilar o jogo."
        exit 1
    fi
    
    mensagem_sucesso "Jogo compilado com sucesso."
}

# Função para criar pacote de distribuição
criar_pacote() {
    mensagem "Criando pacote de distribuição..."
    
    # Criar diretório para o pacote
    PACOTE_DIR="$DIST_DIR/$NOME_JOGO-macOS"
    mkdir -p "$PACOTE_DIR"
    
    # Copiar arquivos para o pacote
    cp -r "$DIST_DIR/$APP_NAME" "$PACOTE_DIR"
    cp README.md "$PACOTE_DIR" 2>/dev/null || :
    cp LICENSE "$PACOTE_DIR" 2>/dev/null || :
    
    # Criar arquivo de instruções
    cat > "$PACOTE_DIR/LEIA-ME.txt" << EOF
$NOME_JOGO para macOS
====================

Instruções de Instalação:
1. Arraste o arquivo '$APP_NAME' para a pasta Aplicativos
2. Clique duas vezes no ícone para iniciar o jogo

Nota: Na primeira execução, pode ser necessário clicar com o botão direito no aplicativo e selecionar "Abrir" para contornar a proteção do Gatekeeper.

Requisitos:
- macOS 10.15 ou superior
- Resolução mínima: 800x600

Controles:
- Setas: Movimentação
- Espaço: Interagir com objetos
- ESC: Pausar/Menu

Divirta-se!
EOF
    
    # Criar arquivo ZIP do pacote
    cd "$DIST_DIR"
    zip -r "$NOME_JOGO-macOS-$(date +%Y%m%d).zip" "$NOME_JOGO-macOS"
    
    if [ $? -ne 0 ]; then
        mensagem_erro "Falha ao criar pacote ZIP."
        exit 1
    fi
    
    mensagem_sucesso "Pacote de distribuição criado em: $DIST_DIR/$NOME_JOGO-macOS-$(date +%Y%m%d).zip"
    
    # Criar DMG se create-dmg estiver disponível
    if [ "$CREATE_DMG" = true ]; then
        mensagem "Criando arquivo DMG..."
        
        create-dmg \
            --volname "$NOME_JOGO" \
            --volicon "assets/images/icon.icns" \
            --window-pos 200 120 \
            --window-size 600 400 \
            --icon "$APP_NAME" 150 190 \
            --app-drop-link 450 190 \
            --no-internet-enable \
            "$DIST_DIR/$NOME_JOGO-macOS-$(date +%Y%m%d).dmg" \
            "$PACOTE_DIR"
        
        if [ $? -ne 0 ]; then
            mensagem_aviso "Falha ao criar arquivo DMG. O pacote ZIP ainda está disponível."
        else
            mensagem_sucesso "Arquivo DMG criado em: $DIST_DIR/$NOME_JOGO-macOS-$(date +%Y%m%d).dmg"
        fi
    fi
}

# Função principal
main() {
    mensagem "Iniciando build do jogo para macOS: $NOME_JOGO"
    
    verificar_dependencias
    limpar_diretorios
    verificar_arquivos_jogo
    compilar_jogo
    criar_pacote
    
    mensagem_sucesso "Build concluído com sucesso!"
    mensagem "O jogo está pronto para distribuição em: $DIST_DIR/$NOME_JOGO-macOS-$(date +%Y%m%d).zip"
    
    if [ "$CREATE_DMG" = true ]; then
        mensagem "Também disponível como DMG em: $DIST_DIR/$NOME_JOGO-macOS-$(date +%Y%m%d).dmg"
    fi
}

# Executar função principal
main 