#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import json
import os

class Map:
    def __init__(self, map_id="map1"):
        # Tipos de tiles
        self.EMPTY = 0
        self.WALL = 1
        self.DOOR = 2
        
        # Carrega o mapa a partir do arquivo JSON
        self.load_map(map_id)
    
    def load_map(self, map_id):
        """Carrega um mapa a partir de um arquivo JSON"""
        try:
            # Verifica se o arquivo existe
            map_path = os.path.join("maps", f"{map_id}.json")
            if not os.path.exists(map_path):
                raise FileNotFoundError(f"Arquivo de mapa não encontrado: {map_path}")
                
            with open(map_path, "r") as f:
                map_data = json.load(f)
                
            # Informações básicas do mapa
            self.id = map_id
            self.name = map_data.get("name", "Mapa Sem Nome")
            self.width = map_data.get("width", 25)
            self.height = map_data.get("height", 19)
            self.tile_size = map_data.get("tile_size", 32)
            
            # Cores
            self.colors = {
                self.EMPTY: tuple(map_data.get("background_color", [50, 150, 50])),
                self.WALL: tuple(map_data.get("wall_color", [100, 100, 100])),
                self.DOOR: (150, 75, 0)  # Marrom para portas
            }
            
            # Dados do mapa
            self.data = map_data.get("data", [])
            
            # Verifica se os dados do mapa têm as dimensões corretas
            if len(self.data) != self.height:
                print(f"Aviso: Altura do mapa {map_id} incorreta. Esperado {self.height}, encontrado {len(self.data)}")
                
                # Ajusta a altura para corresponder aos dados
                if len(self.data) < self.height:
                    # Adiciona linhas vazias se necessário
                    empty_row = [self.WALL if x == 0 or x == self.width - 1 else self.EMPTY for x in range(self.width)]
                    while len(self.data) < self.height:
                        self.data.append(empty_row.copy())
                else:
                    # Corta linhas extras
                    self.data = self.data[:self.height]
            
            # Verifica se todas as linhas têm a largura correta
            for y, row in enumerate(self.data):
                if len(row) != self.width:
                    print(f"Aviso: Largura da linha {y} do mapa {map_id} incorreta. Esperado {self.width}, encontrado {len(row)}")
                    # Ajusta a linha para ter a largura correta
                    if len(row) < self.width:
                        self.data[y] = row + [self.EMPTY] * (self.width - len(row))
                    else:
                        self.data[y] = row[:self.width]
            
            # Portais
            self.portals = map_data.get("portals", [])
            
            # Transições de borda
            self.edge_transitions = map_data.get("edge_transitions", {
                "left": None,
                "right": None,
                "top": None,
                "bottom": None
            })
            
            # Garante que todas as direções estão definidas
            for direction in ["left", "right", "top", "bottom"]:
                if direction not in self.edge_transitions:
                    self.edge_transitions[direction] = None
            
            # Retângulos de colisão para as paredes
            self.wall_rects = []
            self.door_rects = []
            
            for y in range(self.height):
                for x in range(self.width):
                    try:
                        tile_type = self.data[y][x]
                        if tile_type == self.WALL:
                            self.wall_rects.append(pygame.Rect(
                                x * self.tile_size, 
                                y * self.tile_size, 
                                self.tile_size, 
                                self.tile_size
                            ))
                        elif tile_type == self.DOOR:
                            self.door_rects.append({
                                "rect": pygame.Rect(
                                    x * self.tile_size, 
                                    y * self.tile_size, 
                                    self.tile_size, 
                                    self.tile_size
                                ),
                                "x": x,
                                "y": y
                            })
                    except IndexError:
                        print(f"Erro: Índice inválido no mapa {map_id}: ({x}, {y})")
                        
        except Exception as e:
            print(f"Erro ao carregar o mapa {map_id}: {e}")
            # Cria um mapa vazio em caso de erro
            self.id = "error"
            self.name = "Erro"
            self.width = 25
            self.height = 19
            self.tile_size = 32
            self.colors = {
                self.EMPTY: (0, 0, 0),
                self.WALL: (255, 0, 0),
                self.DOOR: (150, 75, 0)
            }
            self.data = [[self.WALL if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1 
                          else self.EMPTY for x in range(self.width)] for y in range(self.height)]
            self.portals = []
            self.edge_transitions = {"left": None, "right": None, "top": None, "bottom": None}
            self.wall_rects = []
            self.door_rects = []
            
            for y in range(self.height):
                for x in range(self.width):
                    if self.data[y][x] == self.WALL:
                        self.wall_rects.append(pygame.Rect(
                            x * self.tile_size, 
                            y * self.tile_size, 
                            self.tile_size, 
                            self.tile_size
                        ))
    
    def draw(self, screen):
        """Desenha o mapa na tela"""
        for y in range(self.height):
            for x in range(self.width):
                try:
                    tile_type = self.data[y][x]
                    rect = pygame.Rect(
                        x * self.tile_size, 
                        y * self.tile_size, 
                        self.tile_size, 
                        self.tile_size
                    )
                    pygame.draw.rect(screen, self.colors.get(tile_type, (255, 0, 255)), rect)
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Borda preta
                except (IndexError, TypeError):
                    # Em caso de erro, desenha um tile roxo para indicar problema
                    rect = pygame.Rect(
                        x * self.tile_size, 
                        y * self.tile_size, 
                        self.tile_size, 
                        self.tile_size
                    )
                    pygame.draw.rect(screen, (255, 0, 255), rect)  # Roxo para indicar erro
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Borda preta
    
    def check_collision(self, player):
        """Verifica colisões entre o jogador e as paredes"""
        # Guarda a posição anterior
        prev_x = player.rect.x
        prev_y = player.rect.y
        
        # Verifica colisão com cada parede
        for wall in self.wall_rects:
            if player.rect.colliderect(wall):
                # Restaura a posição anterior se houve colisão
                player.rect.x = prev_x
                player.rect.y = prev_y
                return True
        
        return False
    
    def check_door_interaction(self, player):
        """Verifica se o jogador está interagindo com uma porta"""
        for door in self.door_rects:
            if player.rect.colliderect(door["rect"]):
                # Procura o portal correspondente
                for portal in self.portals:
                    try:
                        if portal["x"] == door["x"] and portal["y"] == door["y"]:
                            # Verifica se o mapa de destino existe
                            target_map = portal.get("target_map", "map1")
                            if not os.path.exists(os.path.join("maps", f"{target_map}.json")):
                                print(f"Aviso: Mapa de destino não encontrado: {target_map}")
                                return None
                            
                            # Verifica se as coordenadas de destino são válidas
                            target_x = portal.get("target_x", 12)
                            target_y = portal.get("target_y", 1)
                            
                            return {
                                "target_map": target_map,
                                "target_x": target_x,
                                "target_y": target_y
                            }
                    except (KeyError, TypeError) as e:
                        print(f"Erro ao processar portal: {e}")
        return None
    
    def check_edge_transition(self, player):
        """Verifica se o jogador está saindo pelas bordas do mapa"""
        try:
            # Borda esquerda
            if player.rect.left <= 0 and self.edge_transitions.get("left"):
                transition = self.edge_transitions["left"]
                target_map = transition.get("target_map", "map1")
                
                # Verifica se o mapa de destino existe
                if not os.path.exists(os.path.join("maps", f"{target_map}.json")):
                    print(f"Aviso: Mapa de destino não encontrado: {target_map}")
                    return None
                
                return {
                    "direction": "left",
                    "target_map": target_map,
                    "target_x": transition.get("player_x", 23) * self.tile_size,
                    "target_y": player.rect.y if transition.get("player_y") == "same" else transition.get("player_y", 10) * self.tile_size
                }
            
            # Borda direita
            if player.rect.right >= self.width * self.tile_size and self.edge_transitions.get("right"):
                transition = self.edge_transitions["right"]
                target_map = transition.get("target_map", "map1")
                
                # Verifica se o mapa de destino existe
                if not os.path.exists(os.path.join("maps", f"{target_map}.json")):
                    print(f"Aviso: Mapa de destino não encontrado: {target_map}")
                    return None
                
                return {
                    "direction": "right",
                    "target_map": target_map,
                    "target_x": transition.get("player_x", 1) * self.tile_size,
                    "target_y": player.rect.y if transition.get("player_y") == "same" else transition.get("player_y", 10) * self.tile_size
                }
            
            # Borda superior
            if player.rect.top <= 0 and self.edge_transitions.get("top"):
                transition = self.edge_transitions["top"]
                target_map = transition.get("target_map", "map1")
                
                # Verifica se o mapa de destino existe
                if not os.path.exists(os.path.join("maps", f"{target_map}.json")):
                    print(f"Aviso: Mapa de destino não encontrado: {target_map}")
                    return None
                
                return {
                    "direction": "top",
                    "target_map": target_map,
                    "target_x": player.rect.x if transition.get("player_x") == "same" else transition.get("player_x", 12) * self.tile_size,
                    "target_y": transition.get("player_y", 17) * self.tile_size
                }
            
            # Borda inferior
            if player.rect.bottom >= self.height * self.tile_size and self.edge_transitions.get("bottom"):
                transition = self.edge_transitions["bottom"]
                target_map = transition.get("target_map", "map1")
                
                # Verifica se o mapa de destino existe
                if not os.path.exists(os.path.join("maps", f"{target_map}.json")):
                    print(f"Aviso: Mapa de destino não encontrado: {target_map}")
                    return None
                
                return {
                    "direction": "bottom",
                    "target_map": target_map,
                    "target_x": player.rect.x if transition.get("player_x") == "same" else transition.get("player_x", 12) * self.tile_size,
                    "target_y": transition.get("player_y", 1) * self.tile_size
                }
        except (KeyError, TypeError, AttributeError) as e:
            print(f"Erro ao verificar transição de borda: {e}")
            
        return None 