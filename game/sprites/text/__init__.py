import pygame

class Text(pygame.sprite.Sprite):
    """ Text class for create sprite out of text
    """
    def __init__(self, game_env, text='', size=0, color=None, x_pos=None, y_pos=None):
        pygame.sprite.Sprite.__init__(self)                                                 # initializing parent class
        self.color = game_env.constants.text_default_color if color is None else color      # storing argument color in class variable
        self.font = pygame.font.Font(game_env.constants.game_font, size)                    # loading font and creating class variable font with given size
        self.surf = self.font.render(text, 1, self.color)                                   # creating surface by rendering the text
        if not x_pos:
            x_pos = game_env.constants.screen_width / 2                                     # deafult position is set to center of screen
        if not y_pos:
            y_pos = game_env.constants.screen_height / 2                                    # deafult position is set to center of screen
        self.rect = self.surf.get_rect(center=(x_pos, y_pos))                               # creating rectangle from the surface
    
    def render(self, text):
        self.surf = self.font.render(text, 2, self.color)                                   # dynamically updating the surface with updated text
