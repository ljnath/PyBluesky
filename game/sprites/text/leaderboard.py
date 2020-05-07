from game.sprites.text import Text
from pygame.surface import Surface
from game.handlers.leaderboard import LeaderBoardHandler

class LeaderBoardText(Text):
    """ LeaderBoardText class extended from Text class.
        It creates the the leaderboard table sprite
    """
    def __init__(self, game_env): 
        Text.__init__(self, game_env, size=20)
        self.__game_env = game_env
        name_length = self.__game_env.static.name_length * 2
        leaders = LeaderBoardHandler().load()
        seperator = self.font.render('============================================================================', 1, self.color)
        header = self.font.render('=== HALL OF FAME ===', 1, self.color)
        all_surfaces = []
        all_surfaces.append(seperator)
        all_surfaces.append(self.font.render('{}-{}-{}-{}-{}'.format('RANK'.center(5), 'NAME'.center(name_length), 'SCORE'.center(10), 'LEVEL'.center(5), 'ACCURACY'), 1, self.color))
        all_surfaces.append(seperator)
        try:
            if len(leaders) == 0:
                all_surfaces.append(self.font.render('No records, make sure you have working internet connectivity', 1, self.color))

            for index, score in enumerate(leaders['scores']):
                all_surfaces.append(self.font.render('{}-{}-{}-{}-{}'.format(str(index+1).center(5), score['name'][:name_length].center(name_length), str(score['score']).center(10), str(score['level']).center(5), str(score['accuracy'] + '%').center(9)), 1, self.color))
        except:
            pass
        all_surfaces.append(seperator)

        self.surf = Surface((all_surfaces[2].get_width(), all_surfaces[0].get_height() * (len(all_surfaces) + 1)), self.__game_env.SRCALPHA)

        self.surf.blit(header, (self.surf.get_width()/2 - header.get_width()/2, 0))
        for index, temp_surf in enumerate(all_surfaces):
            self.surf.blit(temp_surf, (0, header.get_height() + index * temp_surf.get_height()))

        self.rect = self.surf.get_rect(center=(self.__game_env.static.screen_width/2, self.__game_env.static.screen_height/2))
