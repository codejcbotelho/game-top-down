# Jogo Top-Down em Python

Este é um jogo estilo top-down simples criado com Python e Pygame. O jogo apresenta um personagem que pode ser controlado pelo jogador em um mapa 2D visto de cima.

## Características

- Movimentação em quatro direções (cima, baixo, esquerda, direita)
- Sistema de colisão com paredes e obstáculos
- Mapa 2D renderizado com tiles
- Controles simples e intuitivos

## Requisitos

- Python 3.6+
- Pygame 2.5.2

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
- ESC: Sair do jogo

## Estrutura do Projeto

```
game-top-down/
├── assets/            # Recursos do jogo
│   ├── images/        # Imagens e sprites
│   └── sounds/        # Efeitos sonoros e músicas
├── main.py            # Ponto de entrada do jogo
├── game.py            # Classe principal do jogo
├── player.py          # Classe do jogador
├── map.py             # Classe do mapa
├── requirements.txt   # Dependências
└── README.md          # Este arquivo
```

## Expandindo o Jogo

Algumas ideias para expandir este projeto base:
- Adicionar sprites e animações para o personagem
- Implementar inimigos e combate
- Adicionar sistema de níveis ou missões
- Incluir efeitos sonoros e música de fundo
- Implementar um sistema de inventário

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes. 