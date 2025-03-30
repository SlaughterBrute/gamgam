import pygame

class Screen:
    def __init__(self, width:int, height:int):
        self.surface = pygame.surface.Surface((width, height))

    def update(self, delta_time, pressed_keys, joysticks):
        pass
    
    def draw(self):
        pass