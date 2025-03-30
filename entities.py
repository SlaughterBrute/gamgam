import pygame
import numpy as np
from globals import Globals

class GameObject(pygame.sprite.Sprite):
    def __init__(self, *groups, x:int, y:int, image_path:str, hitpoints:int, size:int=None, width:int=None, height:int=None):
        super().__init__(*groups)
        if size is not None:
            self.width = size
            self.height = size
        elif width is not None and height is not None:
            self.width = width
            self.height = height
        else:
            raise ValueError("Either 'size' or both 'width' and 'height' must be provided.")

        self.rect = pygame.rect.Rect(0, 0, self.width, self.height)
        image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.scale(image, self.rect.size)
        self.rect.center = (x,y)
        self.position = np.array([self.rect.x, self.rect.y], dtype=float)
        self.hitpoints = hitpoints
    
    def damage(self, damage:int):
        self.hitpoints -= damage
        if self.hitpoints <= 0:
            self.kill()

class MovingGameObject(GameObject):
    def __init__(self, *groups, x:int, y:int, speed:float, image_path:str, hitpoints:int, size:int=None, width:int=None, height:int=None):
        super().__init__(*groups, x=x, y=y, image_path=image_path, hitpoints=hitpoints, size=size, width=width, height=height)
        self.speed = speed

    def move(self, direction_vector, delta_time, wall_collision=False):
        original_pos = self.position.copy()

        self.position += direction_vector * self.speed * delta_time

        if wall_collision:
            tilemap = Globals.get('tilemap')

        self.rect.centerx = self.position[0]  # Update rect position

        if wall_collision:
            if direction_vector[0] < 0:
                within_map = 0 <= self.rect.left
            else:
                within_map = self.rect.right <= Globals.get('WIDTH')
            if not within_map or pygame.sprite.spritecollide(self, tilemap.walls, False):
                # Revert position in the x direction
                self.position[0] = original_pos[0]
                self.rect.centerx = self.position[0]

        self.rect.centery = self.position[1]  # Update rect position

        if wall_collision:
            if direction_vector[1] < 0:
                within_map = 0 <= self.rect.top
            else:
                within_map = self.rect.bottom <= Globals.get('HEIGHT')
            if not within_map or pygame.sprite.spritecollide(self, tilemap.walls, False):
                # Revert position in the y direction
                self.position[1] = original_pos[1]
                self.rect.centery = self.position[1]

    def draw(self, surface:pygame.Surface):
        surface.blit(self.image, self.rect)
    