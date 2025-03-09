#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import sys
import os
from player import Player
from map import Map
from game_state import GameState
from title_screen import TitleScreen
from character_select import CharacterSelect
from pause_screen import PauseScreen

class Game:
    def __init__(self):
        # Inicializa o pygame
        pygame.init()
        pygame.mixer.init()  # Inicializa o mixer para áudio
        
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
        
        # Estado do jogo
        self.game_state = GameState()
        
        # Telas do jogo
        self.title_screen = TitleScreen(self.WIDTH, self.HEIGHT)
        self.character_select = CharacterSelect(self.WIDTH, self.HEIGHT)
        self.pause_screen = PauseScreen(self.WIDTH, self.HEIGHT)
        
        # Carrega o mapa inicial
        self.current_map_id = "map1"
        self.map = Map(self.current_map_id)
        
        # Carrega objetos do jogo
        self.all_sprites = pygame.sprite.Group()
        self.player = None  # Será definido após a seleção de personagem
        
        # Mensagem de erro (se houver)
        self.error_message = None
        self.error_timer = 0
        
        # Transição entre mapas
        self.transition_cooldown = 0
        
        # Trilha sonora atual
        self.current_soundtrack = None
        
        # Flag para controlar o loop principal
        self.running = True
    
    def start_game(self, character_data=None):
        """Inicia um novo jogo"""
        try:
            # Carrega o mapa inicial
            self.current_map_id = "map1"
            self.map = Map(self.current_map_id)
            
            # Verifica se o mapa foi carregado corretamente
            if self.map.id == "error":
                print("Aviso: Mapa inicial não pôde ser carregado corretamente.")
                self.show_error("Erro ao carregar o mapa inicial. Verifique os arquivos do jogo.")
            
            # Cria o jogador
            self.all_sprites.empty()
            self.player = Player(self.WIDTH // 2, self.HEIGHT // 2, character_data)
            self.all_sprites.add(self.player)
            
            # Inicia a trilha sonora do mapa
            self.play_map_soundtrack()
            
            # Muda para o estado de jogo
            self.game_state.change_state(GameState.PLAYING)
        except Exception as e:
            print(f"Erro ao iniciar o jogo: {e}")
            self.show_error("Erro ao iniciar o jogo. Verifique os arquivos do jogo.")
    
    def play_map_soundtrack(self):
        """Toca a trilha sonora do mapa atual"""
        soundtrack_path = self.map.get_soundtrack_path()
        
        # Se não há trilha sonora definida, não faz nada
        if not soundtrack_path:
            return
            
        # Verifica se o arquivo existe
        full_path = os.path.join("assets", "sounds", soundtrack_path)
        if not os.path.exists(full_path):
            print(f"Aviso: Arquivo de áudio não encontrado: {full_path}")
            # Não tenta criar o arquivo nem tocar a trilha
            return
            
        # Se a trilha sonora for a mesma que já está tocando, não faz nada
        if self.current_soundtrack == soundtrack_path:
            return
            
        # Para a trilha sonora atual se houver
        try:
            if pygame.mixer.music.get_busy() and self.current_soundtrack != soundtrack_path:
                pygame.mixer.music.stop()
        except Exception as e:
            print(f"Aviso: Erro ao parar trilha sonora: {e}")
            
        # Carrega e toca a nova trilha sonora
        try:
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play(-1)  # Loop infinito
            self.current_soundtrack = soundtrack_path
        except Exception as e:
            print(f"Aviso: Não foi possível tocar trilha sonora {full_path}: {e}")
            # Se ocorrer um erro, define a trilha atual como None para evitar problemas
            self.current_soundtrack = None
            # Continua a execução do jogo normalmente
    
    def process_events(self):
        """Processa os eventos (teclado, mouse, etc)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            # Processa eventos com base no estado atual do jogo
            if self.game_state.is_title_screen():
                action = self.title_screen.handle_event(event)
                if action == "start_game":
                    self.game_state.change_state(GameState.CHARACTER_SELECT)
                elif action == "quit":
                    self.running = False
                    return
            
            elif self.game_state.is_character_select():
                character_data = self.character_select.handle_event(event)
                if character_data:
                    self.start_game(character_data)
                
                # ESC volta para a tela de título
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.game_state.change_state(GameState.TITLE_SCREEN)
            
            elif self.game_state.is_playing():
                # ESC pausa o jogo
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.game_state.change_state(GameState.PAUSED)
                else:
                    # Passa o evento para o jogador
                    self.player.handle_event(event)
            
            elif self.game_state.is_paused():
                action = self.pause_screen.handle_event(event)
                if action == "resume":
                    self.game_state.change_state(GameState.PLAYING)
                elif action == "menu":
                    self.game_state.change_state(GameState.TITLE_SCREEN)
                elif action == "quit":
                    self.running = False
                    return
    
    def update(self):
        """Atualiza todos os objetos do jogo"""
        # Atualiza o cooldown de transição
        if self.transition_cooldown > 0:
            self.transition_cooldown -= 1
        
        # Atualiza o timer de erro
        if self.error_timer > 0:
            self.error_timer -= 1
            if self.error_timer <= 0:
                self.error_message = None
        
        # Atualiza apenas se estiver jogando
        if self.game_state.is_playing():
            self.all_sprites.update()
            
            # Verifica colisões com o mapa
            self.map.check_collision(self.player)
            
            # Limita o jogador aos limites do mapa
            map_width = self.map.width * self.map.tile_size
            map_height = self.map.height * self.map.tile_size
            self.player.constrain_to_map(map_width, map_height)
            
            # Verifica interação com portas
            if self.player.interacting and self.transition_cooldown == 0:
                portal = self.map.check_door_interaction(self.player)
                if portal:
                    self.change_map(portal["target_map"], portal["target_x"], portal["target_y"])
                    self.player.interacting = False
                else:
                    # Verifica interação com outros objetos
                    obj = self.map.check_object_interaction(self.player)
                    if obj:
                        # Processa a interação com o objeto
                        self.process_object_interaction(obj)
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
            
            # Guarda a trilha sonora atual
            previous_soundtrack = self.current_soundtrack
            
            # Carrega o novo mapa
            self.current_map_id = map_id
            self.map = Map(map_id)
            
            # Posiciona o jogador
            self.player.rect.x = player_x * self.map.tile_size
            self.player.rect.y = player_y * self.map.tile_size
            
            # Atualiza a trilha sonora
            self.play_map_soundtrack()
            
            # Define um cooldown para evitar transições múltiplas
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
        # Renderiza com base no estado atual do jogo
        if self.game_state.is_title_screen():
            self.title_screen.draw(self.screen)
        
        elif self.game_state.is_character_select():
            self.character_select.draw(self.screen)
        
        elif self.game_state.is_playing() or self.game_state.is_paused():
            # Preenche o fundo com cor preta
            self.screen.fill((0, 0, 0))
            
            # Desenha o mapa
            self.map.draw(self.screen)
            
            # Desenha todos os sprites
            self.all_sprites.draw(self.screen)
            
            # Desenha informações do mapa atual
            font = pygame.font.SysFont(None, 24)
            map_text = font.render(f"Mapa: {self.map.name}", True, (255, 255, 255))
            self.screen.blit(map_text, (10, 10))
            
            # Desenha informações do personagem
            if self.player:
                player_text = font.render(f"Personagem: {self.player.name}", True, (255, 255, 255))
                self.screen.blit(player_text, (10, 40))
            
            # Desenha instruções
            instructions = font.render("Use WASD ou setas para mover, E para interagir com portas, ESC para pausar", True, (255, 255, 255))
            self.screen.blit(instructions, (10, self.HEIGHT - 30))
            
            # Desenha mensagem de erro, se houver
            if self.error_message:
                # Cria um fundo semi-transparente
                error_bg = pygame.Surface((self.WIDTH, 60))
                error_bg.fill((200, 0, 0))
                error_bg.set_alpha(200)
                self.screen.blit(error_bg, (0, self.HEIGHT // 2 - 30))
                
                # Desenha a mensagem de erro
                error_text = font.render(f"ERRO: {self.error_message}", True, (255, 255, 255))
                error_rect = error_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
                self.screen.blit(error_text, error_rect)
            
            # Se estiver pausado, desenha a tela de pausa por cima
            if self.game_state.is_paused():
                self.pause_screen.draw(self.screen)
        
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

    def process_object_interaction(self, obj):
        """Processa a interação com um objeto"""
        obj_id = str(obj.get("id", 0))
        details = obj.get("details", {})
        
        # Verifica o tipo de objeto e processa de acordo
        if obj_id in self.map.item_config.get("tile_types", {}):
            item_config = self.map.item_config["tile_types"][obj_id]
            item_type = item_config.get("type", "")
            
            # Processa baús
            if item_type == "objeto" and "chest" in item_config.get("name", "").lower():
                # Mostra mensagem sobre os itens encontrados
                drops = details.get("drops", [])
                if drops:
                    drop_names = []
                    for drop in drops:
                        drop_id = drop.replace("item_", "")
                        if drop_id in self.map.item_config.get("tile_types", {}):
                            drop_names.append(self.map.item_config["tile_types"][drop_id].get("name", "Item desconhecido"))
                    
                    if drop_names:
                        self.show_error(f"Você encontrou: {', '.join(drop_names)}")
            
            # Processa NPCs
            elif item_type == "npc":
                # Mostra diálogo do NPC
                dialog = details.get("dialog", "...")
                if dialog:
                    self.show_error(dialog)
            
            # Processa placas
            elif "sign" in item_config.get("name", "").lower():
                # Mostra mensagem da placa
                message = details.get("message", "")
                if message:
                    self.show_error(message) 