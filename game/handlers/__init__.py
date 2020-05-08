from datetime import datetime

class Handlers():
    def __init__(self):
        pass

    def log(self, message):
        with open('game.log', 'a+') as file_handler:
            file_handler.write('\n[{:%Y-%m-%d %H:%M:%S.%f}] : {}'.format(datetime.now(), message))
