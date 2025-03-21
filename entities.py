import pygame
import numpy as np

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
        self.position = np.array([x, y], dtype=float)
        self.hitpoints = hitpoints
    
    def damage(self, damage:int):
        self.hitpoints -= damage
        if self.hitpoints <= 0:
            self.kill()

class MovingGameObject(GameObject):
    def __init__(self, *groups, x:int, y:int, speed:float, image_path:str, hitpoints:int, size:int=None, width:int=None, height:int=None):
        super().__init__(*groups, x=x, y=y, image_path=image_path, hitpoints=hitpoints, size=size, width=width, height=height)
        self.speed = speed

    def move(self, direction_vector, delta_time):
        self.position += direction_vector * self.speed * delta_time
        self.rect.center = (self.position[0], self.position[1])

    def draw(self, surface:pygame.Surface):
        surface.blit(self.image, self.rect)
    

class BasicEnemy(MovingGameObject):
    def __init__(self, *groups, x, y):
        super().__init__(*groups, x=x, y=y, speed=40, size=10, image_path='Enemy.png', hitpoints=5)