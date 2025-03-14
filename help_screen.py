#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame

class HelpScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Fontes para textos
        self.title_font = pygame.font.SysFont(None, 64)
        self.subtitle_font = pygame.font.SysFont(None, 36)
        self.font = pygame.font.SysFont(None, 28)
        
        # Cores
        self.text_color = (255, 255, 255)
        self.background_color = (40, 40, 40)
        self.subtitle_color = (255, 255, 150)
        
        # Seções de ajuda
        self.help_sections = [
            {
                "title": "Controles",
                "content": [
                    "WASD ou SETAS: Mover o personagem",
                    "E: Interagir com objetos e NPCs",
                    "ESPAÇO: Atacar",
                    "SHIFT: Correr",
                    "ESC: Pausar / Voltar"
                ]
            },
            {
                "title": "Itens",
                "content": [
                    "Poções Vermelhas: Restauram vida",
                    "Poções Azuis: Restauram mana",
                    "Chaves: Abrem portas específicas",
                    "Moedas: Usadas para comprar itens",
                    "Pergaminhos: Contêm magias para usar em batalha"
                ]
            },
            {
                "title": "Inimigos",
                "content": [
                    "Slimes: Lentos mas resistentes",
                    "Morcegos: Rápidos e difíceis de acertar",
                    "Esqueletos: Equilibrados e perigosos em grupos"
                ]
            },
            {
                "title": "Mundo",
                "content": [
                    "O mapa é dividido em regiões conectadas",
                    "Use portas ou bordas para mudar de área",
                    "Converse com NPCs para obter dicas",
                    "Compre itens com comerciantes",
                    "Explore para encontrar tesouros escondidos"
                ]
            }
        ]
    
    def handle_event(self, event):
        """Processa eventos da tela de ajuda"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                return "back_to_menu"
        
        return None
    
    def draw(self, screen):
        """Desenha a tela de ajuda"""
        # Preenche o fundo
        screen.fill(self.background_color)
        
        # Título principal
        title_text = self.title_font.render("COMO JOGAR", True, self.text_color)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 80))
        screen.blit(title_text, title_rect)
        
        # Desenha as seções de ajuda
        y_offset = 150
        for section in self.help_sections:
            # Título da seção
            section_title = self.subtitle_font.render(section["title"], True, self.subtitle_color)
            section_rect = section_title.get_rect(topleft=(self.screen_width // 6, y_offset))
            screen.blit(section_title, section_rect)
            
            # Conteúdo da seção
            y_offset += 40
            for line in section["content"]:
                content_text = self.font.render(line, True, self.text_color)
                content_rect = content_text.get_rect(topleft=(self.screen_width // 5, y_offset))
                screen.blit(content_text, content_rect)
                y_offset += 30
            
            y_offset += 20
        
        # Instruções para voltar
        instructions_text = self.font.render("Pressione ESC ou ENTER para voltar ao menu", True, (200, 200, 200))
        instructions_rect = instructions_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        screen.blit(instructions_text, instructions_rect) 