from game.environment import GameEnvironment
from game.sprites.text import Text
from pygame.surface import Surface


class ExitMenuText(Text):
    """ ExitText class extended from Text class.
        It creates the game exit menu with confirmation sprite
    """
    def __init__(self): 
        Text.__init__(self, size=38)
        game_env = GameEnvironment()
        self.__title = Text("Do you want to quit?", 48)

        self.__y_selected_surf = self.font.render("Yes", 1, game_env.static.text_selection_color)        # creating surface with Yes text when highlighted
        self.__n_surf = self.font.render("/No",1, self.color)                                                   # creating surface with No text
        self.__y_surf = self.font.render("Yes/", 1, self.color)                                                 # creating surface with Yes text
        self.__n_selected_surf = self.font.render("No", 1, game_env.static.text_selection_color)          # creating surface with No text when highlighted

        self.__choices = self.__title.surf.get_width()/2 - (self.__y_selected_surf.get_width() + self.__n_surf.get_width())/2 
        self.__highlight_no()
        
    def __recreate_surf(self):
        game_env = GameEnvironment()
        self.surf = Surface((self.__title.surf.get_width(), self.__title.surf.get_height() + self.__y_surf.get_height()), game_env.SRCALPHA)
        self.surf.blit(self.__title.surf, (self.surf.get_width()/2 - self.__title.surf.get_width()/2, 0))

    def update(self, pressed_keys):
        game_env = GameEnvironment()
        if pressed_keys[game_env.K_LEFT]:
            self.__highlight_yes()
            game_env.dynamic.exit = True
        elif pressed_keys[game_env.K_RIGHT]:
            self.__highlight_no()
            game_env.dynamic.exit  = False
        self.rect = self.surf.get_rect(center=(game_env.static.screen_width/2, game_env.static.screen_height/2 + 10))

    def __highlight_yes(self):
        self.__recreate_surf()
        self.surf.blit(self.__y_selected_surf, (self.__choices, self.__title.surf.get_height()))
        self.surf.blit(self.__n_surf, (self.__choices + self.__y_selected_surf.get_width(), self.__title.surf.get_height()))

    def __highlight_no(self):
        self.__recreate_surf()
        self.surf.blit(self.__y_surf, (self.__choices, self.__title.surf.get_height()))
        self.surf.blit(self.__n_selected_surf, (self.__choices + self.__y_surf.get_width(), self.__title.surf.get_height()))

