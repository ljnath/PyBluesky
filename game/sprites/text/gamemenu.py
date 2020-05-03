from game.data.enums import InputMode
from game.sprites.text import Text
from game.sprites.jet import Jet
from pygame.surface import Surface

class GameMenuText(Text):
    """ GameMenuText class extended from Text class.
        It creates the game input menu sprite
    """
    def __init__(self, game_env): 
        Text.__init__(self, game_env, size=42)                                                                          # initilizing parent class with default text color as red
        self.__game_env = game_env
        self.__jet = Jet(game_env)                                                                                      # creating a of jet 
        self.__prefix_surf = self.font.render('Select game input', 1, self.color)                                       # creating surface with the prefix text
        self.__mouse = self.font.render(' Mouse',1, self.color)                                                         # creating surface with mouse text
        self.__keybrd = self.font.render(' Keyboard', 1, self.color)                                                    # creating surface with mouse text

        keybrd_surf = self.font.render(' Keyboard', 1, game_env.static.text_selection_color)                            # creating surface with Keyboard text when highlighted
        self.__keybrd_selected = Surface((self.__jet.surf.get_width() + keybrd_surf.get_width(), keybrd_surf.get_height()), game_env.SRCALPHA)     # creating surface for jet and highlighted keyboard text
        self.__keybrd_selected.blit(self.__jet.surf, (0,0))                                                             # drawing the jet
        self.__keybrd_selected.blit(keybrd_surf, (self.__jet.surf.get_width(), 0))                                      # drawing the highligted keyboard text after the jet image 
        
        mouse_surf = self.font.render(' Mouse', 1, game_env.static.text_selection_color)                                # creating surface with mouse text when highlighted
        self.__mouse_selected = Surface((self.__jet.surf.get_width() + mouse_surf.get_width(), mouse_surf.get_height()), game_env.SRCALPHA)       # creating surface for jet and highlighted mouse text
        self.__mouse_selected.blit(self.__jet.surf, (0,0))                                                              # drawing the jet
        self.__mouse_selected.blit(mouse_surf, (self.__jet.surf.get_width(), 0))                                        # drawing the highligted mouse text after the jet image 

        self.__highlightKeyboard()                                                                                      # calling method to highlight keyboard (the default choice)
        
    def __recreateSurf(self):
        self.surf = Surface((self.__prefix_surf.get_width(), self.__prefix_surf.get_height() * 3), self.__game_env.SRCALPHA)                # creating default surface of combinted expected length
        self.surf.blit(self.__prefix_surf, (0,0))                                                                                           # drawing the prefix text

    def update(self, pressed_keys):
        if pressed_keys[self.__game_env.K_UP]:                                                                          # checking if user has pressed UP
            self.__game_env.dynamic.game_input = InputMode.KEYBOARD                                                     # setting game input mode as keyboard
            self.__highlightKeyboard()                                                                                  # calling method to highlight keyboard
        elif pressed_keys[self.__game_env.K_DOWN]:                                                                      # checking if user has pressed DOWN
            self.__game_env.dynamic.game_input = InputMode.MOUSE                                                        # setting game input mode as mouse
            self.__highlightMouse()                                                                                     # calling method to highlight mouse
        self.rect = self.surf.get_rect(center=(self.__game_env.static.screen_width/2, self.__game_env.static.screen_height/2 + 50))        # creating default rect and setting its position center

    def __highlightKeyboard(self):
        self.__recreateSurf()                                                                                           # recreating the surface, as we will re-draw
        self.surf.blit(self.__keybrd_selected, (0,self.__prefix_surf.get_height()))                                     # drawing the jet+keyboard text
        self.surf.blit(self.__mouse, (self.__jet.surf.get_width(), self.__prefix_surf.get_height() * 2))                # drawing the mouse text

    def __highlightMouse(self):
        self.__recreateSurf()                                                                                           # recreating the surface, as we will re-draw
        self.surf.blit(self.__keybrd, (self.__jet.surf.get_width(), self.__prefix_surf.get_height()))                   # drawing keyboard text
        self.surf.blit(self.__mouse_selected, (0, self.__prefix_surf.get_height()*2))                                   # drawing jet+mouse text
