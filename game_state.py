#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Estados do jogo
class GameState:
    TITLE_SCREEN = 0
    CHARACTER_SELECT = 1
    PLAYING = 2
    PAUSED = 3
    HELP_SCREEN = 4
    SHOPPING = 5
    DIALOG = 6  # Diálogo simples (não interativo)
    INTERACTIVE_DIALOG = 7  # Diálogo interativo (com escolhas)
    INVENTORY = 8  # Inventário do jogador
    
    def __init__(self):
        self.current_state = self.TITLE_SCREEN
        self.previous_state = None
    
    def change_state(self, new_state):
        """Muda o estado atual do jogo"""
        self.previous_state = self.current_state
        self.current_state = new_state
    
    def return_to_previous_state(self):
        """Retorna ao estado anterior"""
        if self.previous_state is not None:
            temp = self.current_state
            self.current_state = self.previous_state
            self.previous_state = temp
    
    def is_title_screen(self):
        """Verifica se está na tela de título"""
        return self.current_state == self.TITLE_SCREEN
    
    def is_character_select(self):
        """Verifica se está na tela de seleção de personagem"""
        return self.current_state == self.CHARACTER_SELECT
    
    def is_playing(self):
        """Verifica se está jogando"""
        return self.current_state == self.PLAYING
    
    def is_paused(self):
        """Verifica se está pausado"""
        return self.current_state == self.PAUSED
        
    def is_help_screen(self):
        """Verifica se está na tela de ajuda"""
        return self.current_state == self.HELP_SCREEN
        
    def is_shopping(self):
        """Verifica se está na interface de compra"""
        return self.current_state == self.SHOPPING
        
    def is_dialog(self):
        """Verifica se está exibindo um diálogo"""
        return self.current_state == self.DIALOG
        
    def is_interactive_dialog(self):
        """Verifica se está exibindo um diálogo interativo"""
        return self.current_state == self.INTERACTIVE_DIALOG
        
    def is_inventory(self):
        """Verifica se está exibindo o inventário"""
        return self.current_state == self.INVENTORY
        
    def is_any_dialog(self):
        """Verifica se está em qualquer tipo de diálogo"""
        return self.is_dialog() or self.is_interactive_dialog() or self.is_shopping() or self.is_inventory() 