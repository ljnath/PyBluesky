from game.handlers import Handlers
import os
import pickle

class SerializeHandler(Handlers):
    def __init__(self, file):
        super().__init__()
        self.__file = file

    def serialize(self, object):
        try:
            if object is None:
                return
            with open(self.__file, 'wb') as file_writter:
                pickle.dump(object, file_writter)
        except Exception:
            self.log('Failed to serialize object to file {}'.format(self.__file))
    

    def deserialize(self):
        serialized_object = None
        try:
            if os.path.exists(self.__file):
                with open(self.__file, 'rb') as file_reader:
                    serialized_object = pickle.load(file_reader)
        except Exception:
            self.log('Failed to deserialize file {}'.format(self.__file))
        finally:
            return serialized_object