import re

from pygame.surface import Surface

from game.sprites.text import Text


class NameInputText(Text):
    """ NameInputText class extended from Text class.
        Class is responsible for creating the sprite for taking player name as input
    """
    def __init__(self, game_env): 
        Text.__init__(self, game_env, size=32)                                          # initilizing parent class with default text color as red
        self.__game_env = game_env
        self.__header = Text(self.__game_env, "=== ENTER YOUR NAME ===", 36)
        self.__footer = Text(self.__game_env, "===============================", 36)
        self.__player_name = ''                                                         # default player name
        self.render(self.__player_name)

    def render(self, key):
        if key and re.match(r'[a-zA-Z0-9@. \b\r]',key):                                 # basic input validation; user cannot enter rubbish
            if key == '\x08':                                                           # backspace
                self.__player_name = self.__player_name[:-1]
            elif key == '\r':                                                           # enter key
                if len(self.__player_name.strip()) > 0:                                 # to avoid spaces as name
                    self.__game_env.dynamic.player_name = self.__player_name.strip()
                else:
                    self.__player_name.strip()
            elif len(self.__player_name) <= self.__game_env.static.name_length:         # to avoid longer name
                self.__player_name += key

        self.__render()
        
    def __render(self):
        self.__input = self.font.render(self.__player_name, 1, self.color)
        self.surf = Surface((self.__header.surf.get_width() , self.__header.surf.get_height()*2 + self.__input.get_height()), self.__game_env.SRCALPHA)
        self.surf.blit(self.__header.surf, (self.surf.get_width()/2 - self.__header.surf.get_width()/2, 0))
        self.surf.blit(self.__input, (self.surf.get_width()/2 - self.__input.get_width()/2, self.__header.surf.get_height()))
        self.surf.blit(self.__footer.surf, (self.surf.get_width()/2 - self.__footer.surf.get_width()/2, self.surf.get_height() - self.__footer.surf.get_height()))       
        self.rect = self.surf.get_rect(center=(self.__game_env.static.screen_width/2, self.__game_env.static.screen_height/2))
