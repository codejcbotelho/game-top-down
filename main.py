#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from game import Game
from check_game_files import check_all_files

if __name__ == "__main__":
    # Verifica e corrige os arquivos do jogo antes de iniciar
    check_all_files()
    
    # Inicia o jogo
    game = Game()
    game.run() 