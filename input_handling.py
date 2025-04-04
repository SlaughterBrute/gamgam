import sys
import logging
import pygame
from utils import Singleton
from keybindings import Keybindings

class InputHandler(metaclass=Singleton):
    def __init__(self):
        self.keybindings = Keybindings()
        self.joysticks = []
        self._just_pressed = {}
        self.pressed = {}

    def update(self):
        self._just_pressed.clear()

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self._just_pressed['exit'] = True
                case pygame.JOYDEVICEADDED:
                    self.joysticks.append(pygame.joystick.Joystick(event.device_index))
                    logging.info(f'Addded: {event}')
                case pygame.JOYDEVICEREMOVED:
                    logging.info(f'Should be removed: {event}')
                case pygame.JOYBUTTONDOWN:
                    logging.debug(f'JOYBUTTONDOWN | Joystick id: {event.instance_id} | Button: {event.button}')
                case pygame.JOYBUTTONUP:
                    logging.debug(f'JOYBUTTONUP | Joystick id: {event.instance_id} | Button: {event.button}')
                case pygame.KEYDOWN:
                    self._just_pressed[event.key] = True
                    self.pressed[event.key] = True
                case pygame.KEYUP:
                    self.pressed[event.key] = False

    def just_pressed(self, action):
        return (
            self._just_pressed.get(action) 
            or self._just_pressed.get(self.keybindings.keyboard.get(action))
        )

    def pressed_keys(self):
        return self.pressed.copy()