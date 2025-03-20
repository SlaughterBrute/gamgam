import pygame
import numpy as np
from globals import Globals
from entities import MovingEntity

class Projectile(MovingEntity):
    def __init__(self, x, y, direction, speed, damage, image_path):
        super().__init__(x=x, y=y, speed=speed, image_path=image_path, width=4, height=2)
        
        self.damage = damage
        self.game_width = Globals.get('WIDTH')
        self.game_height = Globals.get('HEIGHT')

        # Normalize the direction vector and calculate the angle
        direction = np.array(direction, dtype=float)
        norm = np.linalg.norm(direction)
        if norm > 0:
            self.direction = direction / norm  # Normalize
            angle = np.degrees(np.arctan2(-direction[1], direction[0]))  # Calculate angle in degrees
            self.image = pygame.transform.rotate(self.image, angle)  # Rotate the image
            self.rect = self.image.get_rect(center=self.rect.center)  # Update rect to new image size

    def update(self, delta_time, *objects_that_can_be_collided:pygame.sprite.Group):
        super().move(self.direction, delta_time)

        if not (0 <= self.rect.x <= self.game_width and 0 <= self.rect.y <= self.game_height):
            self.kill()
            return

        for group in objects_that_can_be_collided:
            collided = pygame.sprite.spritecollide(self, group, False)
            if collided:
                for sprite in collided:
                    sprite.damage(self.damage)
                self.kill()
        
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

class Bullet(Projectile):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction, speed=150, damage=1, image_path='Bullet.png')