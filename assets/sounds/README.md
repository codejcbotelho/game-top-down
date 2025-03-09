# Sons do Jogo

Este diretório contém todos os arquivos de áudio utilizados no jogo, organizados em subdiretórios por tipo.

## Estrutura de Diretórios

- **music/**: Trilhas sonoras para os mapas
- **effects/**: Efeitos sonoros para interações

## Trilhas Sonoras

Cada mapa pode ter sua própria trilha sonora, definida no arquivo JSON do mapa através da propriedade `soundtrack`. O jogo irá automaticamente:

1. Tocar a trilha sonora quando o jogador entrar no mapa
2. Manter a mesma trilha tocando se o próximo mapa usar a mesma música
3. Mudar para a nova trilha sonora quando o jogador entrar em um mapa com música diferente

### Trilhas Sonoras Disponíveis

- `music/forest.mp3`: Trilha sonora para o mapa da Floresta
- `music/cave.mp3`: Trilha sonora para o mapa da Caverna
- `music/desert.mp3`: Trilha sonora para o mapa do Deserto
- `music/lake.mp3`: Trilha sonora para o mapa do Lago

## Efeitos Sonoros

Os efeitos sonoros são tocados durante interações com objetos, inimigos ou elementos do ambiente. Eles são definidos no arquivo de configuração `config/items.json` através da propriedade `interaction_sound` dentro de `details`.

### Efeitos Sonoros Disponíveis

- `effects/door.wav`: Som de porta abrindo
- `effects/door_locked.wav`: Som de porta trancada
- `effects/chest.wav`: Som de baú abrindo
- `effects/coin.wav`: Som de coleta de moeda
- `effects/potion.wav`: Som de coleta de poção
- `effects/key.wav`: Som de coleta de chave
- `effects/bush.wav`: Som de interação com arbusto
- `effects/grass.wav`: Som de caminhada na grama alta
- `effects/sign.wav`: Som de leitura de placa

## Como Adicionar Novos Sons

Para adicionar novos sons ao jogo:

1. Coloque o arquivo de áudio no diretório apropriado (`music/` ou `effects/`)
2. Para trilhas sonoras, adicione a propriedade `soundtrack` ao arquivo JSON do mapa:
   ```json
   {
     "name": "Novo Mapa",
     "soundtrack": "music/nome_do_arquivo.mp3",
     ...
   }
   ```

3. Para efeitos sonoros, adicione a propriedade `interaction_sound` ao item no arquivo `config/items.json`:
   ```json
   "42": {
     "name": "Novo Item",
     "type": "objeto",
     "details": {
       "interactive": true,
       "interaction_sound": "effects/nome_do_arquivo.wav",
       ...
     }
   }
   ```

## Formatos Suportados

O jogo suporta os seguintes formatos de áudio:
- MP3 (.mp3) - Recomendado para músicas
- WAV (.wav) - Recomendado para efeitos sonoros
- OGG (.ogg) - Alternativa para músicas e efeitos

## Observações

- Todos os arquivos de áudio devem ser colocados nos diretórios apropriados
- Recomenda-se usar arquivos MP3 para músicas (melhor compressão) e WAV para efeitos sonoros (melhor qualidade)
- Os caminhos para os arquivos de áudio são relativos ao diretório `assets/sounds/` 