#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import sys
import os
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
        self.transition_cooldown = 0  # Evita transições repetidas
        
        # Fonte para texto
        self.font = pygame.font.SysFont(None, 24)
        
        # Mensagem de erro (se houver)
        self.error_message = None
        self.error_timer = 0
    
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
        
        # Atualiza o cooldown de transição
        if self.transition_cooldown > 0:
            self.transition_cooldown -= 1
        
        # Atualiza o timer de erro
        if self.error_timer > 0:
            self.error_timer -= 1
            if self.error_timer <= 0:
                self.error_message = None
        
        # Verifica colisões com o mapa
        self.map.check_collision(self.player)
        
        # Verifica interação com portas
        if self.player.interacting and self.transition_cooldown == 0:
            portal = self.map.check_door_interaction(self.player)
            if portal:
                self.change_map(portal["target_map"], portal["target_x"], portal["target_y"])
                self.player.interacting = False
        
        # Verifica transições de borda
        if self.transition_cooldown == 0:
            edge_transition = self.map.check_edge_transition(self.player)
            if edge_transition:
                self.change_map(edge_transition["target_map"], edge_transition["target_x"], edge_transition["target_y"])
    
    def change_map(self, map_id, player_x, player_y):
        """Muda para um novo mapa"""
        try:
            # Verifica se o arquivo do mapa existe
            if not os.path.exists(os.path.join("maps", f"{map_id}.json")):
                self.show_error(f"Mapa não encontrado: {map_id}")
                return
            
            # Carrega o novo mapa
            self.current_map_id = map_id
            self.map = Map(map_id)
            
            # Posiciona o jogador
            self.player.set_position(player_x, player_y)
            
            # Define um cooldown para evitar transições repetidas
            self.transition_cooldown = 10
        except Exception as e:
            self.show_error(f"Erro ao mudar de mapa: {e}")
    
    def show_error(self, message):
        """Mostra uma mensagem de erro temporária"""
        print(f"ERRO: {message}")
        self.error_message = message
        self.error_timer = 180  # 3 segundos a 60 FPS
    
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
        
        # Desenha mensagem de erro, se houver
        if self.error_message:
            # Cria um fundo semi-transparente
            error_bg = pygame.Surface((self.WIDTH, 60))
            error_bg.fill((200, 0, 0))
            error_bg.set_alpha(200)
            self.screen.blit(error_bg, (0, self.HEIGHT // 2 - 30))
            
            # Desenha a mensagem de erro
            error_text = self.font.render(f"ERRO: {self.error_message}", True, (255, 255, 255))
            error_rect = error_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            self.screen.blit(error_text, error_rect)
        
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