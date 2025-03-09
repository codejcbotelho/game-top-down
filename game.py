#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import sys
from player import Player
from map import Map

class Game:
    def __init__(self):
        # Inicializa o pygame
        pygame.init()
        
        # Constantes
        self.WIDTH = 800
        self.HEIGHT = 600
        self.FPS = 60
        self.TITLE = "Jogo Top-Down"
        
        # Configuração da tela
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(self.TITLE)
        
        # Relógio para controlar FPS
        self.clock = pygame.time.Clock()
        
        # Carrega objetos do jogo
        self.all_sprites = pygame.sprite.Group()
        self.map = Map()
        self.player = Player(self.WIDTH // 2, self.HEIGHT // 2)
        self.all_sprites.add(self.player)
        
        # Estado do jogo
        self.running = True
    
    def process_events(self):
        """Processa os eventos (teclado, mouse, etc)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return
    
    def update(self):
        """Atualiza todos os objetos do jogo"""
        self.all_sprites.update()
        
        # Verifica colisões com o mapa
        self.map.check_collision(self.player)
    
    def render(self):
        """Renderiza os objetos na tela"""
        # Preenche o fundo com cor preta
        self.screen.fill((0, 0, 0))
        
        # Desenha o mapa
        self.map.draw(self.screen)
        
        # Desenha todos os sprites
        self.all_sprites.draw(self.screen)
        
        # Atualiza a tela
        pygame.display.flip()
    
    def run(self):
        """Loop principal do jogo"""
        while self.running:
            self.process_events()
            self.update()
            self.render()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit() 