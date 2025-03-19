import pygame
from projectiles import Bullet
from globals import Globals


class Weapon():
    def __init__(self, firing_rate_per_second: float):
        self.firing_rate = 1/firing_rate_per_second * 1000
        self.last_shot_time = 0

    def _can_shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.firing_rate:
            return True
        return False

    def shoot(self, origin_position, direction_vector):
        
        if self._can_shoot():
            self._shoot(origin_position, direction_vector)
            self.last_shot_time = pygame.time.get_ticks()
    
    def _shoot(self, origin_position, direction_vector):
        projectiles:pygame.sprite.Group = Globals.get('projectiles')
        projectiles.add(Bullet(*origin_position, direction_vector))

class Blaster(Weapon):
    def __init__(self):
        super().__init__(firing_rate_per_second=3)