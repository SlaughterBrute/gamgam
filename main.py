import logging
import sys
import random

import pygame

from enemies import BasicEnemy
from generate_map import generate_map
from globals import Globals
from keybindings import Keybindings
from map import TileMap
from player import Player
from screens import Screen
from input_handling import InputHandler

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(funcName)s: %(message)s',
                    datefmt='%H:%M:%S')

pygame.init()
pygame.joystick.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (116, 184, 222)

WIDTH, HEIGHT = 420, 420
Globals.add('WIDTH', WIDTH)
Globals.add('HEIGHT', HEIGHT)

font_size = 36
font = pygame.font.SysFont('Arial', font_size)

class GameOver(Screen):
    def __init__(self, game, score:int):
        super().__init__(width=1000, height=1000)
        self.parent_surface = game.main_surface
        self.game = game
        self.score = score

    def draw(self):
        game_over_surface = font.render(f"Game Over! Score: {self.score}", True, BLACK)
        self.parent_surface.blit(game_over_surface, (200,200))

class Pause(Screen):
    def __init__(self, game):
        super().__init__(width=200, height=200)
        self.game = game
        self.parent_surface = game.main_surface
        self.keybindings = Keybindings()
        self.input_handler = InputHandler()

    def resume_gameplay(self):
        self.game.active_screen = self.game.gameplay

    def update(self, delta_time):
        if self.input_handler.just_pressed('pause'):
            self.resume_gameplay()
            return

    def draw(self):
        surface = font.render(f"Paused, press <pause> to continue playing", True, BLACK)
        self.parent_surface.blit(surface, (200,200))

class Gameplay(Screen):
    def __init__(self, game):
        super().__init__(width=WIDTH, height=HEIGHT)
        self.parent_surface = game.main_surface
        self.game = game
        self.keybindings = Keybindings()
        self.input_handler = InputHandler()

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
    
    def pause_gameplay(self):
        self.game.active_screen = Pause(self.game)

    def game_over(self):
        self.game.active_screen = GameOver(self.game, self.score)

    def update(self, dt):
        if self.input_handler.just_pressed('pause'):
            self.pause_gameplay()
            return

        # TODO: Determine what order things should evaluated in here.
        if not self.enemies:
            self.enemies.add(BasicEnemy(x=10, y=10))

        self.player.update(self.tilemap, dt)

        self.projectiles.update(dt, self.tilemap.walls, self.enemies, self.players)
        self.enemies.update(dt)

        if self.player.hitpoints <= 0:
            self.game_over()
            return
    
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
        self.width = 800
        self.height = 600
        self.main_surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("GamGam")

        self.clock = pygame.time.Clock()
        self.last_time = pygame.time.get_ticks()

        self.keybindings = Keybindings()
        self.keybindings.controller['attack'].add_binding('axis', 5)
        self.gameplay = Gameplay(self)

        self.active_screen:Screen = self.gameplay
        self.input_handler = InputHandler()

        self.init_decoration_surface()
        
    def init_decoration_surface(self):
        self.decoration_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        flower = pygame.image.load('assets/images/simple-flower.png').convert_alpha()
        flower = pygame.transform.scale(flower, (12,12)) # Multiples of three, flower is 3x3 pixels
        flower_rect = flower.get_rect()
        width = self.decoration_surface.get_width()
        height = self.decoration_surface.get_height()
        for _ in range(50):
            x = random.randint(0, width - flower_rect.width)
            y = random.randint(0, height - flower_rect.height)
            
            flower_rect.topleft = (x, y)
            self.decoration_surface.blit(flower, flower_rect)

    def run(self):
        while True:
            self.input_handler.update()
            if self.input_handler.just_pressed('exit'):
                pygame.quit()
                sys.exit()

            current_time = pygame.time.get_ticks()
            delta_time = (current_time - self.last_time) / 1000.0  # Convert to seconds
            self.last_time = current_time

            self.active_screen.update(delta_time)

            self.main_surface.fill(BACKGROUND_COLOR)
            self.main_surface.blit(self.decoration_surface, (0,0))

            self.gameplay.draw()
            if not isinstance(self.active_screen, Gameplay):
                self.active_screen.draw()

            self.clock.tick(30)
            pygame.display.update()


if __name__ == "__main__":
    Game().run()