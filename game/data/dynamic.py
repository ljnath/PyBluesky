
from game.data.static import StaticData
from game.data.enums import InputMode, TitleScreen
from pygame.mixer import Sound
from pygame.sprite import Group

class DynamicData():
    """ Class which holds all the game variables
    """
    def __init__(self):
        self.__static= StaticData()
        self.__collision_sound = Sound(self.__static.game_sound.get('collision'))
        self.__levelup_sound = Sound(self.__static.game_sound.get('levelup'))
        self.__shoot_sound = Sound(self.__static.game_sound.get('shoot'))
        self.__hit_sound = Sound(self.__static.game_sound.get('hit'))
        self.__powerup_sound = Sound(self.__static.game_sound.get('powerup'))
        self.__game_input = InputMode.KEYBOARD
        self.__all_sprites = Group()
        self.__bullets = Group()
        self.__ammo = 100
        self.__noammo_sprite = None
        self.__game_level = 1
        self.__update_available = False
        self.__active_screen = TitleScreen.GAMEMENU
        self.__game_score = 0
        self.__game_playtime = 0
        self.__replay = True
        
    @property
    def collision_sound(self):
        return self.__collision_sound

    @property
    def levelup_sound(self):
        return self.__levelup_sound

    @property
    def shoot_sound(self):
        return self.__shoot_sound

    @property
    def hit_sound(self):
        return self.__hit_sound

    @property
    def powerup_sound(self):
        return self.__powerup_sound

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

    @property
    def bullets(self):
        return self.__bullets

    @bullets.setter
    def bullets(self, value):
        self.__bullets = value

    @property
    def ammo(self):
       return self.__ammo
    
    @ammo.setter
    def ammo(self, value):
        self.__ammo = value if value <= self.__static.max_ammo else self.__static.max_ammo

    @property
    def noammo_sprite(self):
       return self.__noammo_sprite
    
    @noammo_sprite.setter
    def noammo_sprite(self, value):
        self.__noammo_sprite = value

    @property
    def game_level(self):
        return self.__game_level

    @game_level.setter
    def game_level(self, value):
        self.__game_level = value

    @property
    def update_available(self):
        return self.__update_available

    @update_available.setter
    def update_available(self, value):
        self.__update_available = value

    @property
    def active_screen(self):
        return self.__active_screen

    @active_screen.setter
    def active_screen(self, value):
        self.__active_screen = value

    @property
    def game_score(self):
        return self.__game_score

    @game_score.setter
    def game_score(self, value):
        self.__game_score = value

    @property
    def game_playtime(self):
        return self.__game_playtime

    @game_playtime.setter
    def game_playtime(self, value):
        self.__game_playtime = value

    @property
    def replay(self):
        return self.__replay

    @replay.setter
    def replay(self, value):
        self.__replay = value
