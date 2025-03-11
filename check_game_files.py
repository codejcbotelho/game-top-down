#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import pygame
from utils import get_asset_path, ensure_dir_exists, get_resource_path

def check_directory(path):
    """Verifica se um diretório existe e o cria se necessário"""
    full_path = get_asset_path(*path.split('/'))
    if not os.path.exists(full_path):
        print(f"Criando diretório: {full_path}")
        os.makedirs(full_path, exist_ok=True)
    return full_path

def check_json_file(path, default_content):
    """Verifica se um arquivo JSON existe e o cria com conteúdo padrão se necessário"""
    full_path = get_asset_path(*path.split('/'))
    if not os.path.exists(full_path):
        print(f"Criando arquivo JSON: {full_path}")
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(default_content, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao criar arquivo JSON {full_path}: {e}")
    return full_path

def check_audio_file(path, extension='.mp3'):
    """Verifica se um arquivo de áudio existe e cria um arquivo vazio se necessário"""
    full_path = get_asset_path(*path.split('/'))
    if not os.path.exists(full_path):
        print(f"Aviso: Arquivo de áudio ausente: {full_path}")
        # Não cria arquivos de áudio vazios, apenas avisa
    return full_path

def check_image_file(path, color=(255, 255, 255), item_type=""):
    """Verifica se uma imagem existe e cria uma imagem padrão se necessário"""
    full_path = get_asset_path(*path.split('/'))
    if not os.path.exists(full_path):
        print(f"Criando imagem padrão: {full_path}")
        img = pygame.Surface((32, 32))
        img.fill(color)
        
        # Adiciona um texto com o tipo do item
        if item_type:
            try:
                font = pygame.font.SysFont("Arial", 12)
                text = font.render(item_type[:8], True, (0, 0, 0))
                text_rect = text.get_rect(center=(16, 16))
                img.blit(text, text_rect)
            except:
                # Se não conseguir renderizar texto, desenha um padrão
                pygame.draw.rect(img, (0, 0, 0), (4, 4, 24, 24), 2)
        
        pygame.image.save(img, full_path)
    return full_path

def check_all_files():
    """Verifica e cria todos os arquivos necessários"""
    # Inicializa o pygame para poder criar imagens
    pygame.init()
    pygame.display.set_mode((100, 100))  # Cria uma janela mínima para permitir carregar imagens
    
    # Verifica diretórios
    check_directory("assets/images")
    check_directory("assets/images/tiles")
    check_directory("assets/images/objects")
    check_directory("assets/images/items")
    check_directory("assets/images/enemies")
    check_directory("assets/images/npcs")
    check_directory("assets/sounds")
    check_directory("assets/sounds/music")
    check_directory("assets/sounds/effects")
    check_directory("assets/maps")
    check_directory("assets/config")
    
    # Mapa padrão com uma porta funcional
    default_map = {
        "name": "Floresta Inicial",
        "width": 25,
        "height": 19,
        "tile_size": 32,
        "background_color": [50, 150, 50],
        "wall_color": [100, 100, 100],
        "data": [
            [1] * 25,  # Primeira linha toda com paredes
            *[[1] + [0] * 23 + [1] for _ in range(8)],  # 8 linhas com paredes nas bordas
            [1] + [0] * 11 + [2] + [0] * 11 + [1],  # Linha do meio com porta
            *[[1] + [0] * 23 + [1] for _ in range(8)],  # 8 linhas com paredes nas bordas
            [1] * 25  # Última linha toda com paredes
        ],
        "portals": [
            {
                "x": 12,
                "y": 9,
                "target_map": "map2",
                "target_x": 12,
                "target_y": 17
            }
        ],
        "objects": [
            {
                "id": 12,  # Placa
                "x": 10,
                "y": 9,
                "details": {
                    "message": "Use a tecla E para interagir com a porta"
                }
            }
        ],
        "enemies": [],
        "edge_transitions": {
            "north": None,
            "south": None,
            "east": None,
            "west": None
        },
        "soundtrack": "music/forest.mp3"
    }
    
    # Mapa 2 (destino da porta)
    map2 = {
        "name": "Caverna",
        "width": 25,
        "height": 19,
        "tile_size": 32,
        "background_color": [80, 80, 80],
        "wall_color": [60, 60, 60],
        "data": [
            [1] * 25,  # Primeira linha toda com paredes
            *[[1] + [0] * 23 + [1] for _ in range(16)],  # 16 linhas com paredes nas bordas
            [1] + [0] * 11 + [2] + [0] * 11 + [1],  # Linha com porta
            [1] * 25  # Última linha toda com paredes
        ],
        "portals": [
            {
                "x": 12,
                "y": 17,
                "target_map": "map1",
                "target_x": 12,
                "target_y": 9
            }
        ],
        "objects": [
            {
                "id": 12,  # Placa
                "x": 14,
                "y": 17,
                "details": {
                    "message": "Use a tecla E para voltar à Floresta"
                }
            }
        ],
        "enemies": [],
        "edge_transitions": {
            "north": None,
            "south": None,
            "east": None,
            "west": None
        },
        "soundtrack": "music/cave.mp3"
    }
    
    # Configuração de itens
    default_items = {
        "tile_types": {
            "0": {
                "name": "Vazio",
                "type": "terreno",
                "collision": False,
                "image": "tiles/empty.png"
            },
            "1": {
                "name": "Parede",
                "type": "terreno",
                "collision": True,
                "image": "tiles/wall.png"
            },
            "2": {
                "name": "Porta",
                "type": "objeto",
                "collision": False,
                "image": "objects/door.png",
                "details": {
                    "interactive": True,
                    "interaction_sound": "effects/door.wav"
                }
            },
            "12": {
                "name": "Placa",
                "type": "objeto",
                "collision": False,
                "image": "objects/sign.png",
                "details": {
                    "interactive": True,
                    "interaction_sound": "effects/sign.wav"
                }
            }
        }
    }
    
    # Verifica arquivos JSON
    check_json_file("assets/maps/map1.json", default_map)
    check_json_file("assets/maps/map2.json", map2)
    check_json_file("assets/config/items.json", default_items)
    
    # Verifica arquivos de áudio
    check_audio_file("assets/sounds/music/forest.mp3")
    check_audio_file("assets/sounds/music/cave.mp3")
    check_audio_file("assets/sounds/effects/door.wav", '.wav')
    check_audio_file("assets/sounds/effects/sign.wav", '.wav')
    
    # Verifica imagens básicas
    check_image_file("assets/images/tiles/empty.png", color=(50, 150, 50), item_type="terreno")
    check_image_file("assets/images/tiles/wall.png", color=(100, 100, 100), item_type="terreno")
    check_image_file("assets/images/objects/door.png", color=(150, 75, 0), item_type="porta")
    check_image_file("assets/images/objects/sign.png", color=(120, 80, 40), item_type="placa")
    
    print("Verificação de arquivos concluída!")
    pygame.quit()  # Fecha a janela temporária

if __name__ == "__main__":
    check_all_files() 