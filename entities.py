import pygame

class LivingEntity(pygame.sprite.Sprite):
    def __init__(self, *groups, x:int, y:int, size:int, image_path:str, hitpoints:int=1):
        super().__init__(*groups)
        self.hitpoints = hitpoints
        self.rect = pygame.rect.Rect(0, 0, size, size)
        image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.scale(image, self.rect.size)
        self.rect.center = (x,y)

    def damage(self, damage:int):
        self.hitpoints -= damage
        if self.hitpoints <= 0:
            self.kill()
    
    def draw(self, surface:pygame.Surface):
        surface.blit(self.image, self.rect)

class BasicEnemy(LivingEntity):
    def __init__(self, *groups, x, y):
        super().__init__(*groups, x=x, y=y, size=10, image_path='Enemy.png', hitpoints=5)