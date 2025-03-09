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
            with open(os.path.join("maps", f"{map_id}.json"), "r") as f:
                map_data = json.load(f)
                
            # Informações básicas do mapa
            self.id = map_id
            self.name = map_data["name"]
            self.width = map_data["width"]
            self.height = map_data["height"]
            self.tile_size = map_data["tile_size"]
            
            # Cores
            self.colors = {
                self.EMPTY: tuple(map_data["background_color"]),
                self.WALL: tuple(map_data["wall_color"]),
                self.DOOR: (150, 75, 0)  # Marrom para portas
            }
            
            # Dados do mapa
            self.data = map_data["data"]
            
            # Portais
            self.portals = map_data["portals"]
            
            # Transições de borda
            self.edge_transitions = map_data["edge_transitions"]
            
            # Retângulos de colisão para as paredes
            self.wall_rects = []
            self.door_rects = []
            
            for y in range(self.height):
                for x in range(self.width):
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
                tile_type = self.data[y][x]
                rect = pygame.Rect(
                    x * self.tile_size, 
                    y * self.tile_size, 
                    self.tile_size, 
                    self.tile_size
                )
                pygame.draw.rect(screen, self.colors[tile_type], rect)
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
                    if portal["x"] == door["x"] and portal["y"] == door["y"]:
                        return portal
        return None
    
    def check_edge_transition(self, player):
        """Verifica se o jogador está saindo pelas bordas do mapa"""
        # Borda esquerda
        if player.rect.left <= 0 and self.edge_transitions["left"]:
            return {
                "direction": "left",
                "target_map": self.edge_transitions["left"]["target_map"],
                "target_x": self.edge_transitions["left"]["player_x"] * self.tile_size,
                "target_y": player.rect.y if self.edge_transitions["left"]["player_y"] == "same" else self.edge_transitions["left"]["player_y"] * self.tile_size
            }
        
        # Borda direita
        if player.rect.right >= self.width * self.tile_size and self.edge_transitions["right"]:
            return {
                "direction": "right",
                "target_map": self.edge_transitions["right"]["target_map"],
                "target_x": self.edge_transitions["right"]["player_x"] * self.tile_size,
                "target_y": player.rect.y if self.edge_transitions["right"]["player_y"] == "same" else self.edge_transitions["right"]["player_y"] * self.tile_size
            }
        
        # Borda superior
        if player.rect.top <= 0 and self.edge_transitions["top"]:
            return {
                "direction": "top",
                "target_map": self.edge_transitions["top"]["target_map"],
                "target_x": player.rect.x if self.edge_transitions["top"]["player_x"] == "same" else self.edge_transitions["top"]["player_x"] * self.tile_size,
                "target_y": self.edge_transitions["top"]["player_y"] * self.tile_size
            }
        
        # Borda inferior
        if player.rect.bottom >= self.height * self.tile_size and self.edge_transitions["bottom"]:
            return {
                "direction": "bottom",
                "target_map": self.edge_transitions["bottom"]["target_map"],
                "target_x": player.rect.x if self.edge_transitions["bottom"]["player_x"] == "same" else self.edge_transitions["bottom"]["player_x"] * self.tile_size,
                "target_y": self.edge_transitions["bottom"]["player_y"] * self.tile_size
            }
        
        return None 