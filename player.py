#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Cria uma imagem temporária para o jogador (um quadrado azul)
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 0, 255))  # Azul
        
        # Define o retângulo do sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Vetores de velocidade
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 5
        
        # Direção que o jogador está olhando
        self.direction = "down"
    
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
        
        # Impede que o jogador saia da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600 