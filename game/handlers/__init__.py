from datetime import datetime

from game.environment import GameEnvironment


class Handlers():
    def __init__(self):
        self.__game_env = GameEnvironment()

    def log(self, message):
        with open(self.__game_env.static.game_log_file, 'a+') as file_handler:
            file_handler.write('\n[{:%Y-%m-%d %H:%M:%S.%f}] : {}'.format(datetime.now(), message))
