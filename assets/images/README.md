# Imagens do Jogo

Este diretório contém todas as imagens utilizadas no jogo, organizadas em subdiretórios por tipo.

## Estrutura de Diretórios

- **tiles/**: Elementos de terreno (chão, paredes, água, etc.)
- **objects/**: Objetos interativos (portas, árvores, baús, etc.)
- **items/**: Itens coletáveis (moedas, poções, chaves, etc.)
- **enemies/**: Inimigos (slime, morcego, esqueleto, etc.)
- **npcs/**: Personagens não-jogáveis (aldeão, comerciante, etc.)

## Convenções de Nomenclatura

- **Sprites estáticos**: `nome_do_item.png`
- **Sprites animados**: `nome_do_item_0.png`, `nome_do_item_1.png`, etc.

Todas as imagens têm exatamente 32x32 pixels, conforme definido no arquivo de configuração `config/items.json`.

## Imagens Disponíveis

### Tiles
- `empty.png`: Tile vazio (ID: 0)
- `wall.png`: Parede (ID: 1)
- `water_[0-3].png`: Água animada (ID: 5)
- `tall_grass_[0-2].png`: Grama alta animada (ID: 6)

### Objetos
- `door.png` e `door_[0-3].png`: Porta e sua animação (ID: 2)
- `tree.png` e `tree_[0-1].png`: Árvore e sua animação (ID: 3)
- `bush.png`: Arbusto (ID: 4)
- `chest.png` e `chest_[0-2].png`: Baú e sua animação (ID: 9)
- `door_locked.png` e `door_locked_[0-4].png`: Porta trancada e sua animação (ID: 11)
- `sign.png`: Placa (ID: 12)
- `stairs_down.png`: Escada para baixo (ID: 40)
- `stairs_up.png`: Escada para cima (ID: 41)
- `portal.png` e `portal_[0-7].png`: Portal e sua animação (ID: 42)

### Itens
- `coin.png` e `coin_[0-5].png`: Moeda e sua animação (ID: 7)
- `health_potion.png` e `health_potion_[0-3].png`: Poção de vida e sua animação (ID: 8)
- `key.png` e `key_[0-3].png`: Chave e sua animação (ID: 10)

### Inimigos
- `slime.png` e `slime_[0-3].png`: Slime e sua animação (ID: 20)
- `bat.png` e `bat_[0-3].png`: Morcego e sua animação (ID: 21)
- `skeleton.png` e `skeleton_[0-5].png`: Esqueleto e sua animação (ID: 22)

### NPCs
- `villager.png` e `villager_[0-1].png`: Aldeão e sua animação (ID: 30)
- `merchant.png` e `merchant_[0-1].png`: Comerciante e sua animação (ID: 31)

## Como Usar as Imagens

Para usar estas imagens no jogo, você deve referenciar o caminho correto no arquivo de configuração `config/items.json`. Por exemplo:

```json
"7": {
  "name": "Moeda",
  "type": "item",
  "collision": false,
  "image": "items/coin.png",
  "details": {
    "collectible": true,
    "value": 1,
    "animation": "ambient",
    "animation_frames": 6,
    "animation_speed": 0.1
  }
}
```

Para imagens animadas, o jogo carregará automaticamente todos os quadros da animação com base no número de quadros especificado em `animation_frames`.

## Personalizando as Imagens

Você pode substituir qualquer uma dessas imagens por suas próprias versões, desde que:
1. Mantenha o mesmo nome de arquivo
2. Mantenha a dimensão de 32x32 pixels
3. Use o formato PNG com transparência (se necessário)

Para gerar novas imagens, você pode usar o script `generate_images.py` na raiz do projeto. 