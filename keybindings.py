from pygame.locals import (CONTROLLER_BUTTON_X, K_ESCAPE, K_SPACE, K_a, K_d,
                           K_s, K_w, K_q)


class Keybindings():
    DEFAULT_KEYBOARD_KEYBINDINGS = {
        'move_left': K_a,
        'move_right': K_d,
        'move_up': K_w,
        'move_down': K_s,
        'attack': K_SPACE,
        'pause': K_ESCAPE,
        'exit': K_q,
    }
    DEFAULT_CONTROLLER_KEYBINDINGS = {
        'attack': CONTROLLER_BUTTON_X,
    }

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Keybindings, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.keyboard = Keybindings.DEFAULT_KEYBOARD_KEYBINDINGS.copy()
        self.controller = Keybindings.DEFAULT_CONTROLLER_KEYBINDINGS.copy()

    def _set_keybinding(self, keybindings_type:dict, action:str, binding):
        keybindings_dict = getattr(self, f'{keybindings_type}', None)
        if keybindings_dict is None:
            raise ValueError(f'No keybindings type {keybindings_type}.')
        
        if action not in keybindings_dict:
            raise ValueError(f'Action {action} is not a valid {keybindings_type} keybinding action.')
        
        keybindings_dict[action] = binding

    def set_keyboard_keybinding(self, action:str, binding):
        self._set_keybinding('keyboard', action, binding)

    def set_controller_keybinding(self, action:str, binding):
        self._set_keybinding('controller', action, binding)
