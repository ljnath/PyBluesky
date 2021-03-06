from pygame.surface import Surface

from game.sprites.text import Text


class ReplayMenuText(Text):
    """ ReplayText class extended from Text class.
        It creates the game replay menu sprite
    """
    def __init__(self, game_env): 
        Text.__init__(self, game_env, size=38)                                                                  # initilizing parent class with default text color as red
        self.__game_env = game_env
        self.__gameover = Text(self.__game_env, "GAME OVER", 60)

        self.__replaytext_surf = self.font.render("Replay ", 1, self.color)                                     # creating surface with the Replay text

        self.__y_selected_surf = self.font.render("Yes", 1, self.__game_env.static.text_selection_color)        # creating surface with Yes text when highlighted
        self.__n_surf = self.font.render("/No",1, self.color)                                                   # creating surface with No text
        self.__y_surf = self.font.render("Yes/", 1, self.color)                                                 # creating surface with Yes text
        self.__n_selected_surf = self.font.render("No",1, self.__game_env.static.text_selection_color)          # creating surface with No text when highlighted

        self.__replaytext_pos_x = self.__gameover.surf.get_width()/2 - (self.__replaytext_surf.get_width() + self.__y_selected_surf.get_width() + self.__n_surf.get_width())/2 

        self.__highlight_yes()                                                                                     # calling method to highlight Yes (the default choice)
        
    def __recreate_surf(self):
        # creating default surface of combination of expected length
        self.surf = Surface((self.__gameover.surf.get_width() , self.__gameover.surf.get_height() + self.__replaytext_surf.get_height()), self.__game_env.SRCALPHA)
        self.surf.blit(self.__gameover.surf, (self.surf.get_width()/2 - self.__gameover.surf.get_width()/2, 0)) # updating the surface by drawing the prefex surface
        self.surf.blit(self.__replaytext_surf, (self.__replaytext_pos_x, self.__gameover.surf.get_height()))    # updating the surface by drawing the prefex surface

    def update(self, pressed_keys):
        if pressed_keys[self.__game_env.K_LEFT]:                                                                # checking if user has pressed LEFT
            self.__game_env.dynamic.replay = True                                                               # setting game replay choice as True
            self.__highlight_yes()                                                                                 # calling method to highlight Yes
        elif pressed_keys[self.__game_env.K_RIGHT]:                                                             # checking if user has pressed RIGHT
            self.__game_env.dynamic.replay  = False                                                             # setting game replay choice as False
            self.__highlight_no()                                                                                 # calling method to highlight No
        self.rect = self.surf.get_rect(center=(self.__game_env.static.screen_width/2, self.__game_env.static.screen_height/2 + 10))   # creating default rect and setting its position center below the GAME OVER text

    def __highlight_yes(self):
        self.__recreate_surf()
        self.surf.blit(self.__y_selected_surf, (self.__replaytext_pos_x + self.__replaytext_surf.get_width(), self.__gameover.surf.get_height()))                                  # updating the surface by drawing the highlighted Yes after the prefix
        self.surf.blit(self.__n_surf, (self.__replaytext_pos_x + self.__replaytext_surf.get_width() + self.__y_selected_surf.get_width(), self.__gameover.surf.get_height()))      # updating the surface by drawing the No after the highlighted Yes

    def __highlight_no(self):
        self.__recreate_surf()
        self.surf.blit(self.__y_surf, (self.__replaytext_pos_x + self.__replaytext_surf.get_width(), self.__gameover.surf.get_height()))                                           # updating the surface by drawing the Yes after the prefix
        self.surf.blit(self.__n_selected_surf, (self.__replaytext_pos_x + self.__replaytext_surf.get_width() + self.__y_surf.get_width(), self.__gameover.surf.get_height()))      # updating the surface by drawing the highlighted No after the Yes
