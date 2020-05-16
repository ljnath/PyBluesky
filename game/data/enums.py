from enum import Enum

class InputMode(Enum):
    """ InputMode enumerator which holds the supported input modes for the game
    """
    KEYBOARD = 1,
    MOUSE = 2

class Screen(Enum):
    """ TitleScreen enumerator which holds the available title screens
    """
    GAME_MENU = 0,
    HELP = 1,
    LEADERBOARD = 2
    REPLAY_MENU = 3
    NAME_INPUT = 4
    EXIT_MENU = 5
    GAME_SCREEN = 6
