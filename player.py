import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN
from pygame.locals import K_a, K_d, K_w, K_s
from pygame.locals import K_SPACE
from weapons import Blaster
import numpy as np
from globals import Globals
from entities import MovingGameObject
from keybindings import Keybindings
from input_handling import InputHandler

class Player(MovingGameObject):
    def __init__(self, start_x:int=5, start_y:int=5):
        super().__init__(x=start_x, y=start_y, speed=40, image_path='Player.png', hitpoints=10, size=10)
        self.last_movement_vector = np.array([1.0, 0.0], dtype=float)
        self.shooting_vector = np.array([1.0, 0.0], dtype=float)
        self.weapon = Blaster()
        self.keybindings = Keybindings()
        self.input_handler = InputHandler()

    def update(self, tilemap, delta_time):
        joysticks = self.input_handler.joysticks

        if self.input_handler.just_pressed('attack'):
            self.update_shooting_vector()

        pressed_keys = self.input_handler.pressed_keys()

        if joysticks:
            # Controller input
            joystick = joysticks[0]
            x = joystick.get_axis(0)
            y = joystick.get_axis(1)
            movement_vector = np.array([x, y], dtype=float)
            self.move(tilemap, movement_vector, delta_time)

            # Attack
            attack = any(getattr(joystick, f'get_{input_type}')(id) > 0 for
                         (input_type, id) in self.keybindings.controller['attack'])
            
        else:   
            # Keyboard keys
            left = pressed_keys.get(self.keybindings.keyboard['move_left'])
            right = pressed_keys.get(self.keybindings.keyboard['move_right'])
            up = pressed_keys.get(self.keybindings.keyboard['move_up'])
            down = pressed_keys.get(self.keybindings.keyboard['move_down'])
            attack = pressed_keys.get(self.keybindings.keyboard['attack'])
            self._move_keyboard(tilemap, left, right, up, down, delta_time)

        if attack:
            self.shoot()

    def shoot(self):
        self.weapon.shoot(self.rect.center, self.shooting_vector)
    
    def update_shooting_vector(self):
        self.shooting_vector = self.last_movement_vector.copy()

    def _move_keyboard(self, tilemap, left, right, up, down, delta_time):
        # Calculate movement vector
        movement_vector = np.array([0.0, 0.0], dtype=float)

        if left:
            movement_vector[0] -= 1
        if right:
            movement_vector[0] += 1
        if up:
            movement_vector[1] -= 1
        if down:
            movement_vector[1] += 1

        norm = np.linalg.norm(movement_vector)
        if norm > 0:
            movement_vector = movement_vector / norm
            self.move(tilemap, movement_vector, delta_time)

    def move(self, tilemap, movement_vector, delta_time):
        original_pos = self.position.copy()

        movement_vector *= self.speed * delta_time
        self.last_movement_vector = movement_vector.copy()

        # Attempt to move in the x direction
        if movement_vector[0] != 0:
            self.position[0] += movement_vector[0]
            self.rect.x = self.position[0]  # Update rect position

            if movement_vector[0] < 0:
                within_map = 0 <= self.rect.left
            else:
                within_map = self.rect.right <= Globals.get('WIDTH')
            if not within_map or pygame.sprite.spritecollide(self, tilemap.walls, False):
                # Revert position in the x direction
                self.position[0] = original_pos[0]
                self.rect.x = self.position[0]

        # Attempt to move in the y direction
        if movement_vector[1] != 0:
            self.position[1] += movement_vector[1]
            self.rect.y = self.position[1]  # Update rect position

            if movement_vector[1]:
                within_map = 0 <= self.rect.top
            else:
                within_map = self.rect.bottom <= Globals.get('HEIGHT')
            if not within_map or pygame.sprite.spritecollide(self, tilemap.walls, False):
                # Revert position in the y direction
                self.position[1] = original_pos[1]
                self.rect.y = self.position[1]

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)