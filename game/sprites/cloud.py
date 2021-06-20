import random

from game.environment import GameEnvironment
from pygame import image, sprite
from pygame.font import Font


class Cloud(sprite.Sprite):
    """ Cloud sprite class for creating and updating the cloud in the game screen
    """
    def __init__(self):
        super(Cloud, self).__init__()                                                               # initilizing parent class pygame.sprite.Sprite
        self.__game_env = GameEnvironment()
        self.surf = image.load(random.choice(self.__game_env.static.clouds)).convert()    # loading cloud image
        self.surf.set_colorkey((255, 255, 255), self.__game_env.RLEACCEL)                           # setting the white color as the transperant area; RLEACCEL is used for better performance on non accelerated displays
        self.__speed = 5
        pos_x = random.randint(self.__game_env.static.screen_width + 10, self.__game_env.static.screen_width + 50)
        pos_y = random.randint(0, self.__game_env.static.screen_height - self.__game_env.vegetation_size[1] / 2)
        self.rect = self.surf.get_rect(center=(pos_x, pos_y))                                       # create rectange from the cloud screen
        
        if self.__game_env.dynamic.update_available:
            self.update_cloud()

    def update(self):
        self.rect.move_ip(-self.__speed, 0)                                                         # move the cloud towards left at constant speed
        if self.rect.right < 0:                                                                     # if the cloud has completly moved from the screen, the cloud is killed
            self.kill()

    def update_cloud(self):                                                                         # adding 'Update avilable' text to cloud when a new version of the game is available
        font = Font(self.__game_env.static.game_font, 14)
        txt_update_surf = font.render(' Update', 1, self.__game_env.static.text_default_color)
        txt_available_surf = font.render(' Available', 1, self.__game_env.static.text_default_color)
        self.surf.blit(txt_update_surf, (12,13))
        self.surf.blit(txt_available_surf, (5,23))
        self.__speed = 2
