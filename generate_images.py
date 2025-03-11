#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import os
import json
import random
import math
from utils import get_asset_path, ensure_dir_exists

# Inicializa o pygame
pygame.init()

# Tamanho do tile
TILE_SIZE = 32

# Diretório base para as imagens
BASE_DIR = "assets/images"

# Cria os diretórios se não existirem
os.makedirs(os.path.join(BASE_DIR, "tiles"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "objects"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "items"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "enemies"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "npcs"), exist_ok=True)

def create_image(color, path, size=(32, 32), pattern=None, text=None):
    """
    Cria uma imagem colorida com um padrão opcional
    
    Args:
        color (tuple): Cor RGB da imagem
        path (str): Caminho onde salvar a imagem
        size (tuple): Tamanho da imagem em pixels
        pattern (str): Tipo de padrão a ser desenhado ('grid', 'diagonal', etc)
        text (str): Texto opcional para adicionar à imagem
    """
    # Cria o diretório se não existir
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Cria a superfície e preenche com a cor base
    img = pygame.Surface(size)
    img.fill(color)
    
    # Adiciona padrão se especificado
    if pattern == 'grid':
        for x in range(0, size[0], 8):
            pygame.draw.line(img, (0, 0, 0), (x, 0), (x, size[1]), 1)
        for y in range(0, size[1], 8):
            pygame.draw.line(img, (0, 0, 0), (0, y), (size[0], y), 1)
    elif pattern == 'diagonal':
        for i in range(-size[1], size[0], 8):
            pygame.draw.line(img, (0, 0, 0), (i, 0), (i + size[1], size[1]), 1)
    
    # Adiciona texto se especificado
    if text:
        try:
            font = pygame.font.SysFont('Arial', 12)
            text_surface = font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(size[0]//2, size[1]//2))
            img.blit(text_surface, text_rect)
        except:
            # Se não conseguir renderizar texto, desenha um padrão simples
            pygame.draw.rect(img, (0, 0, 0), (4, 4, size[0]-8, size[1]-8), 2)
    
    # Salva a imagem
    pygame.image.save(img, path)

def create_animated_images(color, base_path, num_frames, size=(32, 32), pattern=None):
    """
    Cria uma sequência de imagens para animação
    
    Args:
        color (tuple): Cor RGB base
        base_path (str): Caminho base para salvar as imagens
        num_frames (int): Número de frames na animação
        size (tuple): Tamanho de cada frame em pixels
        pattern (str): Tipo de padrão a ser desenhado
    """
    # Cria o diretório se não existir
    os.makedirs(os.path.dirname(base_path), exist_ok=True)
    
    for i in range(num_frames):
        # Calcula cor variante para este frame
        frame_color = list(color)
        variation = int(20 * (i / (num_frames - 1) - 0.5))  # -10 a +10
        frame_color = [min(255, max(0, c + variation)) for c in frame_color]
        
        # Cria o frame
        frame_path = f"{base_path}_{i}.png"
        create_image(tuple(frame_color), frame_path, size, pattern)

# Gera imagens para os tiles de terreno
def generate_terrain_tiles():
    # Tile vazio (0)
    create_image(
        (100, 200, 100),
        get_asset_path("assets", "images", "tiles", "empty.png"),
        text="Empty"
    )
    
    # Parede (1)
    create_image(
        (100, 100, 100),
        get_asset_path("assets", "images", "tiles", "wall.png"),
        pattern='grid',
        text="Wall"
    )
    
    # Água (5) - animada
    create_animated_images(
        (100, 150, 255),
        get_asset_path("assets", "images", "tiles", "water"),
        4,
        pattern='diagonal'
    )
    
    # Grama Alta (6) - animada
    create_animated_images(
        (70, 180, 70),
        get_asset_path("assets", "images", "tiles", "tall_grass"),
        3,
        pattern='diagonal'
    )

# Gera imagens para os objetos
def generate_objects():
    # Porta (2)
    create_image(
        (150, 75, 0),
        get_asset_path("assets", "images", "objects", "door.png"),
        text="Door"
    )
    
    # Porta animada
    create_animated_images(
        (150, 75, 0),
        get_asset_path("assets", "images", "objects", "door"),
        4,
        pattern='grid'
    )
    
    # Árvore (3)
    create_image(
        (50, 120, 50),
        get_asset_path("assets", "images", "objects", "tree.png"),
        text="Tree"
    )
    
    # Árvore animada
    create_animated_images(
        (50, 120, 50),
        get_asset_path("assets", "images", "objects", "tree"),
        2,
        pattern='diagonal'
    )
    
    # Arbusto (4)
    create_image(
        (30, 150, 30),
        get_asset_path("assets", "images", "objects", "bush.png"),
        text="Bush"
    )
    
    # Baú (9)
    create_image(
        (150, 100, 50),
        get_asset_path("assets", "images", "objects", "chest.png"),
        text="Chest"
    )
    
    # Baú animado
    create_animated_images(
        (150, 100, 50),
        get_asset_path("assets", "images", "objects", "chest"),
        3,
        pattern='grid'
    )
    
    # Porta Trancada (11)
    create_image(
        (100, 50, 0),
        get_asset_path("assets", "images", "objects", "door_locked.png"),
        text="Locked"
    )
    
    # Porta Trancada animada
    create_animated_images(
        (100, 50, 0),
        get_asset_path("assets", "images", "objects", "door_locked"),
        5,
        pattern='grid'
    )
    
    # Placa (12)
    create_image(
        (120, 80, 40),
        get_asset_path("assets", "images", "objects", "sign.png"),
        text="Sign"
    )
    
    # Escada para Baixo (40)
    create_image(
        (80, 80, 80),
        get_asset_path("assets", "images", "objects", "stairs_down.png"),
        text="Down"
    )
    
    # Escada para Cima (41)
    create_image(
        (100, 100, 100),
        get_asset_path("assets", "images", "objects", "stairs_up.png"),
        text="Up"
    )
    
    # Portal (42)
    create_image(
        (150, 50, 200),
        get_asset_path("assets", "images", "objects", "portal.png"),
        text="Portal"
    )
    
    # Portal animado
    create_animated_images(
        (150, 50, 200),
        get_asset_path("assets", "images", "objects", "portal"),
        8,
        pattern='diagonal'
    )

# Gera imagens para os itens
def generate_items():
    # Moeda (7)
    create_image(
        (255, 215, 0),
        get_asset_path("assets", "images", "items", "coin.png"),
        text="Coin"
    )
    
    # Moeda animada
    create_animated_images(
        (255, 215, 0),
        get_asset_path("assets", "images", "items", "coin"),
        6
    )
    
    # Poção de Vida (8)
    create_image(
        (200, 0, 0),
        get_asset_path("assets", "images", "items", "health_potion.png"),
        text="HP"
    )
    
    # Poção de Vida animada
    create_animated_images(
        (200, 0, 0),
        get_asset_path("assets", "images", "items", "health_potion"),
        4,
        pattern='diagonal'
    )
    
    # Chave (10)
    create_image(
        (200, 200, 0),
        get_asset_path("assets", "images", "items", "key.png"),
        text="Key"
    )
    
    # Chave animada
    create_animated_images(
        (200, 200, 0),
        get_asset_path("assets", "images", "items", "key"),
        4,
        pattern='diagonal'
    )

# Gera imagens para os inimigos
def generate_enemies():
    # Slime (20)
    create_image(
        (0, 200, 0),
        get_asset_path("assets", "images", "enemies", "slime.png"),
        text="Slime"
    )
    
    # Slime animado
    create_animated_images(
        (0, 200, 0),
        get_asset_path("assets", "images", "enemies", "slime"),
        4
    )
    
    # Morcego (21)
    create_image(
        (50, 50, 50),
        get_asset_path("assets", "images", "enemies", "bat.png"),
        text="Bat"
    )
    
    # Morcego animado
    create_animated_images(
        (50, 50, 50),
        get_asset_path("assets", "images", "enemies", "bat"),
        4
    )
    
    # Esqueleto (22)
    create_image(
        (200, 200, 200),
        get_asset_path("assets", "images", "enemies", "skeleton.png"),
        text="Skeleton"
    )
    
    # Esqueleto animado
    create_animated_images(
        (200, 200, 200),
        get_asset_path("assets", "images", "enemies", "skeleton"),
        6,
        pattern='grid'
    )

# Gera imagens para os NPCs
def generate_npcs():
    # NPC Aldeão (30)
    create_image(
        (0, 100, 200),
        get_asset_path("assets", "images", "npcs", "villager.png"),
        text="Villager"
    )
    
    # NPC Aldeão animado
    create_animated_images(
        (0, 100, 200),
        get_asset_path("assets", "images", "npcs", "villager"),
        2,
        pattern='grid'
    )
    
    # NPC Comerciante (31)
    create_image(
        (200, 100, 0),
        get_asset_path("assets", "images", "npcs", "merchant.png"),
        text="Merchant"
    )
    
    # NPC Comerciante animado
    create_animated_images(
        (200, 100, 0),
        get_asset_path("assets", "images", "npcs", "merchant"),
        2,
        pattern='grid'
    )

# Gera todas as imagens
def generate_all_images():
    generate_terrain_tiles()
    generate_objects()
    generate_items()
    generate_enemies()
    generate_npcs()
    print("Todas as imagens foram geradas com sucesso!")

if __name__ == "__main__":
    generate_all_images() 