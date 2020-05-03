import pickle
import os
from game.handlers.network import NetworkHandler

class LeaderBoardHandler():
    def __init__(self):
        self.__db = 'leaderboard.dat'

    def load(self):
        leaders = []
        try:
            if os.path.exists(self.__db):
                with open(self.__db, 'rb') as file_reader:
                    leaders = pickle.load(file_reader)
        except Exception:
            print('Failed to load leaders from file')
        finally:
            return leaders

    def dump(self, leaders):
        try:
            if not leaders:
                return

            with open(self.__db, 'wb') as file_writter:
                pickle.dump(leaders, file_writter)
        except Exception:
            print('Failed to dump leaders to file')
    
    def update(self):
        self.dump(NetworkHandler().get_leaders())
