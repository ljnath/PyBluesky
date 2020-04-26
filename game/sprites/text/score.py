from game.sprites.text import Text
# Define a ScoreText class object by Text class
class ScoreText(Text):
    """ ScoreText class extended from Text class.
        It creates the game score sprite
    """
    def __init__(self, game_env):
        Text.__init__(self, game_env, text="TIME 0 SCORE 0", size=28, color=(255,255,255))                          # initializing parent class with defautl text and color
        self.rect = self.surf.get_rect(topright=(game_env.constants.screen_width-10-self.surf.get_width() / 2, 2))  # creating rectangle from text surface
    
    def update(self, playtime, score):
        length = 5                                                                                                  # setting max length of score
        self.surf = self.font.render("TIME {} SCORE {}".format(str(playtime).zfill(length), str(score).zfill(length)), 1, self.color)   # updating scoreboard score and time
