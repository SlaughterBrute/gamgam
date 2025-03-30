import logging
import sys

import pygame

from enemies import BasicEnemy
from generate_map import generate_map
from globals import Globals
from keybindings import Keybindings
from map import TileMap
from player import Player
from screens import Screen

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(funcName)s: %(message)s',
                    datefmt='%H:%M:%S')

pygame.init()
pygame.joystick.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (87, 203, 219) # 57cbdb

WIDTH, HEIGHT = 420, 420
Globals.add('WIDTH', WIDTH)
Globals.add('HEIGHT', HEIGHT)

font_size = 36
font = pygame.font.SysFont('Arial', font_size)

class Gameplay(Screen):
    def __init__(self, game):
        super().__init__(width=WIDTH, height=HEIGHT)
        self.parent_surface = game.main_surface
        self.game = game

        generate_map()

        self.score = 0
        Globals.add('score', self.score)
        self.projectiles = pygame.sprite.Group()
        Globals.add('projectiles', self.projectiles)
        self.tilemap = TileMap()
        Globals.add('tilemap', self.tilemap)
        self.player = Player()
        Globals.add('player', self.player)
        self.players = pygame.sprite.Group()
        self.players.add(self.player)
        self.enemies = pygame.sprite.Group()
        self.enemies.add(BasicEnemy(x=10, y=10))
        
    
    def update(self, dt, keys, joysticks):
        self.player.update(keys, joysticks, self.tilemap, dt)

        self.projectiles.update(dt, self.tilemap.walls, self.enemies, self.players)
        self.enemies.update(dt)
    
    def draw(self):
        self.tilemap.seed_info.draw(self.parent_surface)
        self.tilemap.draw(self.surface)
        
        self.enemies.draw(self.surface)
        self.players.draw(self.surface)
        self.projectiles.draw(self.surface)

        self.parent_surface.blit(self.surface, (20,20))
        
        # Show score
        score_surface = font.render(f"Score: {Globals.get('score')}", True, BLACK)
        self.parent_surface.fill(BACKGROUND_COLOR, pygame.Rect(500, 500, 200, 100))
        self.parent_surface.blit(score_surface, (500,500))

        hitpoints_surface = font.render(f'Lives: {self.player.hitpoints}', True, BLACK)
        self.parent_surface.fill(BACKGROUND_COLOR, pygame.Rect(500, 400, 200, 100))
        self.parent_surface.blit(hitpoints_surface, (500,400))

class Game:
    def __init__(self):
        self.main_surface = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("GamGam")

        self.clock = pygame.time.Clock()
        self.last_time = pygame.time.get_ticks()

        self.joysticks = []
        self.keybindings = Keybindings()
        self.keybindings.controller['attack'].add_binding('axis', 5)
        self.gameplay = Gameplay(self)
        
        self.main_surface.fill(BACKGROUND_COLOR)

        self.active_screen:Screen = self.gameplay
    
    def run(self):
        while True:
            # if player.hitpoints <= 0:
            #     game_over_surface = font.render(f"Game Over! Score: {Globals.get('score')}", True, BLACK)
            #     screen.blit(game_over_surface, (200,200))
            #     pygame.display.update()
            #     pygame.time.delay(4000)
            #     pygame.quit()
            #     sys.exit()
            # if not enemies:
            #     enemies.add(BasicEnemy(x=10, y=10))

            for event in pygame.event.get():
                if event.type == pygame.JOYDEVICEADDED:
                    self.joysticks.append(pygame.joystick.Joystick(event.device_index))
                    logging.info(f'Addded: {event}')
                if event.type == pygame.JOYDEVICEREMOVED:
                    logging.info(f'Should be removed: {event}')
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == self.keybindings.keyboard['attack']:
                        logging.debug('Player should update shooting vector.')
                        # player.update_shooting_vector()
                    if event.key == self.keybindings.keyboard['exit']:
                        pygame.quit()
                        sys.exit()

            pressed_keys = pygame.key.get_pressed()
            current_time = pygame.time.get_ticks()
            delta_time = (current_time - self.last_time) / 1000.0  # Convert to seconds
            self.last_time = current_time

            self.active_screen.update(delta_time, pressed_keys, self.joysticks)

            self.gameplay.draw()
            if not isinstance(self.active_screen, Gameplay):
                self.active_screen.draw()

            self.clock.tick(30)
            pygame.display.update()


if __name__ == "__main__":
    Game().run()