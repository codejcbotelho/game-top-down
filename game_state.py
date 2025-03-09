#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Estados do jogo
class GameState:
    TITLE_SCREEN = 0
    CHARACTER_SELECT = 1
    PLAYING = 2
    PAUSED = 3
    
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