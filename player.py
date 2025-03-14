#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, character_data=None):
        super().__init__()
        
        # Dados do personagem
        if character_data is None:
            # Personagem padrão
            self.name = "Jogador"
            self.color = (0, 0, 255)  # Azul
            self.speed = 5
        else:
            # Personagem personalizado
            self.name = character_data.get("name", "Jogador")
            self.color = character_data.get("color", (0, 0, 255))
            self.speed = character_data.get("speed", 5)
        
        # Sistema de moedas
        self.coins = 10  # Jogador começa com 10 moedas
        self.inventory = []  # Inventário do jogador
        
        # Cria uma imagem para o jogador
        self.image = pygame.Surface((32, 32))
        self.image.fill(self.color)
        
        # Define o retângulo do sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # A hitbox é o próprio retângulo do sprite
        self.hitbox = self.rect
        
        # Vetores de velocidade
        self.velocity = pygame.math.Vector2(0, 0)
        
        # Direção que o jogador está olhando
        self.direction = "down"
        
        # Estado de interação
        self.interacting = False
        
        # Contador para limitar a frequência dos logs
        self.stuck_log_counter = 0
        self.stuck_log_frequency = 60  # Só mostra log a cada 60 frames (aproximadamente 1 segundo)
    
    def update(self):
        """Atualiza a posição do jogador com base nos controles"""
        # Reinicia a velocidade
        self.velocity = pygame.math.Vector2(0, 0)
        
        # Obtém as teclas pressionadas
        keys = pygame.key.get_pressed()
        
        # Movimento horizontal
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = self.speed
            self.direction = "right"
            
        # Movimento vertical
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.y = -self.speed
            self.direction = "up"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity.y = self.speed
            self.direction = "down"
            
        # Normaliza o vetor se estiver se movendo na diagonal
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * self.speed
        
        # Não atualiza a posição aqui, isso será feito pelo Game após verificar colisões
        # self.rect.x += self.velocity.x
        # self.rect.y += self.velocity.y
    
    def handle_event(self, event):
        """Processa eventos específicos do jogador"""
        if event.type == pygame.KEYDOWN:
            # Tecla E para interagir com objetos
            if event.key == pygame.K_e:
                self.interacting = True
                print("Tecla E pressionada - Tentando interagir")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                self.interacting = False
    
    def set_position(self, x, y):
        """Define a posição do jogador"""
        self.rect.x = x
        self.rect.y = y
        self.update_hitbox()
    
    def constrain_to_map(self, map_width, map_height):
        """Impede que o jogador saia dos limites do mapa"""
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > map_width:
            self.rect.right = map_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > map_height:
            self.rect.bottom = map_height
        self.update_hitbox()
    
    def update_hitbox(self):
        """Atualiza a posição da hitbox para centralizar com o sprite"""
        # A hitbox é o próprio retângulo do sprite
        self.hitbox = self.rect
    
    def add_coins(self, amount):
        """Adiciona moedas ao jogador"""
        self.coins += amount
        print(f"Adicionadas {amount} moedas. Total: {self.coins}")
        return self.coins
    
    def remove_coins(self, amount):
        """Remove moedas do jogador se tiver saldo suficiente"""
        if self.coins >= amount:
            self.coins -= amount
            return True
        return False
    
    def add_item_to_inventory(self, item_id):
        """Adiciona um item ao inventário do jogador"""
        if not hasattr(self, 'inventory'):
            self.inventory = []
        
        self.inventory.append(item_id)
        print(f"Item {item_id} adicionado ao inventário do jogador. Total: {len(self.inventory)}")
    
    def remove_item_from_inventory(self, item_id):
        """Remove um item do inventário do jogador"""
        if hasattr(self, 'inventory') and item_id in self.inventory:
            self.inventory.remove(item_id)
            print(f"Item {item_id} removido do inventário do jogador. Total: {len(self.inventory)}")
            return True
        return False
    
    def has_item(self, item_id):
        """Verifica se o jogador possui um determinado item"""
        return item_id in self.inventory
    
    def draw_hitbox(self, screen):
        """Desenha a hitbox do jogador para depuração"""
        # Desenha um retângulo vermelho semi-transparente para representar a hitbox
        hitbox_surface = pygame.Surface((self.hitbox.width, self.hitbox.height), pygame.SRCALPHA)
        hitbox_surface.fill((255, 0, 0, 128))  # Vermelho semi-transparente
        screen.blit(hitbox_surface, self.hitbox.topleft)
        
        # Desenha a borda da hitbox
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)
    
    def move_with_collision(self, collision_rects):
        """Move o jogador considerando colisões"""
        # Guarda a posição original
        original_x = self.rect.x
        original_y = self.rect.y
        collision_detected = False
        
        # Movimento em dois passos (horizontal e depois vertical) para permitir deslizamento
        
        # 1. Movimento horizontal
        if self.velocity.x != 0:
            # Tenta mover horizontalmente
            self.rect.x += self.velocity.x
            
            # Verifica colisões horizontais
            horizontal_collision = False
            for rect in collision_rects:
                if self.rect.colliderect(rect):
                    horizontal_collision = True
                    collision_detected = True
                    # Ajusta a posição para evitar sobreposição
                    if self.velocity.x > 0:  # Movendo para a direita
                        self.rect.right = rect.left
                    else:  # Movendo para a esquerda
                        self.rect.left = rect.right
                    break
        
        # 2. Movimento vertical
        if self.velocity.y != 0:
            # Tenta mover verticalmente
            self.rect.y += self.velocity.y
            
            # Verifica colisões verticais
            vertical_collision = False
            for rect in collision_rects:
                if self.rect.colliderect(rect):
                    vertical_collision = True
                    collision_detected = True
                    # Ajusta a posição para evitar sobreposição
                    if self.velocity.y > 0:  # Movendo para baixo
                        self.rect.bottom = rect.top
                    else:  # Movendo para cima
                        self.rect.top = rect.bottom
                    break
        
        # Verifica se o jogador está completamente preso (não consegue se mover em nenhuma direção)
        if collision_detected and self.velocity.length() > 0:
            # Verifica se o jogador não conseguiu se mover em nenhuma direção
            if self.rect.x == original_x and self.rect.y == original_y:
                # Incrementa o contador e só mostra o log periodicamente
                self.stuck_log_counter += 1
                if self.stuck_log_counter >= self.stuck_log_frequency:
                    print("Log: Jogador preso - Não consegue se mover em nenhuma direção")
                    self.stuck_log_counter = 0
            else:
                # Resetar o contador se o jogador conseguiu se mover
                self.stuck_log_counter = 0
        else:
            # Resetar o contador se não houver colisão
            self.stuck_log_counter = 0
        
        return collision_detected 