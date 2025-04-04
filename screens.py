import pygame

class Screen:
    def __init__(self, width:int, height:int):
        self.surface = pygame.surface.Surface((width, height))

    def update(self, delta_time):
        pass
    
    def draw(self):
        pass