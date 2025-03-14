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
        self.BASE_WIDTH = 800
        self.BASE_HEIGHT = 600
        self.FPS = 60
        self.TITLE = "Jogo Top-Down"
        
        # Carrega o mapa inicial para obter suas dimensões
        self.current_map_id = "map1"
        self.map = Map(self.current_map_id)
        
        # Ajusta o tamanho da tela com base no tamanho do mapa
        self.WIDTH = min(1280, self.map.width * self.map.tile_size)
        self.HEIGHT = min(960, self.map.height * self.map.tile_size)
        
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
        
        # Carrega objetos do jogo
        self.all_sprites = pygame.sprite.Group()
        self.player = None  # Será definido após a seleção de personagem
        
        # Mensagem de erro (se houver)
        self.error_message = None
        self.error_timer = 0
        self.error_item_id = None  # ID do item que gerou a mensagem
        self.error_is_dialog = False  # Indica se é um diálogo (não um erro)
        
        # Controle de colisão
        self.last_collision_time = 0
        self.collision_message_cooldown = 60  # 1 segundo a 60 FPS
        self.last_collision_state = False  # Estado da última colisão
        self.collision_log_counter = 0
        self.collision_log_frequency = 120  # Só mostra log a cada 120 frames (aproximadamente 2 segundos)
        
        # Opções de depuração
        self.show_hitbox = False
        
        # Transição entre mapas
        self.transition_cooldown = 0
        
        # Trilha sonora atual
        self.current_soundtrack = None
        self.soundtrack_warnings_shown = []  # Lista para controlar quais avisos já foram exibidos
        
        # Flag para controlar o loop principal
        self.running = True
        
        # Inicializa o jogo
        self.init_game()
    
    def init_game(self):
        """Inicializa o jogo"""
        try:
            # Carrega o mapa inicial
            self.current_map_id = "map1"
            self.map = Map(self.current_map_id)
            
            # Verifica se o mapa foi carregado corretamente
            if self.map.id == "error":
                print("Aviso: Mapa inicial não pôde ser carregado corretamente.")
                self.show_error("Erro ao carregar o mapa inicial. Verifique os arquivos do jogo.")
            
            # Inicia a trilha sonora do mapa
            self.play_map_soundtrack()
        except Exception as e:
            print(f"Erro ao inicializar o jogo: {e}")
            self.show_error(f"Erro ao inicializar o jogo: {e}")
    
    def start_game(self, character_data=None):
        """Inicia um novo jogo"""
        try:
            # Cria o jogador
            self.all_sprites.empty()
            self.player = Player(self.WIDTH // 2, self.HEIGHT // 2, character_data)
            self.all_sprites.add(self.player)
            
            # Muda o estado do jogo para "jogando"
            self.game_state.change_state(GameState.PLAYING)
            
            # Inicia a trilha sonora do mapa
            self.play_map_soundtrack()
        except Exception as e:
            print(f"Erro ao iniciar o jogo: {e}")
            self.show_error(f"Erro ao iniciar o jogo: {e}")
    
    def play_map_soundtrack(self):
        """Toca a trilha sonora do mapa atual"""
        soundtrack_path = self.map.get_soundtrack_path()
        
        # Se não há trilha sonora definida, não faz nada
        if not soundtrack_path:
            return
            
        # Verifica se o arquivo existe
        full_path = os.path.join("assets", "sounds", soundtrack_path)
        if not os.path.exists(full_path):
            # Evita mostrar o mesmo aviso várias vezes
            if full_path not in self.soundtrack_warnings_shown:
                print(f"Aviso: Arquivo de áudio não encontrado: {full_path}")
                self.soundtrack_warnings_shown.append(full_path)
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
            # Evita mostrar o mesmo aviso várias vezes
            if "stop_soundtrack" not in self.soundtrack_warnings_shown:
                print(f"Aviso: Erro ao parar trilha sonora: {e}")
                self.soundtrack_warnings_shown.append("stop_soundtrack")
            
        # Carrega e toca a nova trilha sonora
        try:
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play(-1)  # Loop infinito
            self.current_soundtrack = soundtrack_path
        except Exception as e:
            # Evita mostrar o mesmo aviso várias vezes
            if full_path not in self.soundtrack_warnings_shown:
                print(f"Aviso: Não foi possível tocar trilha sonora {full_path}: {e}")
                self.soundtrack_warnings_shown.append(full_path)
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state.change_state(GameState.PAUSED)
                    elif event.key == pygame.K_i:
                        # Abre o inventário
                        self.show_inventory()
                
                # Passa os eventos para o jogador
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
            
            elif self.game_state.is_dialog():
                # Diálogo simples (não interativo)
                # Qualquer tecla fecha o diálogo
                if event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    self.close_dialog()
            
            elif self.game_state.is_interactive_dialog():
                # Diálogo interativo
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.close_dialog()
                    # Teclas numéricas para selecionar opções
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                        option_index = event.key - pygame.K_1  # 0-indexed
                        if hasattr(self, 'dialog_options') and option_index < len(self.dialog_options):
                            # Chama o callback se existir
                            if hasattr(self, 'dialog_callback') and self.dialog_callback:
                                self.dialog_callback(option_index)
                            else:
                                self.close_dialog()
                    # Navegar entre opções com setas
                    elif event.key == pygame.K_UP:
                        if hasattr(self, 'dialog_options') and self.dialog_options:
                            if not hasattr(self, 'selected_option'):
                                self.selected_option = 0
                            self.selected_option = (self.selected_option - 1) % len(self.dialog_options)
                    elif event.key == pygame.K_DOWN:
                        if hasattr(self, 'dialog_options') and self.dialog_options:
                            if not hasattr(self, 'selected_option'):
                                self.selected_option = 0
                            self.selected_option = (self.selected_option + 1) % len(self.dialog_options)
                    # Selecionar opção atual com ENTER
                    elif event.key == pygame.K_RETURN:
                        if hasattr(self, 'dialog_options') and hasattr(self, 'selected_option'):
                            if self.selected_option < len(self.dialog_options):
                                # Chama o callback se existir
                                if hasattr(self, 'dialog_callback') and self.dialog_callback:
                                    self.dialog_callback(self.selected_option)
                                else:
                                    self.close_dialog()
            
            elif self.game_state.is_inventory():
                # Inventário do jogador
                # ESC ou tecla I fecha o inventário
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_i:
                        self.close_dialog()
                        print("Fechando inventário...")
            
            elif self.game_state.is_shopping():
                # Processo de compra
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Cancela a compra
                        self.close_dialog()
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                        # Seleciona um item pelo número
                        item_index = event.key - pygame.K_1  # 0-indexed
                        if hasattr(self, 'current_shop_items') and item_index < len(self.current_shop_items):
                            self.buy_item(item_index)
                    # Navegar entre itens com setas
                    elif event.key == pygame.K_UP:
                        if hasattr(self, 'current_shop_items') and self.current_shop_items:
                            if not hasattr(self, 'selected_option'):
                                self.selected_option = 0
                            self.selected_option = (self.selected_option - 1) % len(self.current_shop_items)
                    elif event.key == pygame.K_DOWN:
                        if hasattr(self, 'current_shop_items') and self.current_shop_items:
                            if not hasattr(self, 'selected_option'):
                                self.selected_option = 0
                            self.selected_option = (self.selected_option + 1) % len(self.current_shop_items)
                    # Comprar item selecionado com ENTER
                    elif event.key == pygame.K_RETURN:
                        if hasattr(self, 'current_shop_items') and hasattr(self, 'selected_option'):
                            if self.selected_option < len(self.current_shop_items):
                                self.buy_item(self.selected_option)
            
            elif self.game_state.is_selling():
                # Processo de venda
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Cancela a venda
                        self.close_dialog()
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                        # Seleciona um item pelo número
                        item_index = event.key - pygame.K_1  # 0-indexed
                        if hasattr(self, 'sellable_items') and item_index < len(self.sellable_items):
                            self.sell_item(item_index)
                    # Navegar entre itens com setas
                    elif event.key == pygame.K_UP:
                        if hasattr(self, 'sellable_items') and self.sellable_items:
                            if not hasattr(self, 'selected_option'):
                                self.selected_option = 0
                            self.selected_option = (self.selected_option - 1) % len(self.sellable_items)
                    elif event.key == pygame.K_DOWN:
                        if hasattr(self, 'sellable_items') and self.sellable_items:
                            if not hasattr(self, 'selected_option'):
                                self.selected_option = 0
                            self.selected_option = (self.selected_option + 1) % len(self.sellable_items)
                    # Vender item selecionado com ENTER
                    elif event.key == pygame.K_RETURN:
                        if hasattr(self, 'sellable_items') and hasattr(self, 'selected_option'):
                            if self.selected_option < len(self.sellable_items):
                                self.sell_item(self.selected_option)
            
            # Eventos de teclado
            elif event.type == pygame.KEYDOWN:
                # Tecla ESC para pausar/despausar
                if event.key == pygame.K_ESCAPE:
                    if self.game_state.is_playing():
                        self.game_state.change_state(GameState.PAUSED)
                    elif self.game_state.is_paused():
                        self.game_state.change_state(GameState.PLAYING)
                
                # Tecla H para mostrar/esconder hitbox (modo de depuração)
                elif event.key == pygame.K_h:
                    self.show_hitbox = not self.show_hitbox
                    print(f"Hitbox {'visível' if self.show_hitbox else 'oculta'}")
    
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
            # Atualiza os sprites (calcula velocidade, mas não move o jogador)
            self.all_sprites.update()
            
            # Move o jogador considerando colisões
            if self.player:
                collision = self.player.move_with_collision(self.map.collision_rects)
                
                # Registra a colisão no log apenas quando o estado muda e com frequência limitada
                if collision != self.last_collision_state:
                    self.collision_log_counter += 1
                    if self.collision_log_counter >= self.collision_log_frequency:
                        if collision:
                            print("Log: Colisão detectada - Caminho bloqueado")
                        else:
                            print("Log: Caminho livre")
                        self.collision_log_counter = 0
                    self.last_collision_state = collision
            
            # Verifica transições de borda ANTES de restringir o jogador
            if self.transition_cooldown == 0:
                edge_transition = self.map.check_edge_transition(self.player)
                if edge_transition:
                    self.change_map(edge_transition["target_map"], edge_transition["target_x"], edge_transition["target_y"])
                    # Retorna para não continuar processando o resto do frame após a transição
                    return
            
            # Limita o jogador aos limites do mapa apenas se não houve transição
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
            
            # Ajusta o tamanho da tela para o novo mapa
            self.adjust_screen_size()
            
            # Posiciona o jogador
            # Verifica se as coordenadas já estão em pixels ou em unidades de tile
            if isinstance(player_x, int) and player_x < 100 and isinstance(player_y, int) and player_y < 100:
                # Coordenadas em unidades de tile, converte para pixels
                self.player.rect.x = player_x * self.map.tile_size
                self.player.rect.y = player_y * self.map.tile_size
            else:
                # Coordenadas já em pixels
                self.player.rect.x = player_x
                self.player.rect.y = player_y
            
            # Atualiza a hitbox do jogador
            self.player.update_hitbox()
            
            # Atualiza a trilha sonora
            self.play_map_soundtrack()
            
            # Define um cooldown para evitar transições múltiplas
            self.transition_cooldown = 10
        except Exception as e:
            self.show_error(f"Erro ao mudar de mapa: {e}")
    
    def adjust_screen_size(self):
        """Ajusta o tamanho da tela com base no tamanho do mapa atual"""
        # Calcula o tamanho ideal da tela com base no mapa
        map_width = self.map.width * self.map.tile_size
        map_height = self.map.height * self.map.tile_size
        
        print(f"Tamanho do mapa: {self.map.width}x{self.map.height} tiles")
        print(f"Tamanho do tile: {self.map.tile_size}px")
        print(f"Tamanho do mapa em pixels: {map_width}x{map_height}")
        
        # Limita o tamanho máximo da tela para evitar janelas muito grandes
        new_width = min(1280, map_width)
        new_height = min(960, map_height)
        
        # Verifica se o tamanho da tela precisa ser alterado
        if new_width != self.WIDTH or new_height != self.HEIGHT:
            self.WIDTH = new_width
            self.HEIGHT = new_height
            
            # Redimensiona a tela
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            
            # Atualiza as telas do jogo
            self.title_screen = TitleScreen(self.WIDTH, self.HEIGHT)
            self.character_select = CharacterSelect(self.WIDTH, self.HEIGHT)
            self.pause_screen = PauseScreen(self.WIDTH, self.HEIGHT)
            
            print(f"Tela redimensionada para {self.WIDTH}x{self.HEIGHT}")
        else:
            print(f"Tamanho da tela mantido em {self.WIDTH}x{self.HEIGHT}")
    
    def show_error(self, message, item_id=None, is_dialog=False):
        """Mostra uma mensagem de erro temporária"""
        if is_dialog:
            print(f"DIÁLOGO: {message}")
        else:
            print(f"ERRO: {message}")
        
        self.error_message = message
        self.error_item_id = item_id
        self.error_is_dialog = is_dialog
        self.error_timer = 180  # 3 segundos a 60 FPS
    
    def show_dialog(self, message, item_id=None, interactive=False, options=None, callback=None):
        """Mostra uma janela de diálogo que pausa o jogo
        
        Parâmetros:
        - message: O texto a ser exibido
        - item_id: ID do item associado (para exibir sua imagem)
        - interactive: Se True, requer interação do usuário
        - options: Lista de opções para diálogos interativos
        - callback: Função a ser chamada quando o usuário fizer uma escolha
        """
        print(f"DIÁLOGO: {message}")
        
        # Salva o estado anterior
        self.previous_game_state = self.game_state.current_state
        
        # Armazena as informações do diálogo
        self.dialog_message = message
        self.dialog_item_id = item_id
        self.dialog_options = options or []
        self.dialog_callback = callback
        
        # Reseta a opção selecionada
        self.selected_option = 0
        
        # Define o estado do jogo de acordo com o tipo de diálogo
        if interactive:
            self.game_state.change_state(GameState.INTERACTIVE_DIALOG)
        else:
            self.game_state.change_state(GameState.DIALOG)
    
    def close_dialog(self):
        """Fecha o diálogo atual e retorna ao estado anterior"""
        print(f"Fechando diálogo...")
        
        # Limpa as informações do diálogo
        self.dialog_message = None
        self.dialog_item_id = None
        self.dialog_options = []
        self.dialog_callback = None
        self.current_shop_items = []
        self.sellable_items = []
        
        # Reseta a opção selecionada
        self.selected_option = 0
        
        # Volta ao estado anterior
        if hasattr(self, 'previous_game_state') and self.previous_game_state is not None:
            previous = self.previous_game_state
            self.previous_game_state = None
            self.game_state.change_state(previous)
            
            # Verifica se ainda está no estado de diálogo após a mudança
            # (isso pode acontecer se o estado anterior também era um diálogo)
            if self.game_state.is_any_dialog():
                print("Aviso: Ainda em estado de diálogo após close_dialog(). Forçando estado PLAYING.")
                self.game_state.change_state(GameState.PLAYING)
    
    def render(self):
        """Renderiza os objetos na tela"""
        # Renderiza com base no estado atual do jogo
        if self.game_state.is_title_screen():
            self.title_screen.draw(self.screen)
        
        elif self.game_state.is_character_select():
            self.character_select.draw(self.screen)
        
        elif self.game_state.is_playing() or self.game_state.is_paused() or self.game_state.is_any_dialog():
            # Preenche o fundo com cor preta
            self.screen.fill((0, 0, 0))
            
            # Desenha o mapa
            self.map.draw(self.screen)
            
            # Desenha todos os sprites
            self.all_sprites.draw(self.screen)
            
            # Desenha a hitbox do jogador se a opção estiver ativada
            if self.show_hitbox and self.player:
                self.player.draw_hitbox(self.screen)
            
            # Desenha informações do mapa atual
            font = pygame.font.SysFont(None, 24)
            map_text = font.render(f"Mapa: {self.map.name}", True, (255, 255, 255))
            self.screen.blit(map_text, (10, 10))
            
            # Desenha informações do personagem
            if self.player:
                player_text = font.render(f"Personagem: {self.player.name}", True, (255, 255, 255))
                coins_text = font.render(f"Moedas: {self.player.coins}", True, (255, 215, 0))  # Cor dourada
                
                self.screen.blit(player_text, (10, 40))
                self.screen.blit(coins_text, (10, 70))
                
                # Desenha o inventário (apenas o número de itens por enquanto)
                if hasattr(self.player, 'inventory'):
                    inventory_text = font.render(f"Itens: {len(self.player.inventory)}", True, (255, 255, 255))
                    self.screen.blit(inventory_text, (10, 100))
            
            # Desenha instruções
            instructions = font.render("Use WASD ou setas para mover, E para interagir com portas, ESC para pausar", True, (255, 255, 255))
            instructions2 = font.render("I para abrir inventário, números 1-9 para comprar itens em lojas", True, (255, 255, 255))
            self.screen.blit(instructions, (10, self.HEIGHT - 50))
            self.screen.blit(instructions2, (10, self.HEIGHT - 25))
            
            # Se estiver em qualquer tipo de diálogo, desenha um overlay semi-transparente
            if self.game_state.is_any_dialog():
                # Cria um overlay para ofuscar o fundo
                overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
                overlay.fill((0, 0, 0))  # Preto
                overlay.set_alpha(150)  # Semi-transparente (0-255)
                self.screen.blit(overlay, (0, 0))
                
                # Desenha a janela de diálogo apropriada
                if self.game_state.is_inventory():
                    self.render_inventory()
                else:
                    self.render_dialog()
            
            # Desenha mensagem de erro, se houver
            elif self.error_message and not self.error_is_dialog:
                # Mensagem de erro (estilo antigo)
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

    def render_inventory(self):
        """Renderiza a interface do inventário em estilo tela cheia"""
        # Define a fonte e cores
        title_font = pygame.font.SysFont(None, 36)
        font = pygame.font.SysFont(None, 24)
        small_font = pygame.font.SysFont(None, 20)
        
        # Cores para a interface do inventário
        bg_color = (40, 40, 60)  # Azul escuro
        border_color = (80, 80, 120)  # Azul médio
        title_color = (220, 220, 255)  # Azul claro
        text_color = (255, 255, 255)  # Branco
        highlight_color = (255, 215, 0)  # Dourado
        
        # Calcula o tamanho da janela (quase tela cheia, mas com margens)
        margin = 50
        window_width = self.WIDTH - (margin * 2)
        window_height = self.HEIGHT - (margin * 2)
        window_x = margin
        window_y = margin
        
        # Desenha o fundo da janela
        pygame.draw.rect(self.screen, bg_color, 
                         (window_x, window_y, window_width, window_height), 0)
        pygame.draw.rect(self.screen, border_color, 
                         (window_x, window_y, window_width, window_height), 4)
        
        # Cria um gradiente suave para o fundo interior
        inner_bg = pygame.Surface((window_width - 8, window_height - 8))
        inner_bg.fill((50, 50, 70))
        for i in range(100):
            alpha = 50 + i
            line = pygame.Surface((window_width - 8, 2))
            line.fill((60, 60, 80))
            line.set_alpha(alpha)
            inner_bg.blit(line, (0, i * 2))
        self.screen.blit(inner_bg, (window_x + 4, window_y + 4))
        
        # Desenha o título "INVENTÁRIO"
        title_text = title_font.render("INVENTÁRIO", True, title_color)
        title_rect = title_text.get_rect(midtop=(window_x + window_width // 2, window_y + 15))
        
        # Adiciona um fundo para o título
        title_bg = pygame.Surface((title_text.get_width() + 40, title_text.get_height() + 10))
        title_bg.fill(bg_color)
        title_bg.set_alpha(200)
        self.screen.blit(title_bg, (title_rect.x - 20, title_rect.y - 5))
        
        # Desenha a borda do título
        pygame.draw.rect(self.screen, border_color, 
                         (title_rect.x - 20, title_rect.y - 5, 
                          title_text.get_width() + 40, title_text.get_height() + 10), 2)
        
        # Desenha o texto do título
        self.screen.blit(title_text, title_rect)
        
        # Mostra o total de moedas
        coins_text = font.render(f"Moedas: {self.player.coins}", True, highlight_color)
        coins_rect = coins_text.get_rect(topright=(window_x + window_width - 20, window_y + 20))
        self.screen.blit(coins_text, coins_rect)
        
        # Verifica se o inventário está vazio
        if not hasattr(self.player, 'inventory') or not self.player.inventory:
            empty_text = font.render("Seu inventário está vazio.", True, text_color)
            empty_rect = empty_text.get_rect(center=(window_x + window_width // 2, window_y + window_height // 2))
            self.screen.blit(empty_text, empty_rect)
            
            # Instruções para fechar
            close_text = small_font.render("Pressione ESC ou I para fechar o inventário", True, (180, 180, 180))
            close_rect = close_text.get_rect(midbottom=(window_x + window_width // 2, window_y + window_height - 15))
            self.screen.blit(close_text, close_rect)
            return
        
        # Calcula itens únicos e suas quantidades
        item_counts = {}
        for item_id in self.player.inventory:
            item_counts[item_id] = item_counts.get(item_id, 0) + 1
        
        # Define a área de listagem de itens
        list_x = window_x + 30
        list_y = window_y + 70
        list_width = window_width - 60
        list_height = window_height - 100
        
        # Desenha uma borda para a área da lista
        pygame.draw.rect(self.screen, border_color, 
                         (list_x - 5, list_y - 5, list_width + 10, list_height + 10), 2)
        
        # Define o tamanho de cada item na lista
        item_height = 60
        item_spacing = 10
        max_visible_items = (list_height) // (item_height + item_spacing)
        
        # Prepara para renderizar os itens
        current_y = list_y
        item_index = 0
        
        # Renderiza cada item no inventário
        for item_id, count in item_counts.items():
            if item_index >= max_visible_items:
                break
                
            item_num_id = item_id.replace("item_", "")
            
            if item_num_id in self.map.item_config.get("tile_types", {}):
                item_config = self.map.item_config["tile_types"][item_num_id]
                item_name = item_config.get("name", "Item desconhecido")
                item_description = item_config.get("description", "Sem descrição disponível")
                
                # Cria um fundo para o item atual
                item_bg = pygame.Surface((list_width, item_height))
                item_bg.fill((60, 60, 80))
                item_bg.set_alpha(150)
                self.screen.blit(item_bg, (list_x, current_y))
                
                # Desenha a borda do item
                pygame.draw.rect(self.screen, (100, 100, 150), 
                                (list_x, current_y, list_width, item_height), 1)
                
                # Desenha o ícone do item (se disponível)
                icon_size = 48
                icon_x = list_x + 10
                icon_y = current_y + (item_height - icon_size) // 2
                
                if item_num_id in self.map.images:
                    # Usa a imagem existente
                    item_image = self.map.images[item_num_id]
                    icon_rect = pygame.Rect(icon_x, icon_y, icon_size, icon_size)
                    self.screen.blit(item_image, icon_rect)
                else:
                    # Cria um ícone colorido baseado no tipo do item
                    icon_color = item_config.get("color", (255, 255, 255))
                    pygame.draw.rect(self.screen, icon_color, 
                                    (icon_x, icon_y, icon_size, icon_size), 0)
                    pygame.draw.rect(self.screen, (0, 0, 0), 
                                    (icon_x, icon_y, icon_size, icon_size), 1)
                
                # Desenha o nome do item
                name_text = font.render(f"{item_name} (x{count})", True, text_color)
                self.screen.blit(name_text, (list_x + icon_size + 25, current_y + 10))
                
                # Desenha a descrição do item
                desc_text = small_font.render(item_description, True, (200, 200, 200))
                self.screen.blit(desc_text, (list_x + icon_size + 25, current_y + 35))
                
                # Atualiza a posição Y para o próximo item
                current_y += item_height + item_spacing
                item_index += 1
        
        # Instruções para fechar
        close_text = small_font.render("Pressione ESC ou I para fechar o inventário", True, (180, 180, 180))
        close_rect = close_text.get_rect(midbottom=(window_x + window_width // 2, window_y + window_height - 15))
        self.screen.blit(close_text, close_rect)
    
    def render_dialog(self):
        """Renderiza a janela de diálogo com base no estado atual"""
        # Define o estilo do diálogo com base no tipo
        font = pygame.font.SysFont(None, 24)
        
        # Diferentes estilos para diferentes tipos de diálogo
        if self.game_state.is_shopping():
            # Estilo para diálogo de compra (mais largo e com mais linhas)
            dialog_width = min(650, self.WIDTH - 100)
            dialog_height = 200
            bg_color = (50, 70, 120)  # Azul escuro
            border_color = (80, 100, 180)  # Azul médio
            text_color = (255, 255, 255)  # Branco
            
            # Usa a mensagem armazenada para mostrar os itens à venda
            message = self.dialog_message if hasattr(self, 'dialog_message') else "O que deseja comprar?"
            item_id = self.dialog_item_id if hasattr(self, 'dialog_item_id') else None
        
        elif self.game_state.is_interactive_dialog():
            # Estilo para diálogo interativo (médio, com opções)
            dialog_width = min(600, self.WIDTH - 100)
            dialog_height = 180
            bg_color = (70, 120, 50)  # Verde escuro
            border_color = (100, 180, 80)  # Verde médio
            text_color = (255, 255, 255)  # Branco
            
            # Usa a mensagem armazenada para mostrar as opções
            message = self.dialog_message if hasattr(self, 'dialog_message') else "Escolha uma opção:"
            item_id = self.dialog_item_id if hasattr(self, 'dialog_item_id') else None
        
        else:  # Diálogo normal
            # Estilo para diálogo normal (menor e simples)
            dialog_width = min(550, self.WIDTH - 100)
            dialog_height = 150
            bg_color = (100, 100, 200)  # Azul claro
            border_color = (50, 50, 150)  # Azul escuro
            text_color = (0, 0, 0)  # Preto
            
            # Usa a mensagem armazenada
            message = self.dialog_message if hasattr(self, 'dialog_message') else "..."
            item_id = self.dialog_item_id if hasattr(self, 'dialog_item_id') else None
        
        # Verifica se a mensagem não é None antes de continuar
        if message is None:
            message = "..."  # Define uma mensagem padrão para evitar erros
        
        # Posição do diálogo (centralizado na tela)
        dialog_x = (self.WIDTH - dialog_width) // 2
        dialog_y = (self.HEIGHT - dialog_height) // 2
        
        # Cria o fundo e a borda do diálogo
        pygame.draw.rect(self.screen, bg_color, 
                         (dialog_x, dialog_y, dialog_width, dialog_height), 0)
        pygame.draw.rect(self.screen, border_color, 
                         (dialog_x, dialog_y, dialog_width, dialog_height), 3)
        
        # Cria um fundo para o conteúdo do diálogo
        dialog_bg = pygame.Surface((dialog_width - 6, dialog_height - 6))
        dialog_bg.fill((240, 240, 255))
        dialog_bg.set_alpha(230)
        self.screen.blit(dialog_bg, (dialog_x + 3, dialog_y + 3))
        
        # Desenha a imagem do item, se disponível
        if item_id and item_id in self.map.images:
            item_image = self.map.images[item_id]
            item_rect = pygame.Rect(dialog_x + 15, dialog_y + 15, 48, 48)  # Imagem um pouco maior
            self.screen.blit(item_image, item_rect)
            text_x = dialog_x + 75
            text_width = dialog_width - 90
        else:
            text_x = dialog_x + 15
            text_width = dialog_width - 30
        
        # Renderiza o texto com quebra de linha
        words = message.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            if word == '\n':
                # Força quebra de linha
                lines.append(' '.join(current_line))
                current_line = []
                continue
                
            test_line = ' '.join(current_line + [word])
            test_text = font.render(test_line, True, text_color)
            
            if test_text.get_width() <= text_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Limita o número de linhas com base no tipo de diálogo
        max_lines = 7 if self.game_state.is_shopping() else (6 if self.game_state.is_interactive_dialog() else 5)
        lines = lines[:max_lines]
        
        # Desenha as linhas de texto
        for i, line in enumerate(lines):
            text = font.render(line, True, text_color)
            self.screen.blit(text, (text_x, dialog_y + 20 + i * 25))
        
        # Renderiza as opções com indicador de seleção para diálogos interativos ou compra/venda
        if self.game_state.is_interactive_dialog() and hasattr(self, 'dialog_options') and self.dialog_options:
            options_y = dialog_y + dialog_height - 80
            
            # Certifica-se de que selected_option existe e está dentro dos limites
            if not hasattr(self, 'selected_option'):
                self.selected_option = 0
            self.selected_option = min(max(0, self.selected_option), len(self.dialog_options) - 1)
            
            for i, option in enumerate(self.dialog_options):
                option_text = f"{i+1}. {option}"
                
                # Destaca a opção selecionada
                if i == self.selected_option:
                    # Triângulo indicador
                    pygame.draw.polygon(self.screen, (255, 255, 0), [
                        (text_x - 15, options_y + i * 25 + 12),
                        (text_x - 5, options_y + i * 25 + 6),
                        (text_x - 5, options_y + i * 25 + 18)
                    ])
                    
                    # Texto da opção selecionada em negrito ou cor diferente
                    text = font.render(option_text, True, (255, 255, 0))
                else:
                    text = font.render(option_text, True, text_color)
                
                self.screen.blit(text, (text_x, options_y + i * 25))
        
        # Opções de compra
        elif self.game_state.is_shopping() and hasattr(self, 'current_shop_items') and self.current_shop_items:
            # Obtém a opção selecionada para compra
            if not hasattr(self, 'selected_option'):
                self.selected_option = 0
            self.selected_option = min(max(0, self.selected_option), len(self.current_shop_items) - 1)
            
            for i, item_info in enumerate(self.current_shop_items):
                if i == self.selected_option:
                    # Triângulo indicador
                    pygame.draw.polygon(self.screen, (255, 255, 0), [
                        (text_x - 15, dialog_y + 70 + i * 25 + 12),
                        (text_x - 5, dialog_y + 70 + i * 25 + 6),
                        (text_x - 5, dialog_y + 70 + i * 25 + 18)
                    ])
                    text = font.render(f"{i+1}. {item_info}", True, (255, 255, 0))
                else:
                    text = font.render(f"{i+1}. {item_info}", True, text_color)
                self.screen.blit(text, (text_x, dialog_y + 70 + i * 25))
        
        # Opções de venda
        elif self.game_state.is_selling() and hasattr(self, 'sellable_items') and self.sellable_items:
            # Obtém a opção selecionada para venda
            if not hasattr(self, 'selected_option'):
                self.selected_option = 0
            self.selected_option = min(max(0, self.selected_option), len(self.sellable_items) - 1)
            
            for i, item_info in enumerate(self.sellable_items):
                if i == self.selected_option:
                    # Triângulo indicador
                    pygame.draw.polygon(self.screen, (255, 255, 0), [
                        (text_x - 15, dialog_y + 70 + i * 25 + 12),
                        (text_x - 5, dialog_y + 70 + i * 25 + 6),
                        (text_x - 5, dialog_y + 70 + i * 25 + 18)
                    ])
                    text = font.render(f"{i+1}. {item_info}", True, (255, 255, 0))
                else:
                    text = font.render(f"{i+1}. {item_info}", True, text_color)
                self.screen.blit(text, (text_x, dialog_y + 70 + i * 25))
        
        # Adiciona uma instrução no final do diálogo para informar como interagir
        if self.game_state.is_dialog():
            hint_text = font.render("Pressione qualquer tecla para continuar...", True, (100, 100, 100))
            hint_rect = hint_text.get_rect(bottomright=(dialog_x + dialog_width - 15, dialog_y + dialog_height - 10))
            self.screen.blit(hint_text, hint_rect)
        elif self.game_state.is_interactive_dialog():
            hint_text = font.render("Use ↑↓ para escolher ou pressione o número da opção", True, (100, 100, 100))
            hint_rect = hint_text.get_rect(bottomright=(dialog_x + dialog_width - 15, dialog_y + dialog_height - 10))
            self.screen.blit(hint_text, hint_rect)
        elif self.game_state.is_shopping():
            hint_text = font.render("Use ↑↓ para escolher ou pressione o número do item", True, (100, 100, 100))
            hint_rect = hint_text.get_rect(bottomright=(dialog_x + dialog_width - 15, dialog_y + dialog_height - 10))
            self.screen.blit(hint_text, hint_rect)
        elif self.game_state.is_selling():
            hint_text = font.render("Use ↑↓ para escolher ou pressione o número do item", True, (100, 100, 100))
            hint_rect = hint_text.get_rect(bottomright=(dialog_x + dialog_width - 15, dialog_y + dialog_height - 10))
            self.screen.blit(hint_text, hint_rect)
    
    def show_inventory(self):
        """Mostra o inventário do jogador com interface aprimorada"""
        # Verifica se o jogador tem um inventário
        if not hasattr(self.player, 'inventory'):
            self.show_dialog("Seu inventário está vazio.", None, interactive=False)
            return
            
        # Salva o estado anterior para poder voltar depois
        self.previous_game_state = self.game_state.current_state
        
        # Muda para o estado de inventário
        self.game_state.change_state(GameState.INVENTORY)
    
    def process_object_interaction(self, obj):
        """Processa a interação com um objeto"""
        obj_id = str(obj.get("id", 0))
        details = obj.get("details", {})
        
        print(f"Processando interação com objeto ID {obj_id}")
        
        # Verifica o tipo de objeto e processa de acordo
        if obj_id in self.map.item_config.get("tile_types", {}):
            item_config = self.map.item_config["tile_types"][obj_id]
            item_type = item_config.get("type", "")
            item_name = item_config.get("name", "Objeto desconhecido")
            
            print(f"Tipo de objeto: {item_type}, Nome: {item_name}")
            
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
                        # Mostra diálogo não interativo
                        self.show_dialog(f"Você encontrou: {', '.join(drop_names)}", obj_id, interactive=False)
                        
                        # Adiciona os itens ao inventário do jogador
                        for drop in drops:
                            self.player.add_item_to_inventory(drop)
            
            # Processa NPCs
            elif item_type == "npc":
                # Verifica se o NPC é uma loja
                is_shop = details.get("shop", False)
                is_buyer = details.get("buyer", False)
                
                if is_shop or is_buyer:
                    # Obtém os itens à venda (se for loja)
                    items_for_sale = details.get("items_for_sale", [])
                    
                    # Se o NPC pode comprar itens, mostra opções de compra e venda
                    if is_shop and is_buyer:
                        self.show_shop_buyer_options(obj_id, items_for_sale, details)
                    # Se o NPC só vende itens
                    elif is_shop:
                        shop_dialog = details.get("dialog", "O que você gostaria de comprar?")
                        self.show_shop_interface(obj_id, items_for_sale, shop_dialog)
                    # Se o NPC só compra itens
                    elif is_buyer:
                        buyer_dialog = details.get("dialog", "Estou interessado em comprar seus itens.")
                        self.show_selling_interface(obj_id, details, buyer_dialog)
                else:
                    # Obtém o diálogo do NPC
                    # Primeiro verifica nos detalhes do objeto no mapa
                    dialog = details.get("dialog", "")
                    
                    # Se não encontrar, verifica nos detalhes da configuração do item
                    if not dialog and "details" in item_config:
                        dialog = item_config["details"].get("dialog", "...")
                    
                    print(f"Diálogo do NPC: {dialog}")
                    
                    # Mostra diálogo do NPC (não interativo)
                    if dialog:
                        self.show_dialog(dialog, obj_id, interactive=False)
                    else:
                        self.show_dialog(f"{item_name} não tem nada a dizer.", obj_id, interactive=False)
            
            # Processa placas
            elif "sign" in item_config.get("name", "").lower():
                # Mostra mensagem da placa
                message = details.get("message", "")
                if message:
                    self.show_dialog(message, obj_id, interactive=False)
    
    def show_shop_interface(self, npc_id, items_for_sale, shop_dialog="O que você gostaria de comprar?"):
        """Mostra a interface da loja"""
        # Se não houver itens à venda, mostra uma mensagem e retorna
        if not items_for_sale:
            self.show_dialog("Desculpe, não tenho itens para vender no momento.")
            return
        
        # Obtém as informações dos itens
        shop_items = []
        current_shop_items_info = []
        
        for item_id in items_for_sale:
            try:
                item_type = item_id.split("_")[0]
                item_number = item_id.split("_")[1]
                
                if item_type == "item":
                    # Verifica se existe no config
                    item_data = self.map.item_config["tile_types"].get(item_number)
                    if not item_data:
                        continue
                    
                    # Obtém o nome e preço
                    item_name = item_data.get("name", f"Item {item_number}")
                    item_price = item_data.get("price", 10)  # Preço padrão se não definido
                    
                    # Adiciona à lista de itens
                    shop_items.append({
                        "id": item_id,
                        "name": item_name,
                        "price": item_price
                    })
                    
                    # Adiciona informação formatada para exibição
                    current_shop_items_info.append(f"{item_name} - {item_price} moedas")
            except Exception as e:
                print(f"Erro ao processar item da loja {item_id}: {e}")
        
        # Se todos os itens foram inválidos, mostra mensagem
        if not shop_items:
            self.show_dialog("Desculpe, não tenho itens válidos para vender no momento.")
            return
        
        # Armazena os itens da loja atual
        self.current_shop_npc = npc_id
        self.current_shop_items = shop_items
        self.current_shop_items_info = current_shop_items_info
        
        # Reseta a opção selecionada
        self.selected_option = 0
        
        # Monta a mensagem da loja
        coins_message = f"Itens à venda (você tem {self.player.coins} moedas):"
        items_message = "\n".join([f"{i+1}. {item_info}" for i, item_info in enumerate(current_shop_items_info)])
        full_message = f"{shop_dialog}\n{coins_message}\n{items_message}\nPressione o número do item para comprar ou ESC para sair."
        
        # Mostra o diálogo da loja
        self.dialog_message = full_message
        self.game_state.change_state(GameState.SHOPPING)
    
    def buy_item(self, item_index):
        """Processa a compra de um item da loja"""
        if not hasattr(self, 'current_shop_items') or not self.current_shop_items:
            return
            
        # Verifica se o índice é válido
        if item_index < 0 or item_index >= len(self.current_shop_items):
            self.show_dialog("Item inválido.", self.current_shop_npc, interactive=False)
            return
            
        # Obtém o item selecionado
        selected_item = self.current_shop_items[item_index]
        
        # Verifica se o jogador tem moedas suficientes
        if self.player.coins >= selected_item["price"]:
            # Remove as moedas do jogador
            self.player.remove_coins(selected_item["price"])
            
            # Adiciona o item ao inventário
            self.player.add_item_to_inventory(selected_item["id"])
            
            # Prepara mensagem de sucesso
            success_message = f"Você comprou {selected_item['name']} por {selected_item['price']} moedas! Agora você tem {self.player.coins} moedas."
            
            # Primeiro fecha o diálogo atual (da loja)
            self.close_dialog()
            
            # Depois mostra a mensagem de sucesso como um novo diálogo
            self.show_dialog(success_message, self.current_shop_npc if hasattr(self, 'current_shop_npc') else None, interactive=False)
        else:
            # Prepara mensagem de erro
            error_message = f"Você não tem moedas suficientes! O item custa {selected_item['price']} moedas e você tem apenas {self.player.coins}."
            
            # Primeiro fecha o diálogo atual (da loja)
            self.close_dialog()
            
            # Depois mostra a mensagem de erro como um novo diálogo
            self.show_dialog(error_message, self.current_shop_npc if hasattr(self, 'current_shop_npc') else None, interactive=False)
    
    def show_shop_buyer_options(self, npc_id, items_for_sale, details):
        """Mostra opções para comprar ou vender itens"""
        # Diálogo introdutório do NPC
        shop_dialog = details.get("dialog", "Posso comprar ou vender itens para você.")
        
        # Prepara as opções
        options = [
            "Quero comprar itens",
            "Quero vender meus itens",
            "Só estou olhando"
        ]
        
        # Mostra diálogo interativo com opções
        self.show_dialog(f"{shop_dialog}\n\nO que você deseja fazer?", npc_id, interactive=True, options=options)
        
        # Guarda informações para uso posterior
        self.current_shop_npc = npc_id
        self.current_shop_items = items_for_sale
        self.current_shop_details = details
        
        # Define o estado do jogo para diálogo interativo
        self.game_state.change_state(GameState.INTERACTIVE_DIALOG)
        
        # Define uma função de callback para processar a escolha do jogador
        self.dialog_callback = self.process_shop_buyer_choice
    
    def process_shop_buyer_choice(self, choice_index):
        """Processa a escolha do jogador para comprar ou vender"""
        if choice_index == 0:  # Comprar
            items_for_sale = self.current_shop_items
            shop_dialog = self.current_shop_details.get("dialog", "O que você gostaria de comprar?")
            self.show_shop_interface(self.current_shop_npc, items_for_sale, shop_dialog)
        elif choice_index == 1:  # Vender
            buyer_dialog = self.current_shop_details.get("buyer_dialog", "O que você gostaria de vender?")
            self.show_selling_interface(self.current_shop_npc, self.current_shop_details, buyer_dialog)
        else:  # Cancelar
            self.close_dialog()
    
    def show_selling_interface(self, npc_id, details, buyer_dialog="O que você gostaria de vender?"):
        """Mostra a interface para vender itens ao NPC"""
        # Obtém os preços de compra do NPC
        buy_prices = details.get("buy_prices", {})
        
        # Se não tiver preços definidos, mostra uma mensagem
        if not buy_prices:
            self.show_dialog("Desculpe, não estou comprando itens no momento.")
            return
        
        # Verifica se o jogador tem itens no inventário
        if not hasattr(self.player, 'inventory') or not self.player.inventory:
            self.show_dialog("Você não tem itens para vender.")
            return
        
        # Conta os itens no inventário para agrupar
        item_counts = {}
        for item in self.player.inventory:
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1
        
        # Filtra apenas os itens que o NPC compra
        sellable_items = []
        sellable_items_info = []
        
        for item_id, count in item_counts.items():
            # Verifica se o NPC compra este item
            if item_id in buy_prices:
                price = buy_prices[item_id]
                
                try:
                    # Obtém informações do item
                    item_type = item_id.split("_")[0]
                    item_number = item_id.split("_")[1]
                    
                    if item_type == "item":
                        # Verifica se existe no config
                        item_data = self.map.item_config["tile_types"].get(item_number)
                        if not item_data:
                            continue
                        
                        # Obtém o nome
                        item_name = item_data.get("name", f"Item {item_number}")
                        
                        # Adiciona à lista de itens vendáveis
                        sellable_items.append({
                            "id": item_id,
                            "name": item_name,
                            "price": price,
                            "count": count
                        })
                        
                        # Adiciona informação formatada para exibição
                        sellable_items_info.append(f"{item_name} (x{count}) - {price} moedas cada")
                except Exception as e:
                    print(f"Erro ao processar item para venda {item_id}: {e}")
        
        # Se o jogador não tiver itens que o NPC compra
        if not sellable_items:
            self.show_dialog("Você não tem itens que eu possa comprar no momento.")
            return
        
        # Armazena os itens vendáveis
        self.current_buyer_npc = npc_id
        self.sellable_items = sellable_items
        self.sellable_items_info = sellable_items_info
        
        # Reseta a opção selecionada
        self.selected_option = 0
        
        # Monta a mensagem de venda
        coins_message = f"Itens para vender (você tem {self.player.coins} moedas):"
        items_message = "\n".join([f"{i+1}. {item_info}" for i, item_info in enumerate(sellable_items_info)])
        full_message = f"{buyer_dialog}\n{coins_message}\n{items_message}\nPressione o número do item para vender ou ESC para sair."
        
        # Mostra o diálogo de venda
        self.dialog_message = full_message
        self.game_state.change_state(GameState.SELLING)
    
    def sell_item(self, item_index):
        """Processa a venda de um item do inventário"""
        if not hasattr(self, 'sellable_items') or not self.sellable_items:
            return
            
        # Verifica se o índice é válido
        if item_index < 0 or item_index >= len(self.sellable_items):
            self.show_dialog("Item inválido.", self.current_buyer_npc, interactive=False)
            return
            
        # Obtém o item selecionado
        selected_item = self.sellable_items[item_index]
        
        # Verifica se o jogador ainda tem este item
        if selected_item["id"] in self.player.inventory:
            # Adiciona as moedas ao jogador
            self.player.add_coins(selected_item["price"])
            
            # Remove o item do inventário
            self.player.remove_item_from_inventory(selected_item["id"])
            
            # Atualiza a contagem do item
            selected_item["count"] -= 1
            if selected_item["count"] <= 0:
                # Remove o item da lista se não houver mais
                self.sellable_items[item_index] = None
            
            # Prepara mensagem de sucesso
            success_message = f"Você vendeu {selected_item['name']} por {selected_item['price']} moedas! Agora você tem {self.player.coins} moedas."
            
            # Primeiro fecha o diálogo atual
            self.close_dialog()
            
            # Depois mostra a mensagem de sucesso como um novo diálogo
            self.show_dialog(success_message, self.current_buyer_npc, interactive=False)
        else:
            # Mensagem de erro se o item não estiver mais disponível
            self.show_dialog("Você não possui mais este item.", self.current_buyer_npc, interactive=False)
    
    def run(self):
        """Loop principal do jogo"""
        while self.running:
            self.process_events()
            self.update()
            self.render()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit() 