import pygame
import random

class Vegetation(pygame.sprite.Sprite):
    """ Vegetation sprite class for creating and updating the vegetation in the game screen
    """
    def __init__(self, game_env, x_pos=None, y_pos=None):
        super(Vegetation, self).__init__()
        self.__game_env= game_env
        self.surf = pygame.image.load(random.choice(self.__game_env.constants.vegetation)).convert()
        x_pos = self.__game_env.constants.screen_width if x_pos is None else x_pos
        y_pos = self.__game_env.constants.screen_height - self.surf.get_height() / 2 if y_pos is None else y_pos
        self.rect = self.surf.get_rect(center=(x_pos, y_pos))
        self.__speed = 2

    def update(self):
        self.rect.move_ip(-self.__speed, 0)
        if self.rect.right < 0:
            self.kill()
