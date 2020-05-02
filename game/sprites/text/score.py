from game.sprites.text import Text
# Define a ScoreText class object by Text class
class ScoreText(Text):
    """ ScoreText class extended from Text class.
        It creates the game score sprite
    """
    def __init__(self, game_env):
        Text.__init__(self, game_env, text="LEVEL 00 TIME 0 AMMO 0 SCORE 0", size=28, color=(103,103,103))                             # initializing parent class with defautl text and color
        self.__game_env = game_env
        self.rect = self.surf.get_rect(topright=(self.__game_env.constants.screen_width-self.surf.get_width()/2 + 30, 2))       # creating rectangle from text surface
    
    def update(self, playtime, score):
        self.surf = self.font.render("LEVEL {} TIME {} AMMO {} SCORE {}".format(str(self.__game_env.variables.game_level).zfill(2), str(playtime).zfill(5), str(self.__game_env.variables.ammo).zfill(3),str(score).zfill(8)), 1, self.color)   # updating scoreboard score and time
