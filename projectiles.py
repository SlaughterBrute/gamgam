import pygame
import numpy as np
from globals import Globals

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, damage, image_path):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert()
        self.position = np.array([x, y], dtype=float)
        self.rect = pygame.rect.Rect(0, 0, 2, 4)
        self.rect.center = (x, y)
        self.damage = damage
        self.game_width = Globals.get('WIDTH')
        self.game_height = Globals.get('HEIGHT')

        # Normalize the direction vector and calculate the angle
        direction = np.array(direction, dtype=float)
        norm = np.linalg.norm(direction)
        if norm > 0:
            direction = direction / norm  # Normalize
            angle = np.degrees(np.arctan2(-direction[1], direction[0]))  # Calculate angle in degrees
            self.image = pygame.transform.rotate(self.original_image, angle)  # Rotate the image
            self.rect = self.image.get_rect(center=self.rect.center)  # Update rect to new image size

        # Set the bullet's velocity based on the direction
        self.velocity = direction * 2  # Adjust speed as necessary

    def update(self, *objects_that_can_be_collided:pygame.sprite.Group):
        # Update the bullet's position based on its velocity
        self.position += self.velocity
        self.rect.topleft = (self.position[0], self.position[1])  # Update rect position

        for group in objects_that_can_be_collided:
            collided = pygame.sprite.spritecollide(self, group, False)
            if collided:
                for sprite in collided:
                    sprite.damage(self.damage)
                self.kill()
                # Should I return early here?
        
        if not (0 <= self.rect.x <= self.game_width and 0 <= self.rect.y <= self.game_height):
            self.kill()  # Remove the bullet from all groups
        
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

class Bullet(Projectile):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction, 1, 'Bullet.png')