from game.data import Constants, Variables
import random
from pygame import image
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

    def get_random_point_on_right(self):
        pos_x = random.randint(self.__constants.screen_width + 20, self.__constants.screen_width + 100)     # generating random x position
        pos_y = random.randint(0, self.__constants.screen_height)                                           # generating random y position
        return (pos_x, pos_y)

    def get_random_point_on_top(self):
        pos_x = random.randint(0, self.__constants.screen_width)                    # generating random x position
        pos_y = random.randint(10, 20)                                              # generating random y position
        return (pos_x, pos_y * -1)
        
    def get_image_size(self, image_file):
        image_surf = image.load(image_file)
        return (image_surf.get_width(), image_surf.get_height())

    @property
    def vegetation_size(self):
        return self.get_image_size(self.__constants.vegetation[0])
            
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