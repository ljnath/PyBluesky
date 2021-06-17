from pygame.surface import Surface

from game.data.enums import StartChoice
from game.sprites.jet import Jet
from game.sprites.text import Text


class GameMenuText(Text):
    """ GameMenuText class extended from Text class.
        It creates the game start choice menu sprite
    """
    def __init__(self, game_env): 
        Text.__init__(self, game_env, size=36)                                                                          # initilizing parent class with default text color as red
        self.__game_env = game_env
        
        exit_text = 'Exit'
        start_game_text = 'Start Game'
        
        self.__jet = Jet(game_env)                                                                                      # creating a of jet 
        self.__prefix_surf = self.font.render("What do you want to do ?", 1, self.color)                                # creating surface with the prefix text
        self.__exit = self.font.render(f' {exit_text}',1, self.color)                                                   # creating surface with Exit text
        self.__play = self.font.render(f' {start_game_text}', 1, self.color)                                            # creating surface with Play Game text

        start_game_surface = self.font.render(f' {start_game_text}', 1, game_env.static.text_selection_color)                                                       # creating surface with Start Game text when highlighted
        self.__start_game_selected = Surface((self.__jet.surf.get_width() + start_game_surface.get_width(), start_game_surface.get_height()), game_env.SRCALPHA)    # creating surface for jet and highlighted StartGame text
        self.__start_game_selected.blit(self.__jet.surf, (0,0))                                                                                                     # drawing the jet
        self.__start_game_selected.blit(start_game_surface, (self.__jet.surf.get_width(), 0))                                                                       # drawing the highligted StartGame text after the jet image 
        
        exit_surface = self.font.render(f' {exit_text}', 1, game_env.static.text_selection_color)                                                               # creating surface with Exit text when highlighted
        self.__exit_selected = Surface((self.__jet.surf.get_width() + exit_surface.get_width(), exit_surface.get_height()), game_env.SRCALPHA)                  # creating surface for jet and highlighted Exit text
        self.__exit_selected.blit(self.__jet.surf, (0,0))                                                                                                       # drawing the jet
        self.__exit_selected.blit(exit_surface, (self.__jet.surf.get_width(), 0))                                                                               # drawing the highligted Exit text after the jet image 
       
        self.__left_padding = self.__prefix_surf.get_width()/2 - self.__start_game_selected.get_width() / 2
        self.__highlight_start_game()                                                                                                                           # calling method to highlight StartGame (the default choice)
        
    def __recreate_surface(self):
        self.surf = Surface((self.__prefix_surf.get_width(), self.__prefix_surf.get_height() * 3), self.__game_env.SRCALPHA)                # creating default surface of combinted expected length
        self.surf.blit(self.__prefix_surf, (0,0))                                                                                           # drawing the prefix text

    def update(self, accleration_value):
        if not accleration_value or len(accleration_value) != 3 or not accleration_value[0]:                                                # validation of accleration_value
            return
        
        x_axis = accleration_value[0]
        if x_axis > self.__game_env.static.acceleration_threshold:                                                                          # when device accleration is moved DOWN
            self.__game_env.dynamic.game_start_choice = StartChoice.EXIT                                                                    # StartChoice 'Exit'is selected
            self.__highlight_exit()                                                                                                         # StartChoice 'Exit'is highlighted
        elif x_axis < self.__game_env.static.acceleration_threshold * -1:                                                                   # when device accleration is moved UP
            self.__game_env.dynamic.game_start_choice = StartChoice.START                                                                   # StartChoice 'Start Game'is selected
            self.__highlight_start_game()                                                                                                   # StartChoice 'Start Game'is highlighted
            
        self.rect = self.surf.get_rect(center=(self.__game_env.static.screen_width/2, self.__game_env.static.screen_height/2 + 50))         # creating default rect and setting its position center

    def __highlight_start_game(self):
        self.__recreate_surface()                                                                                                           # recreating the surface, as we will re-draw
        self.surf.blit(self.__start_game_selected, (self.__left_padding ,self.__prefix_surf.get_height()))                                  # drawing the jet+StartGame text
        self.surf.blit(self.__exit, (self.__left_padding  + self.__jet.surf.get_width(), self.__prefix_surf.get_height() * 2))              # drawing the Exit text

    def __highlight_exit(self):
        self.__recreate_surface()                                                                                                           # recreating the surface, as we will re-draw
        self.surf.blit(self.__play, (self.__left_padding  + self.__jet.surf.get_width(), self.__prefix_surf.get_height()))                  # drawing StartGame text
        self.surf.blit(self.__exit_selected, (self.__left_padding , self.__prefix_surf.get_height()*2))                                     # drawing jet+Exit text
