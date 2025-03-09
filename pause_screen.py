#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame

class PauseScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Fonte para textos
        self.title_font = pygame.font.SysFont(None, 72)
        self.font = pygame.font.SysFont(None, 36)
        
        # Botões
        self.buttons = [
            {"text": "Continuar", "action": "resume"},
            {"text": "Voltar ao Menu", "action": "menu"},
            {"text": "Sair", "action": "quit"}
        ]
        
        self.selected_index = 0
        
        # Dimensões dos botões
        self.button_width = 200
        self.button_height = 50
        self.button_margin = 20
        
        # Posição inicial dos botões
        self.buttons_y = self.screen_height // 2 - 50
        
        # Cores
        self.button_color = (100, 100, 100)
        self.button_hover_color = (150, 150, 150)
        self.button_text_color = (255, 255, 255)
        self.selected_color = (255, 255, 0)
        
        # Fundo semi-transparente
        self.overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))  # Preto com 50% de transparência
    
    def handle_event(self, event):
        """Processa eventos da tela de pausa"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.buttons)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                return self.buttons[self.selected_index]["action"]
            elif event.key == pygame.K_ESCAPE:
                return "resume"
        
        return None
    
    def draw(self, screen):
        """Desenha a tela de pausa sobre o jogo"""
        # Aplica o overlay semi-transparente
        screen.blit(self.overlay, (0, 0))
        
        # Título
        title_text = self.title_font.render("Jogo Pausado", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title_text, title_rect)
        
        # Desenha os botões
        for i, button in enumerate(self.buttons):
            # Posição do botão
            button_y = self.buttons_y + (i * (self.button_height + self.button_margin))
            
            # Cor do botão (destacado se selecionado)
            color = self.selected_color if i == self.selected_index else self.button_color
            
            # Desenha o botão
            button_rect = pygame.Rect(
                (self.screen_width - self.button_width) // 2,
                button_y,
                self.button_width,
                self.button_height
            )
            pygame.draw.rect(screen, color, button_rect, border_radius=10)
            
            # Texto do botão
            button_text = self.font.render(button["text"], True, self.button_text_color)
            text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, text_rect)
        
        # Instruções
        instructions_text = self.font.render("Use as setas para selecionar e ENTER para confirmar", True, (200, 200, 200))
        instructions_rect = instructions_text.get_rect(center=(self.screen_width // 2, self.screen_height - 100))
        screen.blit(instructions_text, instructions_rect) 