#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import shutil
import pygame

def check_directory(path):
    """Verifica se um diretório existe e o cria se necessário"""
    if not os.path.exists(path):
        print(f"Criando diretório: {path}")
        os.makedirs(path, exist_ok=True)
        return False
    return True

def check_json_file(path, default_content=None):
    """Verifica se um arquivo JSON existe e é válido"""
    if not os.path.exists(path):
        print(f"Arquivo não encontrado: {path}")
        if default_content:
            print(f"Criando arquivo padrão: {path}")
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(default_content, f, ensure_ascii=False, indent=2)
            return False
        return False
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True
    except json.JSONDecodeError as e:
        print(f"Erro no arquivo JSON {path}: {e}")
        if default_content:
            backup_path = f"{path}.bak"
            print(f"Fazendo backup do arquivo corrompido para: {backup_path}")
            shutil.copy2(path, backup_path)
            
            print(f"Substituindo por arquivo padrão: {path}")
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(default_content, f, ensure_ascii=False, indent=2)
        return False

def check_audio_file(path, file_type='.mp3'):
    """Verifica se um arquivo de áudio existe"""
    if not os.path.exists(path):
        print(f"Aviso: Arquivo de áudio não encontrado: {path}")
        # Apenas cria o diretório, mas não o arquivo
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return False
    
    return True

def check_image_file(path, size=(32, 32), color=(200, 200, 200), item_type=None):
    """Verifica se um arquivo de imagem existe e cria uma imagem colorida se necessário"""
    if not os.path.exists(path):
        print(f"Aviso: Arquivo de imagem não encontrado: {path}")
        
        # Cria o diretório se necessário
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Define a cor com base no tipo de item
        if item_type == "terreno":
            color = (50, 150, 50)  # Verde para terreno
        elif item_type == "objeto":
            color = (150, 75, 0)   # Marrom para objetos
        elif item_type == "item":
            color = (255, 215, 0)  # Dourado para itens
        elif item_type == "inimigo":
            color = (200, 0, 0)    # Vermelho para inimigos
        elif item_type == "npc":
            color = (0, 100, 200)  # Azul para NPCs
        elif item_type == "transição":
            color = (150, 50, 200) # Roxo para transições
        
        # Cria uma imagem colorida
        pygame.init()
        img = pygame.Surface(size)
        img.fill(color)
        
        # Adiciona um padrão para identificação
        pygame.draw.rect(img, (0, 0, 0), (4, 4, size[0]-8, size[1]-8), 2)
        
        # Salva a imagem
        pygame.image.save(img, path)
        
        print(f"Criada imagem colorida para {path}: {color}")
        return False
    
    return True

def check_game_files():
    """Verifica e corrige os arquivos do jogo"""
    print("Verificando arquivos do jogo...")
    
    # Inicializa o pygame para poder criar imagens
    pygame.init()
    
    # Verifica diretórios principais
    check_directory("maps")
    check_directory("config")
    check_directory("assets")
    check_directory("assets/images")
    check_directory("assets/images/tiles")
    check_directory("assets/images/objects")
    check_directory("assets/images/items")
    check_directory("assets/images/enemies")
    check_directory("assets/images/npcs")
    check_directory("assets/sounds")
    check_directory("assets/sounds/music")
    check_directory("assets/sounds/effects")
    
    # Verifica arquivos de configuração
    default_items = {
        "tile_types": {
            "0": {
                "name": "Vazio",
                "type": "terreno",
                "collision": False,
                "image": "tiles/empty.png",
                "details": {
                    "walkable": True
                }
            },
            "1": {
                "name": "Parede",
                "type": "terreno",
                "collision": True,
                "image": "tiles/wall.png",
                "details": {
                    "walkable": False,
                    "destructible": False
                }
            }
        }
    }
    
    # Carrega a configuração de itens para verificar as imagens
    items_config = default_items
    if check_json_file("config/items.json", default_items):
        try:
            with open("config/items.json", "r", encoding="utf-8") as f:
                items_config = json.load(f)
        except:
            pass
    
    # Verifica mapas
    default_map = {
        "name": "Mapa Padrão",
        "width": 25,
        "height": 19,
        "tile_size": 32,
        "background_color": [50, 150, 50],
        "wall_color": [100, 100, 100],
        "data": [[1 if x == 0 or x == 24 or y == 0 or y == 18 else 0 for x in range(25)] for y in range(19)],
        "portals": [],
        "objects": [],
        "enemies": [],
        "edge_transitions": {"left": None, "right": None, "top": None, "bottom": None}
    }
    check_json_file("maps/map1.json", default_map)
    
    # Verifica arquivos de áudio
    check_audio_file("assets/sounds/music/forest.mp3")
    check_audio_file("assets/sounds/music/cave.mp3")
    check_audio_file("assets/sounds/music/desert.mp3")
    check_audio_file("assets/sounds/music/lake.mp3")
    
    check_audio_file("assets/sounds/effects/door.wav", '.wav')
    check_audio_file("assets/sounds/effects/door_locked.wav", '.wav')
    check_audio_file("assets/sounds/effects/chest.wav", '.wav')
    check_audio_file("assets/sounds/effects/coin.wav", '.wav')
    check_audio_file("assets/sounds/effects/potion.wav", '.wav')
    check_audio_file("assets/sounds/effects/key.wav", '.wav')
    check_audio_file("assets/sounds/effects/bush.wav", '.wav')
    check_audio_file("assets/sounds/effects/grass.wav", '.wav')
    check_audio_file("assets/sounds/effects/sign.wav", '.wav')
    
    # Verifica imagens básicas
    check_image_file("assets/images/tiles/empty.png", color=(50, 150, 50), item_type="terreno")
    check_image_file("assets/images/tiles/wall.png", color=(100, 100, 100), item_type="terreno")
    
    # Verifica imagens de todos os itens na configuração
    for tile_id, tile_info in items_config.get("tile_types", {}).items():
        image_path = tile_info.get("image", "")
        if image_path:
            full_path = os.path.join("assets/images", image_path)
            item_type = tile_info.get("type", "")
            check_image_file(full_path, item_type=item_type)
    
    print("Verificação concluída!")

if __name__ == "__main__":
    check_game_files()
    print("Pressione Enter para sair...")
    input() 