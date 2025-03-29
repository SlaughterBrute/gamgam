import pygame
import logging
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN
from pygame.locals import K_a, K_d, K_w, K_s
from pygame.locals import K_SPACE, K_ESCAPE
import sys
from player import Player
from globals import Globals
from map import TileMap
import cProfile
from enemies import BasicEnemy
from generate_map import generate_map
from keybindings import Keybindings

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(funcName)s: %(message)s',
                    datefmt='%H:%M:%S')

# Initialize Pygame
pygame.init()
pygame.joystick.init()

# Set up display
WIDTH, HEIGHT = 420, 420
Globals.add('WIDTH', WIDTH)
Globals.add('HEIGHT', HEIGHT)
game_surface = pygame.Surface((WIDTH,HEIGHT))
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("GamGam")
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (87, 203, 219) # 57cbdb

font_size = 36
font = pygame.font.SysFont('Arial', font_size)

joysticks = []

def main():
    generate_map()
    keybindings = Keybindings()

    score = 0
    Globals.add('score', score)
    projectiles = pygame.sprite.Group()
    Globals.add('projectiles', projectiles)
    tilemap = TileMap()
    Globals.add('tilemap', tilemap)
    clock = pygame.time.Clock()
    player = Player()
    Globals.add('player', player)
    players = pygame.sprite.Group()
    players.add(player)
    enemies = pygame.sprite.Group()
    enemies.add(BasicEnemy(x=10, y=10))
    last_time = pygame.time.get_ticks()

    screen.fill(BACKGROUND_COLOR)

    tilemap.seed_info.draw(screen)
    while True:
        if player.hitpoints <= 0:
            game_over_surface = font.render(f"Game Over! Score: {Globals.get('score')}", True, BLACK)
            screen.blit(game_over_surface, (200,200))
            pygame.display.update()
            pygame.time.delay(4000)
            pygame.quit()
            sys.exit()
        if not enemies:
            enemies.add(BasicEnemy(x=10, y=10))

        for event in pygame.event.get():
            if event.type == pygame.JOYBALLMOTION:
                logging.inf(f'Ball: {event}')
            if event.type == pygame.JOYHATMOTION:
                logging.inf(f'Hat: {event}')
            if event.type == pygame.JOYAXISMOTION:
                logging.info(f'Axis: {event}')
            if event.type == pygame.JOYBUTTONDOWN:
                logging.info(f'Pressed: {event}')
            if event.type == pygame.JOYDEVICEADDED:
                joysticks.append(pygame.joystick.Joystick(event.device_index))
                logging.info(f'Addded: {event}')
            if event.type == pygame.JOYDEVICEREMOVED:
                logging.info(f'Should be removed: {event}')
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == keybindings.keyboard['attack']:
                    player.update_shooting_vector()
                if event.key == keybindings.keyboard['exit']:
                    pygame.quit()
                    sys.exit()

        pressed_keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - last_time) / 1000.0  # Convert to seconds
        last_time = current_time

        player.update(pressed_keys, joysticks, tilemap, delta_time)

        projectiles.update(delta_time, tilemap.walls, enemies, players)
        enemies.update(delta_time)

        tilemap.draw(game_surface)
        
        enemies.draw(game_surface)
        player.draw(game_surface)
        projectiles.draw(game_surface)

        clock.tick(30)
        screen.blit(game_surface, (20,20))
        
        # Show score
        score_surface = font.render(f"Score: {Globals.get('score')}", True, BLACK)
        screen.fill(BACKGROUND_COLOR, pygame.Rect(500, 500, 200, 100))
        screen.blit(score_surface, (500,500))

        hitpoints_surface = font.render(f'Lives: {player.hitpoints}', True, BLACK)
        screen.fill(BACKGROUND_COLOR, pygame.Rect(500, 400, 200, 100))
        screen.blit(hitpoints_surface, (500,400))

        pygame.display.update()

if __name__ == "__main__":
    main()
    # cProfile.run('main()')
