from enum import Enum
from pygame.mixer import Sound
from pygame.sprite import Group

class InputMode(Enum):
    """ InputMode enumerator which holds the supported input modes for the game
    """
    KEYBOARD = 1,
    MOUSE = 2


class Constants():
    """ Class which holds all the game constants
    """
    def __init__(self):
        """ default constructor"""
        pass

    @property
    def screen_width(self):
        return 800                          # game resolution is 800x600

    @property
    def screen_height(self):
        return 600                          # game resolution is 800x600
    
    @property
    def text_default_color(sef):
        return (255,0,0)                    # default color is red
    
    @property
    def text_selection_color(sef):
        return (0,0,255)                    # selection color is blue

    @property
    def game_font(self):
        return 'font/ARCADE.ttf'            # game font file path

    @property
    def clouds(self):
        return ('image/cloud1.png', 'image/cloud2.png', 'image/cloud3.png') # all game cloud designs

    @property
    def missile_image(self):
        return 'image/missile.png'          # missle image path

    @property
    def jet_image(self):
        return 'image/jet.png'              # jet image path

    @property
    def cloud_per_sec(self):
        return 1                            # number of cloud to be spawned per second

    @property
    def missile_per_sec(self):
        return 4                            # number of missiles to be spawned per seconds

    @property
    def background_default(self):
        return (135, 206, 250)              # skyblue color

    @property
    def background_special(self):
        return (196, 226, 255)              # pale skyblue

    @property
    def fps(self):
        return 30                           # game should run at 30 pfs

    @property
    def game_sound(self):
        return {
            'music' : 'audio/Apoxode_-_Electric_1.mp3',   # sound source: http://ccmixter.org/files/Apoxode/59262 ; License: https://creativecommons.org/licenses/by/3.0/
            'move_up' : 'audio/Rising_putter.ogg',        # sound sources: Jon Fincher
            'move_down' : 'audio/Falling_putter.ogg',     # sound sources: Jon Fincher
            'collision' : 'audio/collision.ogg'
        }


class Variables():
    """ Class which holds all the game variables
    """
    def __init__(self):
        constants= Constants()
        self.__moveup_sound = Sound(constants.game_sound.get('move_up'))
        self.__movedown_sound = Sound(constants.game_sound.get('move_down'))
        self.__collision_sound = Sound(constants.game_sound.get('collision'))
        self.__game_input = InputMode.KEYBOARD
        self.__all_sprites = Group()

    @property
    def moveup_sound(self):
        return self.__moveup_sound

    @property
    def movedown_sound(self):
        return self.__movedown_sound

    @property
    def collision_sound(self):
        return self.__collision_sound

    @property
    def game_input(self):
        return self.__game_input

    @game_input.setter
    def game_input(self, value):
        self.__game_input = value

    @property
    def all_sprites(self):
        return self.__all_sprites

    @all_sprites.setter
    def all_sprites(self, value):
        self.__all_sprites = value
