#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame

class Map:
    def __init__(self):
        # Tamanho do mapa em tiles
        self.width = 25
        self.height = 19
        self.tile_size = 32
        
        # Tipos de tiles
        self.EMPTY = 0
        self.WALL = 1
        
        # Cores
        self.colors = {
            self.EMPTY: (50, 150, 50),  # Verde escuro
            self.WALL: (100, 100, 100)   # Cinza
        }
        
        # Criar um mapa simples com paredes nas bordas
        self.data = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    row.append(self.WALL)
                else:
                    row.append(self.EMPTY)
            self.data.append(row)
            
        # Adicionar alguns obstáculos
        for x in range(5, 10):
            self.data[5][x] = self.WALL
        
        for y in range(8, 12):
            self.data[y][15] = self.WALL
        
        # Retângulos de colisão para as paredes
        self.wall_rects = []
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