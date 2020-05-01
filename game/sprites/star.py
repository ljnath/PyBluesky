import pygame
import random

# Star class which holds star attributes and behaviour
class Star(pygame.sprite.Sprite):
    """ Powerup sprite class for creating and updating the star in the game screen
    """
    def __init__(self, game_env):
        super(Star, self).__init__() 
        self.surf = pygame.image.load(game_env.constants.powerup_image).convert()   
        self.surf.set_colorkey((255, 255, 255), game_env.RLEACCEL)    
        self.rect = self.surf.get_rect(center=game_env.get_random_point_on_top())           # powerup stars are created on top of screen 

    def update(self):
        self.rect.move_ip(0, 4)                                                             # star moves down with speed 4
        if self.rect.bottom < 0:                                                            # star is killed if it crosses the screens
                self.kill()
