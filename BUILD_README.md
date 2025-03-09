# Instruções de Build do Jogo

Este documento explica como compilar o jogo para diferentes sistemas operacionais.

## Requisitos Gerais

- Python 3.6 ou superior
- pip (gerenciador de pacotes do Python)
- pygame
- PyInstaller

## Scripts de Build Disponíveis

Existem três scripts de build disponíveis, um para cada sistema operacional:

1. `build_game.sh` - Para Linux/Unix
2. `build_game_mac.sh` - Para macOS
3. `build_game.bat` - Para Windows

## Como Usar

### No Linux/Unix

```bash
# Torne o script executável (se ainda não estiver)
chmod +x build_game.sh

# Execute o script
./build_game.sh
```

### No macOS

```bash
# Torne o script executável (se ainda não estiver)
chmod +x build_game_mac.sh

# Execute o script
./build_game_mac.sh
```

Para criar um arquivo DMG, você precisará do `create-dmg`. O script tentará instalá-lo automaticamente usando o Homebrew, mas você pode instalá-lo manualmente:

```bash
brew install create-dmg
```

### No Windows

Basta clicar duas vezes no arquivo `build_game.bat` ou executá-lo a partir do Prompt de Comando:

```cmd
build_game.bat
```

## O Que os Scripts Fazem

Cada script realiza as seguintes operações:

1. Verifica se todas as dependências necessárias estão instaladas
2. Limpa diretórios de build anteriores
3. Verifica e corrige arquivos do jogo usando `check_game_files.py`
4. Compila o jogo usando PyInstaller
5. Cria um pacote de distribuição (ZIP e, no caso do macOS, opcionalmente um DMG)

## Saída

Após a execução bem-sucedida, você encontrará:

- No Linux/Unix: `dist/game-top-down-YYYYMMDD.zip`
- No macOS: `dist/game-top-down-macOS-YYYYMMDD.zip` (e opcionalmente um arquivo DMG)
- No Windows: `dist\game-top-down-YYYYMMDD.zip`

## Solução de Problemas

### Erro de Permissão no Linux/macOS

Se você receber um erro de permissão ao tentar executar os scripts, torne-os executáveis:

```bash
chmod +x build_game.sh build_game_mac.sh
```

### Dependências Ausentes

Os scripts tentarão instalar automaticamente as dependências necessárias (PyInstaller e pygame). Se isso falhar, você pode instalá-las manualmente:

```bash
# No Linux/macOS
pip3 install pygame pyinstaller

# No Windows
pip install pygame pyinstaller
```

### Erro ao Criar DMG no macOS

Se o script não conseguir criar o arquivo DMG, verifique se o `create-dmg` está instalado:

```bash
brew install create-dmg
```

### Arquivos de Jogo Ausentes

Se o script reportar arquivos de jogo ausentes, execute o verificador de arquivos manualmente:

```bash
python3 check_game_files.py  # Linux/macOS
python check_game_files.py   # Windows
```

## Personalização

Você pode personalizar os scripts editando as variáveis no início de cada arquivo:

- `NOME_JOGO`: Nome do jogo (e do executável gerado)
- `PROJETO_DIR`: Diretório do projeto (por padrão, o diretório atual)
- `DIST_DIR`: Diretório onde os arquivos de distribuição serão criados
- `BUILD_DIR`: Diretório onde os arquivos temporários de build serão criados 