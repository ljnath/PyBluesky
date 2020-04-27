import pygame

class Text(pygame.sprite.Sprite):
    """ Text class for create sprite out of text
    """
    def __init__(self, game_env, text='', size=0, color=None, x_pos=None, y_pos=None):
        pygame.sprite.Sprite.__init__(self)                                                 # initializing parent class
        self.__game_env = game_env
        self.color = game_env.constants.text_default_color if color is None else color      # storing argument color in class variable
        self.font = pygame.font.Font(game_env.constants.game_font, size)                    # loading font and creating class variable font with given size
        self.surf = self.font.render(text, 1, self.color)                                   # creating surface by rendering the text
        if not x_pos:
            x_pos = game_env.constants.screen_width / 2                                     # deafult position is set to center of screen
        if not y_pos:
            y_pos = game_env.constants.screen_height / 2                                    # deafult position is set to center of screen
        self.rect = self.surf.get_rect(center=(x_pos, y_pos))                               # creating rectangle from the surface
        self.__forward_move = True
        self.__forward_up = True

    
    def render(self, text):
        self.surf = self.font.render(text, 2, self.color)                                   # dynamically updating the surface with updated text

    def moveOnXaxis(self, speed):
        """ Method to move the text across the X axis
        """
        if not self.__forward_move and self.rect.x <= 0:
            self.__forward_move = True
        elif self.__forward_move and self.rect.x + self.rect.width >= self.__game_env.constants.screen_width:
            self.__forward_move = False
        self.rect.x += speed if self.__forward_move else (speed*-1)
    
    def moveOnYaxis(self, speed):
        """ Method to move the text across the Y axis
        """
        if not self.__forward_up and self.rect.y <= 0:
            self.__forward_up = True
        elif self.__forward_up and self.rect.y + self.rect.height >= self.__game_env.constants.screen_height:
            self.__forward_up = False
        self.rect.y += speed if self.__forward_up else (speed*-1)