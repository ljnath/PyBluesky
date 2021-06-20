import random

from game.environment import GameEnvironment
from pygame import image, sprite


# Missile class which holds missile attributes and behaviour
class Missile(sprite.Sprite):
    """ Missile sprite class for creating and updating the missile in the game screen
    """
    def __init__(self):
        super(Missile, self).__init__()                                                                                 # initilizing parent class pygame.sprite.Sprite
        self.__game_env = GameEnvironment()
        self.surf = image.load(self.__game_env.static.missile_activated_image).convert()                                # loading missile image from file
        self.surf.set_colorkey((255, 255, 255), self.__game_env.RLEACCEL)                                               # setting the white color as the transperant area; RLEACCEL is used for better performance on non accelerated displays
        pos_x = random.randint(self.__game_env.static.screen_width + 10, self.__game_env.static.screen_width + 60)      # generating random x position
        pos_y = random.randint(0, self.__game_env.static.screen_height - self.__game_env.vegetation_size[1] / 2)        # generating random y position
        self.rect = self.surf.get_rect(center=(pos_x, pos_y))                                                           # create rectange from the missile screen
        self.__activated = True                                                                                         # bad missiles will drop down
        self.__speed = random.randint(5, 20)                                                                            # generating random speed for the missle
        boost_factor = self.__game_env.dynamic.game_level // 10                                                         # increasing missile speed by 5% every 10th level
        self.__speed += int(self.__speed * (boost_factor * 5) / 100)

    def update(self):
        if not self.__activated:
            self.rect.move_ip(0, 10)                                                                    # missile moves down
        else:
            self.rect.move_ip(-self.__speed, 0)                                                         # missile moves towards jet

        if self.rect.right < 0 or self.rect.bottom > self.__game_env.static.screen_height:              # if the missile has completly moved from the screen, the missile is killed
            self.kill()

    def deactivate(self):
        self.__activated = False                                                                        # marking the current missile as bad
        self.surf = image.load(self.__game_env.static.missile_deactivated_image).convert()       # updating missle image when deactivated
        self.surf.set_colorkey((255, 255, 255), self.__game_env.RLEACCEL)                               # adding transperacny to image
