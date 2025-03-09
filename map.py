#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import json
import os

class Map:
    def __init__(self, map_id="map1"):
        # Tipos de tiles
        self.EMPTY = 0
        self.WALL = 1
        self.DOOR = 2
        
        # Dicionário para armazenar as imagens carregadas
        self.images = {}
        
        # Dicionário para armazenar os sons de interação
        self.interaction_sounds = {}
        
        # Trilha sonora do mapa
        self.soundtrack = None
        self.soundtrack_path = None
        
        # Inicializa a configuração de itens (deve ser feito antes de carregar o mapa)
        self.item_config = {"tile_types": {}}
        self.load_item_config()
        
        # Carrega o mapa a partir do arquivo JSON
        self.load_map(map_id)
        
        # Carrega as imagens dos tiles
        self.load_images()
        
        # Carrega os sons de interação
        self.load_sounds()
    
    def load_item_config(self):
        """Carrega a configuração de itens do arquivo JSON"""
        try:
            config_path = os.path.join("config", "items.json")
            if not os.path.exists(config_path):
                print(f"Aviso: Arquivo de configuração de itens não encontrado: {config_path}")
                self.item_config = {"tile_types": {}}
                return
                
            with open(config_path, "r") as f:
                self.item_config = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar configuração de itens: {e}")
            self.item_config = {"tile_types": {}}
    
    def load_images(self):
        """Carrega as imagens para os tiles com base na configuração"""
        base_dir = "assets/images"
        
        # Cria os diretórios necessários se não existirem
        os.makedirs(os.path.join(base_dir, "tiles"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "objects"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "items"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "enemies"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "npcs"), exist_ok=True)
        
        # Carrega imagens para cada tipo de tile na configuração
        for tile_id, tile_info in self.item_config.get("tile_types", {}).items():
            image_path = tile_info.get("image", "")
            if image_path:
                full_path = os.path.join(base_dir, image_path)
                try:
                    if os.path.exists(full_path):
                        # Carrega a imagem e redimensiona para o tamanho do tile
                        image = pygame.image.load(full_path).convert_alpha()
                        image = pygame.transform.scale(image, (self.tile_size, self.tile_size))
                        self.images[tile_id] = image
                    else:
                        # Cria uma imagem colorida para substituir a ausente
                        self._create_colored_image(tile_id, tile_info)
                except Exception as e:
                    print(f"Erro ao carregar imagem {full_path}: {e}")
                    # Cria uma imagem colorida para substituir a ausente
                    self._create_colored_image(tile_id, tile_info)
        
        # Cria imagens padrão para tiles sem imagem
        if "0" not in self.images:  # Tile vazio
            img = pygame.Surface((self.tile_size, self.tile_size))
            img.fill(self.colors.get(self.EMPTY, (50, 150, 50)))
            self.images["0"] = img
            
        if "1" not in self.images:  # Parede
            img = pygame.Surface((self.tile_size, self.tile_size))
            img.fill(self.colors.get(self.WALL, (100, 100, 100)))
            self.images["1"] = img
            
        if "2" not in self.images:  # Porta
            img = pygame.Surface((self.tile_size, self.tile_size))
            img.fill(self.colors.get(self.DOOR, (150, 75, 0)))
            self.images["2"] = img
    
    def _create_colored_image(self, tile_id, tile_info):
        """Cria uma imagem colorida para substituir uma imagem ausente"""
        img = pygame.Surface((self.tile_size, self.tile_size))
        
        # Define a cor com base no tipo de item
        item_type = tile_info.get("type", "")
        if item_type == "terreno":
            color = (50, 150, 50)  # Verde para terreno
        elif item_type == "objeto":
            color = (150, 75, 0)   # Marrom para objetos
        elif item_type == "item":
            color = (255, 215, 0)  # Dourado para itens
        elif item_type == "inimigo":
            color = (200, 0, 0)    # Vermelho para inimigos
        elif item_type == "npc":
            color = (0, 100, 200)  # Azul para NPCs
        elif item_type == "transição":
            color = (150, 50, 200) # Roxo para transições
        else:
            color = (200, 200, 200) # Cinza para outros
        
        img.fill(color)
        
        # Adiciona um texto com o ID para identificação
        try:
            font = pygame.font.SysFont("Arial", 12)
            text = font.render(str(tile_id), True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.tile_size//2, self.tile_size//2))
            img.blit(text, text_rect)
        except:
            # Se não conseguir renderizar texto, desenha um padrão
            pygame.draw.rect(img, (0, 0, 0), (4, 4, self.tile_size-8, self.tile_size-8), 2)
        
        self.images[tile_id] = img
        print(f"Substituída imagem ausente do item {tile_id} ({tile_info.get('name', '')}) por cor {color}")
    
    def load_sounds(self):
        """Carrega os sons de interação para os objetos"""
        base_dir = "assets/sounds"
        
        # Cria o diretório de sons se não existir
        os.makedirs(os.path.join(base_dir, "effects"), exist_ok=True)
        
        # Carrega sons para cada tipo de tile na configuração
        for tile_id, tile_info in self.item_config.get("tile_types", {}).items():
            details = tile_info.get("details", {})
            
            # Verifica se o item tem som de interação
            if "interaction_sound" in details:
                sound_path = details["interaction_sound"]
                full_path = os.path.join(base_dir, sound_path)
                
                try:
                    if os.path.exists(full_path):
                        try:
                            sound = pygame.mixer.Sound(full_path)
                            self.interaction_sounds[tile_id] = sound
                        except Exception as e:
                            # Ignora erros ao carregar o som e continua a execução
                            print(f"Aviso: Não foi possível carregar o som {full_path}: {e}")
                            # Não armazena o som para este item
                    else:
                        print(f"Aviso: Arquivo de som não encontrado: {full_path}")
                        # Não tenta criar o arquivo nem armazenar o som
                except Exception as e:
                    print(f"Aviso: Erro ao processar som {full_path}: {e}")
                    # Ignora o erro e continua a execução
    
    def load_map(self, map_id):
        """Carrega um mapa a partir de um arquivo JSON"""
        try:
            # Verifica se o arquivo existe
            map_path = os.path.join("maps", f"{map_id}.json")
            if not os.path.exists(map_path):
                print(f"Erro: Arquivo de mapa não encontrado: {map_path}")
                self._create_error_map()
                return
                
            with open(map_path, "r") as f:
                try:
                    map_data = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Erro: Arquivo de mapa inválido: {map_path} - {e}")
                    self._create_error_map()
                    return
                
            # Informações básicas do mapa
            self.id = map_id
            self.name = map_data.get("name", "Mapa Sem Nome")
            self.width = map_data.get("width", 25)
            self.height = map_data.get("height", 19)
            self.tile_size = map_data.get("tile_size", 32)
            
            # Trilha sonora do mapa
            self.soundtrack_path = map_data.get("soundtrack", None)
            
            # Cores
            self.colors = {
                self.EMPTY: tuple(map_data.get("background_color", [50, 150, 50])),
                self.WALL: tuple(map_data.get("wall_color", [100, 100, 100])),
                self.DOOR: (150, 75, 0)  # Marrom para portas
            }
            
            # Dados do mapa
            self.data = map_data.get("data", [])
            
            # Verifica se os dados do mapa têm as dimensões corretas
            if len(self.data) != self.height:
                print(f"Aviso: Altura do mapa {map_id} incorreta. Esperado {self.height}, encontrado {len(self.data)}")
                
                # Ajusta a altura para corresponder aos dados
                if len(self.data) < self.height:
                    # Adiciona linhas vazias se necessário
                    empty_row = [self.WALL if x == 0 or x == self.width - 1 else self.EMPTY for x in range(self.width)]
                    while len(self.data) < self.height:
                        self.data.append(empty_row.copy())
                else:
                    # Corta linhas extras
                    self.data = self.data[:self.height]
            
            # Verifica se todas as linhas têm a largura correta
            for y, row in enumerate(self.data):
                if len(row) != self.width:
                    print(f"Aviso: Largura da linha {y} do mapa {map_id} incorreta. Esperado {self.width}, encontrado {len(row)}")
                    # Ajusta a linha para ter a largura correta
                    if len(row) < self.width:
                        self.data[y] = row + [self.EMPTY] * (self.width - len(row))
                    else:
                        self.data[y] = row[:self.width]
            
            # Portais
            self.portals = map_data.get("portals", [])
            
            # Objetos
            self.objects = map_data.get("objects", [])
            
            # Inimigos
            self.enemies = map_data.get("enemies", [])
            
            # Transições de borda
            self.edge_transitions = map_data.get("edge_transitions", {
                "left": None,
                "right": None,
                "top": None,
                "bottom": None
            })
            
            # Garante que todas as direções estão definidas
            for direction in ["left", "right", "top", "bottom"]:
                if direction not in self.edge_transitions:
                    self.edge_transitions[direction] = None
            
            # Retângulos de colisão para as paredes e objetos
            self.wall_rects = []
            self.door_rects = []
            self.collision_rects = []  # Nova lista para todos os objetos com colisão
            
            # Adiciona colisões para tiles no mapa
            for y in range(self.height):
                for x in range(self.width):
                    try:
                        tile_type = self.data[y][x]
                        tile_str = str(tile_type)
                        
                        # Cria o retângulo para o tile
                        rect = pygame.Rect(
                            x * self.tile_size, 
                            y * self.tile_size, 
                            self.tile_size, 
                            self.tile_size
                        )
                        
                        # Verifica se é uma parede
                        if tile_type == self.WALL:
                            self.wall_rects.append(rect)
                            self.collision_rects.append(rect)
                        
                        # Verifica se é uma porta
                        elif tile_type == self.DOOR:
                            self.door_rects.append({
                                "rect": rect,
                                "x": x,
                                "y": y
                            })
                        
                        # Verifica se o tile tem colisão baseado na configuração
                        elif tile_str in self.item_config.get("tile_types", {}):
                            item_config = self.item_config["tile_types"][tile_str]
                            if item_config.get("collision", False):
                                self.collision_rects.append(rect)
                    except IndexError:
                        print(f"Erro: Índice inválido no mapa {map_id}: ({x}, {y})")
            
            # Adiciona colisões para objetos específicos
            for obj in self.objects:
                obj_id = str(obj.get("id", 0))
                if obj_id in self.item_config.get("tile_types", {}):
                    item_config = self.item_config["tile_types"][obj_id]
                    if item_config.get("collision", False):
                        x, y = obj.get("x", 0), obj.get("y", 0)
                        rect = pygame.Rect(
                            x * self.tile_size, 
                            y * self.tile_size, 
                            self.tile_size, 
                            self.tile_size
                        )
                        self.collision_rects.append(rect)
            
            # Adiciona colisões para inimigos
            for enemy in self.enemies:
                enemy_id = str(enemy.get("id", 0))
                if enemy_id in self.item_config.get("tile_types", {}):
                    item_config = self.item_config["tile_types"][enemy_id]
                    if item_config.get("collision", False):
                        x, y = enemy.get("x", 0), enemy.get("y", 0)
                        rect = pygame.Rect(
                            x * self.tile_size, 
                            y * self.tile_size, 
                            self.tile_size, 
                            self.tile_size
                        )
                        self.collision_rects.append(rect)
                
        except Exception as e:
            print(f"Erro ao carregar o mapa {map_id}: {e}")
            self._create_error_map()
    
    def _create_error_map(self):
        """Cria um mapa de erro quando ocorre um problema ao carregar o mapa"""
        self.id = "error"
        self.name = "Erro ao Carregar Mapa"
        self.width = 25
        self.height = 19
        self.tile_size = 32
        self.soundtrack_path = None
        self.colors = {
            self.EMPTY: (50, 50, 50),  # Cinza escuro para o fundo
            self.WALL: (255, 0, 0),    # Vermelho para as paredes
            self.DOOR: (150, 75, 0)    # Marrom para portas
        }
        
        # Cria um mapa com bordas e um padrão de "X" no meio para indicar erro
        self.data = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Bordas do mapa
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    row.append(self.WALL)
                # Padrão de "X" no meio
                elif x == y or x == (self.width - 1 - y):
                    row.append(self.WALL)
                # Resto é vazio
                else:
                    row.append(self.EMPTY)
            self.data.append(row)
        
        # Limpa outras estruturas
        self.portals = []
        self.objects = [
            {
                "id": 12,  # Placa
                "x": 12,
                "y": 9,
                "details": {
                    "message": "Erro ao carregar o mapa. Verifique os arquivos do jogo."
                }
            }
        ]
        self.enemies = []
        self.edge_transitions = {"left": None, "right": None, "top": None, "bottom": None}
        
        # Recria os retângulos de colisão
        self.wall_rects = []
        self.door_rects = []
        self.collision_rects = []
        
        for y in range(self.height):
            for x in range(self.width):
                if self.data[y][x] == self.WALL:
                    rect = pygame.Rect(
                        x * self.tile_size, 
                        y * self.tile_size, 
                        self.tile_size, 
                        self.tile_size
                    )
                    self.wall_rects.append(rect)
                    self.collision_rects.append(rect)
    
    def draw(self, screen):
        """Desenha o mapa na tela"""
        for y in range(self.height):
            for x in range(self.width):
                try:
                    tile_type = self.data[y][x]
                    tile_str = str(tile_type)
                    rect = pygame.Rect(
                        x * self.tile_size, 
                        y * self.tile_size, 
                        self.tile_size, 
                        self.tile_size
                    )
                    
                    # Desenha a imagem se disponível, caso contrário usa um retângulo colorido
                    if tile_str in self.images:
                        screen.blit(self.images[tile_str], rect)
                    else:
                        pygame.draw.rect(screen, self.colors.get(tile_type, (255, 0, 255)), rect)
                        pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Borda preta
                except (IndexError, TypeError):
                    # Em caso de erro, desenha um tile roxo para indicar problema
                    rect = pygame.Rect(
                        x * self.tile_size, 
                        y * self.tile_size, 
                        self.tile_size, 
                        self.tile_size
                    )
                    pygame.draw.rect(screen, (255, 0, 255), rect)  # Roxo para indicar erro
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Borda preta
        
        # Desenha objetos específicos
        for obj in self.objects:
            obj_id = str(obj.get("id", 0))
            if obj_id in self.images:
                x, y = obj.get("x", 0), obj.get("y", 0)
                rect = pygame.Rect(
                    x * self.tile_size, 
                    y * self.tile_size, 
                    self.tile_size, 
                    self.tile_size
                )
                screen.blit(self.images[obj_id], rect)
        
        # Desenha inimigos
        for enemy in self.enemies:
            enemy_id = str(enemy.get("id", 0))
            if enemy_id in self.images:
                x, y = enemy.get("x", 0), enemy.get("y", 0)
                rect = pygame.Rect(
                    x * self.tile_size, 
                    y * self.tile_size, 
                    self.tile_size, 
                    self.tile_size
                )
                screen.blit(self.images[enemy_id], rect)
    
    def check_collision(self, player):
        """Verifica colisões entre o jogador e as paredes/objetos"""
        # Guarda a posição anterior
        prev_x = player.rect.x
        prev_y = player.rect.y
        
        # Verifica colisão com cada objeto de colisão
        for collision_rect in self.collision_rects:
            if player.rect.colliderect(collision_rect):
                # Restaura a posição anterior se houve colisão
                player.rect.x = prev_x
                player.rect.y = prev_y
                return True
        
        return False
    
    def check_door_interaction(self, player):
        """Verifica se o jogador está interagindo com uma porta"""
        for door in self.door_rects:
            if player.rect.colliderect(door["rect"]):
                # Toca o som de interação da porta, se disponível
                try:
                    if "2" in self.interaction_sounds:
                        self.interaction_sounds["2"].play()
                except Exception as e:
                    # Ignora erros ao tocar o som
                    print(f"Aviso: Não foi possível tocar som de porta: {e}")
                
                # Procura o portal correspondente
                for portal in self.portals:
                    try:
                        if portal["x"] == door["x"] and portal["y"] == door["y"]:
                            # Verifica se o mapa de destino existe
                            target_map = portal.get("target_map", "map1")
                            if not os.path.exists(os.path.join("maps", f"{target_map}.json")):
                                print(f"Aviso: Mapa de destino não encontrado: {target_map}")
                                return None
                            
                            # Verifica se as coordenadas de destino são válidas
                            target_x = portal.get("target_x", 1)
                            target_y = portal.get("target_y", 1)
                            
                            return {
                                "target_map": target_map,
                                "target_x": target_x,
                                "target_y": target_y
                            }
                    except Exception as e:
                        print(f"Erro ao processar portal: {e}")
        
        return None
    
    def check_object_interaction(self, player):
        """Verifica se o jogador está interagindo com um objeto"""
        for obj in self.objects:
            obj_id = str(obj.get("id", 0))
            x, y = obj.get("x", 0), obj.get("y", 0)
            
            # Cria um retângulo para o objeto
            obj_rect = pygame.Rect(
                x * self.tile_size, 
                y * self.tile_size, 
                self.tile_size, 
                self.tile_size
            )
            
            # Verifica se o jogador está colidindo com o objeto
            if player.rect.colliderect(obj_rect):
                # Toca o som de interação do objeto, se disponível
                try:
                    if obj_id in self.interaction_sounds:
                        self.interaction_sounds[obj_id].play()
                except Exception as e:
                    # Ignora erros ao tocar o som
                    print(f"Aviso: Não foi possível tocar som do objeto {obj_id}: {e}")
                
                # Retorna o objeto para processamento adicional
                return obj
        
        return None
    
    def check_edge_transition(self, player):
        """Verifica se o jogador está saindo pelas bordas do mapa"""
        try:
            # Borda esquerda
            if player.rect.left <= 0 and self.edge_transitions.get("left"):
                transition = self.edge_transitions["left"]
                target_map = transition.get("target_map", "map1")
                
                # Verifica se o mapa de destino existe
                if not os.path.exists(os.path.join("maps", f"{target_map}.json")):
                    print(f"Aviso: Mapa de destino não encontrado: {target_map}")
                    return None
                
                return {
                    "direction": "left",
                    "target_map": target_map,
                    "target_x": transition.get("player_x", 23) * self.tile_size,
                    "target_y": player.rect.y if transition.get("player_y") == "same" else transition.get("player_y", 10) * self.tile_size
                }
            
            # Borda direita
            if player.rect.right >= self.width * self.tile_size and self.edge_transitions.get("right"):
                transition = self.edge_transitions["right"]
                target_map = transition.get("target_map", "map1")
                
                # Verifica se o mapa de destino existe
                if not os.path.exists(os.path.join("maps", f"{target_map}.json")):
                    print(f"Aviso: Mapa de destino não encontrado: {target_map}")
                    return None
                
                return {
                    "direction": "right",
                    "target_map": target_map,
                    "target_x": transition.get("player_x", 1) * self.tile_size,
                    "target_y": player.rect.y if transition.get("player_y") == "same" else transition.get("player_y", 10) * self.tile_size
                }
            
            # Borda superior
            if player.rect.top <= 0 and self.edge_transitions.get("top"):
                transition = self.edge_transitions["top"]
                target_map = transition.get("target_map", "map1")
                
                # Verifica se o mapa de destino existe
                if not os.path.exists(os.path.join("maps", f"{target_map}.json")):
                    print(f"Aviso: Mapa de destino não encontrado: {target_map}")
                    return None
                
                return {
                    "direction": "top",
                    "target_map": target_map,
                    "target_x": player.rect.x if transition.get("player_x") == "same" else transition.get("player_x", 12) * self.tile_size,
                    "target_y": transition.get("player_y", 17) * self.tile_size
                }
            
            # Borda inferior
            if player.rect.bottom >= self.height * self.tile_size and self.edge_transitions.get("bottom"):
                transition = self.edge_transitions["bottom"]
                target_map = transition.get("target_map", "map1")
                
                # Verifica se o mapa de destino existe
                if not os.path.exists(os.path.join("maps", f"{target_map}.json")):
                    print(f"Aviso: Mapa de destino não encontrado: {target_map}")
                    return None
                
                return {
                    "direction": "bottom",
                    "target_map": target_map,
                    "target_x": player.rect.x if transition.get("player_x") == "same" else transition.get("player_x", 12) * self.tile_size,
                    "target_y": transition.get("player_y", 1) * self.tile_size
                }
        except (KeyError, TypeError, AttributeError) as e:
            print(f"Erro ao verificar transição de borda: {e}")
            
        return None 

    def get_soundtrack_path(self):
        """Retorna o caminho da trilha sonora do mapa"""
        return self.soundtrack_path 