from datetime import datetime

class Handlers():
    def __init__(self):
        self.__log_files = 'game.log'

    def log(self, message):
        with open(self.__log_files, 'a+') as file_handler:
            file_handler.write('\n[{:%Y-%m-%d %H:%M:%S.%f}] : {}'.format(datetime.now(), message))
