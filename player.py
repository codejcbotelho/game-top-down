#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, character_data=None):
        super().__init__()
        
        # Dados do personagem
        if character_data is None:
            # Personagem padrão
            self.name = "Jogador"
            self.color = (0, 0, 255)  # Azul
            self.speed = 5
        else:
            # Personagem personalizado
            self.name = character_data.get("name", "Jogador")
            self.color = character_data.get("color", (0, 0, 255))
            self.speed = character_data.get("speed", 5)
        
        # Cria uma imagem para o jogador
        self.image = pygame.Surface((32, 32))
        self.image.fill(self.color)
        
        # Define o retângulo do sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Vetores de velocidade
        self.velocity = pygame.math.Vector2(0, 0)
        
        # Direção que o jogador está olhando
        self.direction = "down"
        
        # Estado de interação
        self.interacting = False
    
    def update(self):
        """Atualiza a posição do jogador com base nos controles"""
        # Reinicia a velocidade
        self.velocity = pygame.math.Vector2(0, 0)
        
        # Obtém as teclas pressionadas
        keys = pygame.key.get_pressed()
        
        # Movimento horizontal
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = self.speed
            self.direction = "right"
            
        # Movimento vertical
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.y = -self.speed
            self.direction = "up"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity.y = self.speed
            self.direction = "down"
            
        # Normaliza o vetor se estiver se movendo na diagonal
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * self.speed
        
        # Atualiza a posição
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
    
    def handle_event(self, event):
        """Processa eventos específicos do jogador"""
        if event.type == pygame.KEYDOWN:
            # Tecla E para interagir com objetos
            if event.key == pygame.K_e:
                self.interacting = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                self.interacting = False
    
    def set_position(self, x, y):
        """Define a posição do jogador"""
        self.rect.x = x
        self.rect.y = y
    
    def constrain_to_map(self, map_width, map_height):
        """Impede que o jogador saia dos limites do mapa"""
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > map_width:
            self.rect.right = map_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > map_height:
            self.rect.bottom = map_height 