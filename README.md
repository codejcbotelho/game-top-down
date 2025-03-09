# Jogo Top-Down em Python

Este é um jogo estilo top-down simples criado com Python e Pygame. O jogo apresenta um personagem que pode ser controlado pelo jogador em um mapa 2D visto de cima, com sistema de múltiplos mapas e transições entre eles.

## Características

- Tela inicial com menu
- Seleção de personagem com diferentes atributos
- Movimentação em quatro direções (cima, baixo, esquerda, direita)
- Sistema de colisão com paredes e obstáculos
- Mapa 2D renderizado com tiles
- Sistema de múltiplos mapas com transições
- Interação com portas e objetos
- Menu de pausa
- Controles simples e intuitivos

## Requisitos

- Python 3.6+
- Pygame 2.6.1

## Instalação

1. Clone este repositório ou baixe os arquivos
2. Instale as dependências:

```
pip install -r requirements.txt
```

## Como Jogar

Execute o arquivo principal do jogo:

```
python main.py
```

### Controles

- Setas direcionais ou WASD: Movimentar o personagem
- Tecla E: Interagir com portas e objetos
- ESC: Pausar o jogo / Voltar ao menu anterior
- ENTER: Confirmar seleção nos menus

### Personagens

O jogo oferece três tipos de personagens para escolher:
- **Guerreiro**: Velocidade média, representado pela cor vermelha
- **Arqueiro**: Velocidade alta, representado pela cor verde
- **Mago**: Velocidade baixa, representado pela cor azul

### Sistema de Mapas

O jogo possui 4 mapas diferentes:
1. **Floresta**: Mapa inicial com vegetação
2. **Caverna**: Um ambiente subterrâneo escuro
3. **Deserto**: Área árida com pouca vegetação
4. **Lago**: Região com um grande corpo d'água

Você pode mudar de mapa de duas formas:
- **Transição por borda**: Ao chegar na extremidade de um mapa, você será transportado para o mapa adjacente
- **Portas**: Interagindo com portas (tiles marrons) usando a tecla E

## Estrutura do Projeto

```
game-top-down/
├── assets/                # Recursos do jogo
│   ├── images/            # Imagens e sprites
│   └── sounds/            # Efeitos sonoros e músicas
├── maps/                  # Arquivos JSON dos mapas
│   ├── map1.json          # Mapa da Floresta
│   ├── map2.json          # Mapa da Caverna
│   ├── map3.json          # Mapa do Deserto
│   └── map4.json          # Mapa do Lago
├── main.py                # Ponto de entrada do jogo
├── game.py                # Classe principal do jogo
├── player.py              # Classe do jogador
├── map.py                 # Classe do mapa
├── game_state.py          # Gerenciador de estados do jogo
├── title_screen.py        # Tela de título
├── character_select.py    # Tela de seleção de personagem
├── pause_screen.py        # Tela de pausa
├── requirements.txt       # Dependências
└── README.md              # Este arquivo
```

## Personalização dos Mapas

Os mapas são definidos em arquivos JSON na pasta `maps/`. Cada arquivo contém:
- Dimensões e propriedades visuais do mapa
- Matriz de dados representando os tiles (0 = vazio, 1 = parede, 2 = porta)
- Definição de portais e suas conexões
- Configuração de transições pelas bordas

Você pode editar esses arquivos para criar seus próprios mapas e conexões.

## Expandindo o Jogo

Algumas ideias para expandir este projeto base:
- Adicionar sprites e animações para o personagem
- Implementar inimigos e combate
- Adicionar sistema de níveis ou missões
- Incluir efeitos sonoros e música de fundo
- Implementar um sistema de inventário

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes. 