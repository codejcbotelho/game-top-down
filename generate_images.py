#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import os
import json
import random
import math

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

# Função para criar uma imagem básica
def create_image(color, filename, details=None):
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surface.fill(color)
    
    # Adiciona detalhes específicos se fornecidos
    if details:
        if "pattern" in details:
            if details["pattern"] == "grid":
                # Desenha uma grade
                for x in range(0, TILE_SIZE, 8):
                    pygame.draw.line(surface, details["line_color"], (x, 0), (x, TILE_SIZE), 1)
                for y in range(0, TILE_SIZE, 8):
                    pygame.draw.line(surface, details["line_color"], (0, y), (TILE_SIZE, y), 1)
            elif details["pattern"] == "circle":
                # Desenha um círculo
                pygame.draw.circle(surface, details["circle_color"], 
                                  (TILE_SIZE // 2, TILE_SIZE // 2), 
                                  details["radius"])
            elif details["pattern"] == "rect":
                # Desenha um retângulo
                rect = pygame.Rect(details["rect_x"], details["rect_y"], 
                                  details["rect_width"], details["rect_height"])
                pygame.draw.rect(surface, details["rect_color"], rect)
    
    # Salva a imagem
    pygame.image.save(surface, filename)
    print(f"Imagem '{filename}' criada com sucesso!")

# Função para criar imagens animadas
def create_animated_images(base_color, filename_base, num_frames, details=None):
    for i in range(num_frames):
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        
        # Cor base com variação para animação
        color_variation = 20 * math.sin(i * math.pi / num_frames)
        r = max(0, min(255, base_color[0] + color_variation))
        g = max(0, min(255, base_color[1] + color_variation))
        b = max(0, min(255, base_color[2] + color_variation))
        
        surface.fill((r, g, b))
        
        # Adiciona detalhes específicos se fornecidos
        if details:
            if "pattern" in details:
                if details["pattern"] == "wave":
                    # Desenha uma onda
                    for x in range(TILE_SIZE):
                        y = int(TILE_SIZE // 2 + 5 * math.sin((x + i * 5) * math.pi / 16))
                        pygame.draw.line(surface, details["line_color"], (x, y), (x, TILE_SIZE), 1)
                elif details["pattern"] == "sparkle":
                    # Desenha brilhos
                    for _ in range(5):
                        x = random.randint(4, TILE_SIZE - 4)
                        y = random.randint(4, TILE_SIZE - 4)
                        size = random.randint(1, 3)
                        pygame.draw.circle(surface, details["sparkle_color"], (x, y), size)
        
        # Salva a imagem
        filename = f"{filename_base}_{i}.png"
        pygame.image.save(surface, filename)
        print(f"Imagem '{filename}' criada com sucesso!")

# Gera imagens para os tiles de terreno
def generate_terrain_tiles():
    # Tile vazio (0)
    create_image((100, 200, 100), os.path.join(BASE_DIR, "tiles", "empty.png"))
    
    # Parede (1)
    create_image((100, 100, 100), os.path.join(BASE_DIR, "tiles", "wall.png"), 
                {"pattern": "grid", "line_color": (80, 80, 80)})
    
    # Água (5) - animada
    create_animated_images((100, 150, 255), os.path.join(BASE_DIR, "tiles", "water"), 4,
                         {"pattern": "wave", "line_color": (80, 130, 255)})
    
    # Grama Alta (6) - animada
    create_animated_images((70, 180, 70), os.path.join(BASE_DIR, "tiles", "tall_grass"), 3,
                         {"pattern": "wave", "line_color": (50, 160, 50)})

# Gera imagens para os objetos
def generate_objects():
    # Porta (2)
    create_image((150, 75, 0), os.path.join(BASE_DIR, "objects", "door.png"),
                {"pattern": "rect", "rect_x": 8, "rect_y": 4, 
                 "rect_width": 16, "rect_height": 24, "rect_color": (120, 60, 0)})
    
    # Porta animada
    create_animated_images((150, 75, 0), os.path.join(BASE_DIR, "objects", "door"), 4,
                         {"pattern": "rect", "rect_x": 8, "rect_y": 4, 
                          "rect_width": 16, "rect_height": 24, "rect_color": (120, 60, 0)})
    
    # Árvore (3)
    create_image((50, 120, 50), os.path.join(BASE_DIR, "objects", "tree.png"),
                {"pattern": "rect", "rect_x": 12, "rect_y": 16, 
                 "rect_width": 8, "rect_height": 16, "rect_color": (100, 50, 0)})
    
    # Árvore animada
    create_animated_images((50, 120, 50), os.path.join(BASE_DIR, "objects", "tree"), 2,
                         {"pattern": "rect", "rect_x": 12, "rect_y": 16, 
                          "rect_width": 8, "rect_height": 16, "rect_color": (100, 50, 0)})
    
    # Arbusto (4)
    create_image((30, 150, 30), os.path.join(BASE_DIR, "objects", "bush.png"),
                {"pattern": "circle", "circle_color": (20, 120, 20), "radius": 10})
    
    # Baú (9)
    create_image((150, 100, 50), os.path.join(BASE_DIR, "objects", "chest.png"),
                {"pattern": "rect", "rect_x": 8, "rect_y": 12, 
                 "rect_width": 16, "rect_height": 12, "rect_color": (120, 80, 40)})
    
    # Baú animado
    create_animated_images((150, 100, 50), os.path.join(BASE_DIR, "objects", "chest"), 3,
                         {"pattern": "rect", "rect_x": 8, "rect_y": 12, 
                          "rect_width": 16, "rect_height": 12, "rect_color": (120, 80, 40)})
    
    # Porta Trancada (11)
    create_image((100, 50, 0), os.path.join(BASE_DIR, "objects", "door_locked.png"),
                {"pattern": "rect", "rect_x": 8, "rect_y": 4, 
                 "rect_width": 16, "rect_height": 24, "rect_color": (80, 40, 0)})
    
    # Porta Trancada animada
    create_animated_images((100, 50, 0), os.path.join(BASE_DIR, "objects", "door_locked"), 5,
                         {"pattern": "rect", "rect_x": 8, "rect_y": 4, 
                          "rect_width": 16, "rect_height": 24, "rect_color": (80, 40, 0)})
    
    # Placa (12)
    create_image((120, 80, 40), os.path.join(BASE_DIR, "objects", "sign.png"),
                {"pattern": "rect", "rect_x": 12, "rect_y": 16, 
                 "rect_width": 8, "rect_height": 12, "rect_color": (100, 60, 20)})
    
    # Escada para Baixo (40)
    create_image((80, 80, 80), os.path.join(BASE_DIR, "objects", "stairs_down.png"),
                {"pattern": "rect", "rect_x": 8, "rect_y": 8, 
                 "rect_width": 16, "rect_height": 16, "rect_color": (60, 60, 60)})
    
    # Escada para Cima (41)
    create_image((100, 100, 100), os.path.join(BASE_DIR, "objects", "stairs_up.png"),
                {"pattern": "rect", "rect_x": 8, "rect_y": 8, 
                 "rect_width": 16, "rect_height": 16, "rect_color": (120, 120, 120)})
    
    # Portal (42)
    create_image((150, 50, 200), os.path.join(BASE_DIR, "objects", "portal.png"),
                {"pattern": "circle", "circle_color": (200, 100, 255), "radius": 12})
    
    # Portal animado
    create_animated_images((150, 50, 200), os.path.join(BASE_DIR, "objects", "portal"), 8,
                         {"pattern": "sparkle", "sparkle_color": (255, 200, 255)})

# Gera imagens para os itens
def generate_items():
    # Moeda (7)
    create_image((255, 215, 0), os.path.join(BASE_DIR, "items", "coin.png"),
                {"pattern": "circle", "circle_color": (255, 255, 0), "radius": 8})
    
    # Moeda animada
    create_animated_images((255, 215, 0), os.path.join(BASE_DIR, "items", "coin"), 6,
                         {"pattern": "sparkle", "sparkle_color": (255, 255, 200)})
    
    # Poção de Vida (8)
    create_image((200, 0, 0), os.path.join(BASE_DIR, "items", "health_potion.png"),
                {"pattern": "rect", "rect_x": 10, "rect_y": 8, 
                 "rect_width": 12, "rect_height": 16, "rect_color": (255, 0, 0)})
    
    # Poção de Vida animada
    create_animated_images((200, 0, 0), os.path.join(BASE_DIR, "items", "health_potion"), 4,
                         {"pattern": "sparkle", "sparkle_color": (255, 100, 100)})
    
    # Chave (10)
    create_image((200, 200, 0), os.path.join(BASE_DIR, "items", "key.png"),
                {"pattern": "rect", "rect_x": 12, "rect_y": 12, 
                 "rect_width": 8, "rect_height": 8, "rect_color": (255, 255, 0)})
    
    # Chave animada
    create_animated_images((200, 200, 0), os.path.join(BASE_DIR, "items", "key"), 4,
                         {"pattern": "sparkle", "sparkle_color": (255, 255, 100)})

# Gera imagens para os inimigos
def generate_enemies():
    # Slime (20)
    create_image((0, 200, 0), os.path.join(BASE_DIR, "enemies", "slime.png"),
                {"pattern": "circle", "circle_color": (0, 150, 0), "radius": 10})
    
    # Slime animado
    create_animated_images((0, 200, 0), os.path.join(BASE_DIR, "enemies", "slime"), 4,
                         {"pattern": "wave", "line_color": (0, 150, 0)})
    
    # Morcego (21)
    create_image((50, 50, 50), os.path.join(BASE_DIR, "enemies", "bat.png"),
                {"pattern": "circle", "circle_color": (100, 100, 100), "radius": 8})
    
    # Morcego animado
    create_animated_images((50, 50, 50), os.path.join(BASE_DIR, "enemies", "bat"), 4,
                         {"pattern": "sparkle", "sparkle_color": (100, 100, 100)})
    
    # Esqueleto (22)
    create_image((200, 200, 200), os.path.join(BASE_DIR, "enemies", "skeleton.png"),
                {"pattern": "rect", "rect_x": 10, "rect_y": 6, 
                 "rect_width": 12, "rect_height": 20, "rect_color": (150, 150, 150)})
    
    # Esqueleto animado
    create_animated_images((200, 200, 200), os.path.join(BASE_DIR, "enemies", "skeleton"), 6,
                         {"pattern": "sparkle", "sparkle_color": (150, 150, 150)})

# Gera imagens para os NPCs
def generate_npcs():
    # NPC Aldeão (30)
    create_image((0, 100, 200), os.path.join(BASE_DIR, "npcs", "villager.png"),
                {"pattern": "rect", "rect_x": 10, "rect_y": 6, 
                 "rect_width": 12, "rect_height": 20, "rect_color": (0, 80, 150)})
    
    # NPC Aldeão animado
    create_animated_images((0, 100, 200), os.path.join(BASE_DIR, "npcs", "villager"), 2,
                         {"pattern": "sparkle", "sparkle_color": (0, 150, 255)})
    
    # NPC Comerciante (31)
    create_image((200, 100, 0), os.path.join(BASE_DIR, "npcs", "merchant.png"),
                {"pattern": "rect", "rect_x": 10, "rect_y": 6, 
                 "rect_width": 12, "rect_height": 20, "rect_color": (150, 80, 0)})
    
    # NPC Comerciante animado
    create_animated_images((200, 100, 0), os.path.join(BASE_DIR, "npcs", "merchant"), 2,
                         {"pattern": "sparkle", "sparkle_color": (255, 150, 0)})

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