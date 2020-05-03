from enum import Enum


class InputMode(Enum):
    """ InputMode enumerator which holds the supported input modes for the game
    """
    KEYBOARD = 1,
    MOUSE = 2

class Screen(Enum):
    """ TitleScreen enumerator which holds the available title screens
    """
    GAMEMENU = 0,
    HELP = 1,
    LEADERBOARD = 2
    REPLAYMENU = 3
    NAMEINPUT = 4
    