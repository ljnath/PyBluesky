import pickle
import os
from game.handlers import Handlers
from game.handlers.network import NetworkHandler

class LeaderBoardHandler(Handlers):
    def __init__(self):
        super().__init__()
        self.__db = 'leaders.dat'

    def load(self):
        leaders = []
        try:
            if os.path.exists(self.__db):
                with open(self.__db, 'rb') as file_reader:
                    leaders = pickle.load(file_reader)
        except Exception:
            self.log('Failed to load leaders from file')
        finally:
            return leaders

    def dump(self, leaders):
        try:
            if not leaders:
                return

            with open(self.__db, 'wb') as file_writter:
                pickle.dump(leaders, file_writter)
        except Exception:
            self.log('Failed to dump leaders to file')
    
    def update(self, api_key):
        self.dump(NetworkHandler().get_leaders(api_key))
