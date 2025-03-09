#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame

class CharacterSelect:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Opções de personagens
        self.characters = [
            {"name": "Guerreiro", "color": (255, 0, 0), "speed": 5},
            {"name": "Arqueiro", "color": (0, 255, 0), "speed": 6},
            {"name": "Mago", "color": (0, 0, 255), "speed": 4}
        ]
        
        self.selected_index = 0
        
        # Fonte para textos
        self.title_font = pygame.font.SysFont(None, 48)
        self.font = pygame.font.SysFont(None, 36)
        
        # Botões
        self.button_width = 200
        self.button_height = 50
        self.button_margin = 20
        
        # Posição dos botões
        self.buttons_y = self.screen_height // 2
        
        # Cores
        self.button_color = (100, 100, 100)
        self.button_hover_color = (150, 150, 150)
        self.button_text_color = (255, 255, 255)
        self.selected_color = (255, 255, 0)
    
    def handle_event(self, event):
        """Processa eventos da tela de seleção de personagem"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_index = (self.selected_index - 1) % len(self.characters)
            elif event.key == pygame.K_RIGHT:
                self.selected_index = (self.selected_index + 1) % len(self.characters)
            elif event.key == pygame.K_RETURN:
                return self.get_selected_character()
        
        return None
    
    def get_selected_character(self):
        """Retorna o personagem selecionado"""
        return self.characters[self.selected_index]
    
    def draw(self, screen):
        """Desenha a tela de seleção de personagem"""
        # Fundo
        screen.fill((50, 50, 50))
        
        # Título
        title_text = self.title_font.render("Selecione seu Personagem", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(title_text, title_rect)
        
        # Desenha os personagens
        for i, character in enumerate(self.characters):
            # Posição do botão
            button_x = (self.screen_width // 2) + ((i - 1) * (self.button_width + self.button_margin))
            
            # Cor do botão (destacado se selecionado)
            color = self.selected_color if i == self.selected_index else self.button_color
            
            # Desenha o botão
            button_rect = pygame.Rect(
                button_x - self.button_width // 2,
                self.buttons_y,
                self.button_width,
                self.button_height
            )
            pygame.draw.rect(screen, color, button_rect, border_radius=10)
            
            # Texto do botão
            button_text = self.font.render(character["name"], True, self.button_text_color)
            text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, text_rect)
            
            # Desenha o avatar do personagem (um quadrado colorido)
            avatar_size = 80
            avatar_rect = pygame.Rect(
                button_x - avatar_size // 2,
                self.buttons_y - avatar_size - 20,
                avatar_size,
                avatar_size
            )
            pygame.draw.rect(screen, character["color"], avatar_rect)
        
        # Instruções
        instructions_text = self.font.render("Use as setas para selecionar e ENTER para confirmar", True, (200, 200, 200))
        instructions_rect = instructions_text.get_rect(center=(self.screen_width // 2, self.screen_height - 100))
        screen.blit(instructions_text, instructions_rect) 