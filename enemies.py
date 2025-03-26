import pygame
import numpy as np
from entities import MovingGameObject
from pathfinding import astar
from globals import Globals
from weapons import Weapon

class BasicEnemy(MovingGameObject):
    def __init__(self, *groups, x, y):
        super().__init__(*groups, x=x, y=y, speed=20, size=10, image_path='Enemy.png', hitpoints=5)
        attack_rate_per_second = 1
        self.weapon = Weapon(firing_rate_per_second=attack_rate_per_second)

    def kill(self):
        score = Globals.get('score')
        Globals.add('score', score+1)
        super().kill()

    def update(self, delta_time):
        map = Globals.get('tilemap')
        player = Globals.get('player')

        x, y = map.to_map_position(self.rect.center)
        xt, yt = map.to_map_position(player.rect.center)

        if (x,y) == (xt,yt):
            # On same tile, get as close as posible
            direction_vector = (player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        else:
            # Not close, pathfind to get there
            path = astar((x,y), (xt, yt), map.tilemap)
            if path is None or len(path) <= 1:
                return

            self.next_path_position = path[1]

            direction_vector = (self.next_path_position[0] - x, self.next_path_position[1] - y)
        
        norm = np.linalg.norm(direction_vector)
        if norm > 0:
            direction_vector = direction_vector / norm
        else:
            raise Exception("I don't know what went wrong here.")

        if pygame.sprite.collide_rect(self, player):
            direction_vector = (player.rect.x - self.rect.x, player.rect.y - self.rect.y)
            self.weapon.shoot(self.rect.center, direction_vector)
        else:
            super().move(direction_vector, delta_time)