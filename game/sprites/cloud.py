import pygame
import random

class Cloud(pygame.sprite.Sprite):
    """ Cloud sprite class for creating and updating the cloud in the game screen
    """
    def __init__(self, game_env):
        super(Cloud, self).__init__()                                                       # initilizing parent class pygame.sprite.Sprite
        self.surf = pygame.image.load(random.choice(game_env.constants.clouds)).convert()   # loading cloud image
        self.surf.set_colorkey((255, 255, 255), game_env.RLEACCEL)                          # setting the white color as the transperant area; RLEACCEL is used for better performance on non accelerated displays
        pos_x = random.randint(game_env.constants.screen_width + 10, game_env.constants.screen_width + 50)
        pos_y = random.randint(0, game_env.constants.screen_height - game_env.vegetation_size[1] / 2)
        self.rect = self.surf.get_rect(center=(pos_x, pos_y))                               # create rectange from the cloud screen

    def update(self):
        self.rect.move_ip(-5, 0)                                        # move the cloud towards left at constant speed
        if self.rect.right < 0:                                         # if the cloud has completly moved from the screen, the cloud is killed
            self.kill()
