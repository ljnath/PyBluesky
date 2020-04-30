from game.data import Constants, Variables
import random

 # importing here to avoid reimporting in all the sub modules
from pygame.locals import (
    SRCALPHA,
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_RETURN,
    K_SPACE,
    KEYDOWN,
    MOUSEMOTION,
    MOUSEBUTTONDOWN,
    FULLSCREEN,
    QUIT,
)

class GameEnvironment():
    """ Game environment which holds the game contants, variables as well as pygame constants
    """
    def __init__(self):
        self.__constants = Constants()
        self.__variables = Variables()

    def get_random_point(self):
        x_pos = random.randint(self.__constants.screen_width + 20, self.__constants.screen_width + 100)     # generating random x position
        y_pos = random.randint(0, self.__constants.screen_height)                                           # generating random y position
        return (x_pos, y_pos)
        
    @property
    def constants(self):
        return self.__constants
    
    @property
    def variables(self):
        return self.__variables

    @property
    def RLEACCEL(self):
        return RLEACCEL

    @property
    def SRCALPHA(self):
        return SRCALPHA

    @property
    def K_UP(self):
        return K_UP

    @property
    def K_DOWN(self):
        return K_DOWN

    @property
    def K_LEFT(self):
        return K_LEFT

    @property
    def K_RIGHT(self):
        return K_RIGHT

    @property
    def K_ESCAPE(self):
        return K_ESCAPE

    @property
    def K_RETURN(self):
        return K_RETURN

    @property
    def KEYDOWN(self):
        return KEYDOWN

    @property
    def FULLSCREEN(self):
        return FULLSCREEN

    @property
    def RLEACCEL(self):
        return RLEACCEL

    @property
    def QUIT(self):
        return QUIT

    @property
    def MOUSEMOTION(self):
        return MOUSEMOTION

    @property
    def K_SPACE(self):
        return K_SPACE

    @property
    def MOUSEBUTTONDOWN(self):
        return MOUSEBUTTONDOWN