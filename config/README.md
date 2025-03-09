# Documentação de Configuração de Itens

Este documento explica como utilizar o arquivo de configuração `items.json` para definir os diferentes tipos de objetos, inimigos, itens e elementos de terreno no jogo.

## Estrutura do Arquivo

O arquivo `items.json` contém três seções principais:

1. **tile_types**: Define todos os tipos de tiles e objetos do jogo
2. **animation_types**: Lista os tipos de animações disponíveis
3. **enemy_behaviors**: Lista os comportamentos possíveis para inimigos

## Tipos de Tiles (tile_types)

Cada tipo de tile é identificado por um número único que será usado nos arquivos de mapa. A estrutura de cada definição é a seguinte:

```json
"ID": {
  "name": "Nome do Item",
  "type": "tipo_do_item",
  "collision": true/false,
  "image": "caminho/para/imagem.png",
  "details": {
    // Propriedades específicas do tipo
  }
}
```

### Campos Comuns

- **name**: Nome descritivo do item
- **type**: Categoria do item (terreno, objeto, item, inimigo, npc, transição)
- **collision**: Se o jogador colide com este item (true/false)
- **image**: Caminho para a imagem do item (sempre 32x32 pixels)
- **details**: Propriedades específicas do tipo de item

### Tipos de Itens

#### Terreno (0-6)
- **0**: Vazio (tile base)
- **1**: Parede (com colisão)
- **5**: Água (com colisão e animação)
- **6**: Grama Alta (sem colisão, animação ao caminhar)

#### Objetos (2-12)
- **2**: Porta (interativa)
- **3**: Árvore (com colisão)
- **4**: Arbusto (com colisão, destrutível)
- **9**: Baú (interativo, contém itens)
- **11**: Porta Trancada (requer chave)
- **12**: Placa (interativa, mostra mensagem)

#### Itens Coletáveis (7-10)
- **7**: Moeda (coletável, valor)
- **8**: Poção de Vida (coletável, restaura vida)
- **10**: Chave (coletável, abre portas)

#### Inimigos (20-22)
- **20**: Slime (movimento aleatório)
- **21**: Morcego (persegue o jogador)
- **22**: Esqueleto (patrulha área)

#### NPCs (30-31)
- **30**: Aldeão (diálogo)
- **31**: Comerciante (diálogo, loja)

#### Transições (40-42)
- **40**: Escada para Baixo
- **41**: Escada para Cima
- **42**: Portal (animado)

## Propriedades Específicas

### Terreno
- **walkable**: Se o jogador pode caminhar sobre (true/false)
- **destructible**: Se pode ser destruído (true/false)

### Objetos
- **interactive**: Se o jogador pode interagir (true/false)
- **requires_key**: Se requer uma chave para interagir (true/false)
- **key_type**: ID do item de chave necessário
- **drops**: Lista de itens que podem ser obtidos

### Itens
- **collectible**: Se pode ser coletado (true/false)
- **value**: Valor do item (para moedas)
- **health_restore**: Quantidade de vida restaurada
- **opens**: Lista de objetos que este item pode abrir

### Inimigos
- **health**: Pontos de vida
- **damage**: Dano causado ao jogador
- **speed**: Velocidade de movimento
- **behavior**: Tipo de comportamento
- **detection_radius**: Raio de detecção (para perseguição)
- **patrol_radius**: Raio de patrulha
- **drops**: Itens que podem ser obtidos ao derrotar

### NPCs
- **dialog**: Texto de diálogo
- **shop**: Se é uma loja (true/false)
- **items_for_sale**: Lista de itens à venda

### Transições
- **target_map**: ID do mapa de destino
- **target_x**: Posição X de destino
- **target_y**: Posição Y de destino

## Animações

As animações são definidas pelos seguintes parâmetros:

- **animation**: Tipo de animação (none, ambient, on_interaction, on_walk, movement, idle)
- **animation_frames**: Número de quadros na animação
- **animation_speed**: Velocidade da animação (em segundos por quadro)

## Convenções de Nomeação de Arquivos

Para as imagens dos sprites, siga estas convenções:

- **Sprites estáticos**: `nome_do_item.png`
- **Sprites animados**: `nome_do_item_0.png`, `nome_do_item_1.png`, etc.

Todas as imagens devem ter exatamente 32x32 pixels.

## Exemplo de Uso em Mapas

Nos arquivos de mapa JSON, você pode usar os IDs numéricos para representar os diferentes tipos de tiles:

```json
"data": [
  [1, 1, 1, 1, 1],
  [1, 0, 7, 0, 1],
  [1, 0, 2, 0, 1],
  [1, 20, 0, 0, 1],
  [1, 1, 1, 1, 1]
]
```

Este exemplo representa:
- Paredes (1) ao redor
- Uma moeda (7) no centro superior
- Uma porta (2) no meio
- Um slime (20) no canto inferior esquerdo
- Espaços vazios (0) no resto do mapa 