import pygame
import random

# Missile class which holds missile attributes and behaviour
class Missile(pygame.sprite.Sprite):
    """ Missile sprite class for creating and updating the missile in the game screen
    """
    def __init__(self, game_env):
        super(Missile, self).__init__()                                             # initilizing parent class pygame.sprite.Sprite
        self.surf = pygame.image.load(game_env.constants.missile_image).convert()   # loading missile image from file
        self.surf.set_colorkey((255, 255, 255), game_env.RLEACCEL)                  # setting the white color as the transperant area; RLEACCEL is used for better performance on non accelerated displays
        self.__speed = random.randint(5, 20)                                        # generating random speed for the missle
        self.rect = self.surf.get_rect(center=game_env.get_random_point_on_right()) # create rectange from the missile screen
        self.__activated = True                                                     # bad missiles will drop down

    def update(self):
        if not self.__activated:
            self.rect.move_ip(0, 10)                                                 # missile moves down
        else:
            self.rect.move_ip(-self.__speed, 0)                                     # missile moves towards jet

        if self.rect.right < 0 or self.rect.bottom < 0:                             # if the missile has completly moved from the screen, the missile is killed
            self.kill()

    def deactivate(self):
        self.__activated = False                                                           # marking the current missile as bad                                           