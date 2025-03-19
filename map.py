import pygame
from globals import Globals

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type: str, x: int, y: int, destructable:bool=False, hitpoints:int=1):
        super().__init__()
        self.image = pygame.image.load(f'{tile_type}.png').convert()
        self.rect = pygame.Rect(0, 0, 20, 20)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.rect.left = x * self.rect.width
        self.rect.top = y * self.rect.height
        self.x = x
        self.y = y
        self.destructable = destructable
        self.hitpoints = hitpoints
    
    def draw(self, surface:pygame.Surface):
        surface.blit(self.image, self.rect)
    
    def damage(self, damage:int):
        if self.destructable:
            self.hitpoints -= damage

            if self.hitpoints <= 0:
                self.kill()

class GrassTile(Tile):
    def __init__(self, x, y):
        super().__init__('Grass', x, y)

class WallTile(Tile):
    def __init__(self, x, y):
        super().__init__('Wall', x, y, destructable=True, hitpoints=5)
    
    def kill(self):
        super().kill()
        tile = GrassTile(self.x, self.y)
        tilemap:TileMap = Globals.get('tilemap')
        tilemap.ground.add(tile)

class TileMap():
    def __init__(self):
        super().__init__()
        self._load_tilemap()
        self.ground = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.init_tiles()
    
    def _load_tilemap(self):
        tilemap = {}
        with open('map2.txt', 'r') as f:
            for row, tiles in enumerate(f.readlines()):
                for col, tile in enumerate(tiles):
                    if tile != '\n':
                        tilemap[col, row] = int(tile)
        self.tilemap = tilemap

    def create_tile(self, xy, raw_type):
        x, y = xy
        if raw_type == 0:
            self.ground.add(GrassTile(x,y))
        elif raw_type == 1:
            self.walls.add(WallTile(x,y))
        else:
            raise ValueError('No tilemapping for raw_type: %s', raw_type)

    def init_tiles(self):
        for tile in self.tilemap.items():
            self.create_tile(*tile)
    
    def draw(self, surface):
        self.ground.draw(surface)

        self.walls.draw(surface)