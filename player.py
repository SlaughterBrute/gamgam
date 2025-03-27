import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN
from pygame.locals import K_a, K_d, K_w, K_s
from pygame.locals import K_SPACE
from weapons import Blaster
import numpy as np
from globals import Globals
from entities import MovingGameObject
from keybindings import Keybindings

class Player(MovingGameObject):
    def __init__(self, start_x:int=0, start_y:int=0):
        super().__init__(x=start_x, y=start_y, speed=40, image_path='Player.png', hitpoints=10, size=10)
        self.last_movement_vector = np.array([1.0, 0.0], dtype=float)
        self.shooting_vector = np.array([1.0, 0.0], dtype=float)
        self.weapon = Blaster()
        self.keybindings = Keybindings()

    def update(self, tilemap, delta_time):
        pressed_keys = pygame.key.get_pressed()
        left = pressed_keys[self.keybindings.keyboard['move_left']]
        right = pressed_keys[self.keybindings.keyboard['move_right']]
        up = pressed_keys[self.keybindings.keyboard['move_up']]
        down = pressed_keys[self.keybindings.keyboard['move_down']]
        attack = pressed_keys[self.keybindings.keyboard['attack']]

        self.move(tilemap, left, right, up, down, delta_time)

        if attack:
            self.shoot()

    def shoot(self):
        self.weapon.shoot(self.rect.center, self.shooting_vector)
    
    def update_shooting_vector(self):
        self.shooting_vector = self.last_movement_vector.copy()

    def move(self, tilemap, left, right, up, down, delta_time):
        # Store the original position for collision resolution
        original_pos = self.position.copy()

        # Calculate movement vector
        movement_vector = np.array([0.0, 0.0], dtype=float)

        if left and self.rect.left > 0:
            movement_vector[0] -= 1
        if right and self.rect.right < Globals.get('WIDTH'):
            movement_vector[0] += 1
        if up and self.rect.top > 0:
            movement_vector[1] -= 1
        if down and self.rect.bottom < Globals.get('HEIGHT'):
            movement_vector[1] += 1
        
        norm = np.linalg.norm(movement_vector)
        if norm > 0:
            movement_vector = movement_vector / norm
            movement_vector *= self.speed * delta_time
            self.last_movement_vector = movement_vector.copy()

            # Attempt to move in the x direction
            if movement_vector[0] != 0:
                self.position[0] += movement_vector[0]
                self.rect.x = self.position[0]  # Update rect position

                # Check for collisions in the x direction
                if pygame.sprite.spritecollide(self, tilemap.walls, False):
                    # Revert position in the x direction
                    self.position[0] = original_pos[0]
                    self.rect.x = self.position[0]

            # Attempt to move in the y direction
            if movement_vector[1] != 0:
                self.position[1] += movement_vector[1]
                self.rect.y = self.position[1]  # Update rect position

                # Check for collisions in the y direction
                if pygame.sprite.spritecollide(self, tilemap.walls, False):
                    # Revert position in the y direction
                    self.position[1] = original_pos[1]
                    self.rect.y = self.position[1]

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)