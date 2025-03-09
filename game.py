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
        
        # Carrega o mapa inicial
        self.current_map_id = "map1"
        self.map = Map(self.current_map_id)
        
        # Carrega objetos do jogo
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self.WIDTH // 2, self.HEIGHT // 2)
        self.all_sprites.add(self.player)
        
        # Estado do jogo
        self.running = True
        
        # Fonte para texto
        self.font = pygame.font.SysFont(None, 24)
    
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
            
            # Passa o evento para o jogador
            self.player.handle_event(event)
    
    def update(self):
        """Atualiza todos os objetos do jogo"""
        self.all_sprites.update()
        
        # Verifica colisões com o mapa
        self.map.check_collision(self.player)
        
        # Verifica interação com portas
        if self.player.interacting:
            portal = self.map.check_door_interaction(self.player)
            if portal:
                self.change_map(portal["target_map"], portal["target_x"], portal["target_y"])
                self.player.interacting = False
        
        # Verifica transições de borda
        edge_transition = self.map.check_edge_transition(self.player)
        if edge_transition:
            self.change_map(edge_transition["target_map"], edge_transition["target_x"], edge_transition["target_y"])
    
    def change_map(self, map_id, player_x, player_y):
        """Muda para um novo mapa"""
        self.current_map_id = map_id
        self.map = Map(map_id)
        self.player.set_position(player_x, player_y)
    
    def render(self):
        """Renderiza os objetos na tela"""
        # Preenche o fundo com cor preta
        self.screen.fill((0, 0, 0))
        
        # Desenha o mapa
        self.map.draw(self.screen)
        
        # Desenha todos os sprites
        self.all_sprites.draw(self.screen)
        
        # Desenha informações do mapa atual
        map_text = self.font.render(f"Mapa: {self.map.name}", True, (255, 255, 255))
        self.screen.blit(map_text, (10, 10))
        
        # Desenha instruções
        instructions = self.font.render("Use WASD ou setas para mover, E para interagir com portas", True, (255, 255, 255))
        self.screen.blit(instructions, (10, self.HEIGHT - 30))
        
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