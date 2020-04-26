from pygame.surface import Surface
from game.sprites.text import Text

class ReplayText(Text):
    """ ReplayText class extended from Text class.
        It creates the game replay menu sprite
    """
    def __init__(self, game_env): 
        Text.__init__(self, game_env, size=38)                                                          # initilizing parent class with default text color as red
        self.__game_env = game_env
        self.__prefix_surf = self.font.render("Replay ", 1, self.color)                                 # creating surface with the Replay text
        self.__y_selected_surf = self.font.render("Yes", 1, game_env.constants.text_selection_color)    # creating surface with Yes text when highlighted
        self.__n_surf = self.font.render("/No",1, self.color)                                           # creating surface with No text
        self.__y_surf = self.font.render("Yes/", 1, self.color)                                         # creating surface with Yes text
        self.__n_selected_surf = self.font.render("No",1, game_env.constants.text_selection_color)      # creating surface with No text when highlighted
        self.__highlightY()                                                                             # calling method to highlight Yes (the default choice)
        self.replay_choice = True                                                                       # setting replay to True
        
    def __recreateSurf(self):
        # creating default surface of combination of expected length
        self.surf = Surface((self.__prefix_surf.get_width() + self.__y_surf.get_width() + self.__n_surf.get_width(), self.__prefix_surf.get_height()), self.__game_env.SRCALPHA)
        self.surf.blit(self.__prefix_surf, (0,0))                                                       # updating the surface by drawing the prefex surface

    def update(self, pressed_keys):
        if pressed_keys[self.__game_env.K_LEFT]:                                                        # checking if user has pressed LEFT
            self.replay_choice = True                                                                   # setting game replay choice as True
            self.__highlightY()                                                                         # calling method to highlight Yes
        elif pressed_keys[self.__game_env.K_RIGHT]:                                                     # checking if user has pressed RIGHT
            self.replay_choice = False                                                                  # setting game replay choice as False
            self.__highlightN()                                                                         # calling method to highlight No
        self.rect = self.surf.get_rect(center=(self.__game_env.constants.screen_width/2, self.__game_env.constants.screen_height/2 + 10))   # creating default rect and setting its position center below the GAME OVER text

    def __highlightY(self):
        self.__recreateSurf()
        self.surf.blit(self.__y_selected_surf, (self.__prefix_surf.get_width(),0))                                  # updating the surface by drawing the highlighted Yes after the prefix
        self.surf.blit(self.__n_surf, (self.__prefix_surf.get_width() + self.__y_selected_surf.get_width(),0))      # updating the surface by drawing the No after the highlighted Yes

    def __highlightN(self):
        self.__recreateSurf()
        self.surf.blit(self.__y_surf, (self.__prefix_surf.get_width(),0))                                           # updating the surface by drawing the Yes after the prefix
        self.surf.blit(self.__n_selected_surf, (self.__prefix_surf.get_width() + self.__y_surf.get_width(),0))      # updating the surface by drawing the highlighted No after the Yes

