import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN
from pygame.locals import K_a, K_d, K_w, K_s
from pygame.locals import K_SPACE, K_ESCAPE
import sys
from player import Player
from globals import Globals
from map import TileMap
import cProfile
from entities import BasicEnemy
from generate_map import generate_map

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
Globals.add('WIDTH', WIDTH)
Globals.add('HEIGHT', HEIGHT)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GamGam")
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (87, 203, 219) # 57cbdb

def main():
    generate_map()

    projectiles = pygame.sprite.Group()
    Globals.add('projectiles', projectiles)
    tilemap = TileMap()
    Globals.add('tilemap', tilemap)
    clock = pygame.time.Clock()
    player = Player()
    Globals.add('player', player)
    enemies = pygame.sprite.Group()
    enemies.add(BasicEnemy(x=10, y=10))
    last_time = pygame.time.get_ticks()

    screen.fill(BACKGROUND_COLOR)

    tilemap.seed_info.draw(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    player.update_shooting_vector()
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        current_time = pygame.time.get_ticks()
        delta_time = (current_time - last_time) / 1000.0  # Convert to seconds
        last_time = current_time

        player.update(tilemap, delta_time)

        projectiles.update(delta_time, tilemap.walls, enemies)
        enemies.update(delta_time)

        tilemap.draw(screen)
        
        enemies.draw(screen)
        player.draw(screen)
        projectiles.draw(screen)

        clock.tick(30)
        pygame.display.update()

if __name__ == "__main__":
    main()
    # cProfile.run('main()')
