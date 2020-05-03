import http.client
import mimetypes
from getpass import getuser
from datetime import datetime
from json import loads, dumps

API_KEY = ''

class NetworkHandler():
    def __init__(self):
        pass

    @staticmethod
    def log(message):
        with open('network.log', 'a+') as file_handler:
            file_handler.write('\n[{:%Y-%m-%d %H:%M:%S.%f}] : {}'.format(datetime.now(), message))

    @staticmethod
    def check_game_update(game_env):
        try:
            conn = http.client.HTTPSConnection("www.ljnath.com")
            conn.request("GET", "/api/pybluesky?action=getUpdate&apiKey={}".format(API_KEY), headers={ 'Content-Type': 'application/json' })
            response = conn.getresponse()
            if response.code != 200:
                raise Exception()
            json_reponse = loads(response.read().decode('utf-8'))
            if json_reponse['version'] != game_env.static.version:
                game_env.dynamic.update_available = True
                NetworkHandler.log('New game version {} detected'.format(json_reponse['version']))
        except:
            NetworkHandler.log('Failed to check for game update')

    @staticmethod
    def get_leaders():
        leaders = {}
        try:
            conn = http.client.HTTPSConnection("www.ljnath.com")
            conn.request("GET", "/api/pybluesky?action=getTopScores&apiKey={}".format(API_KEY), headers={ 'Content-Type': 'application/json' })
            response = conn.getresponse()
            if response.code != 200:
                raise Exception()
            leaders = loads(response.read().decode('utf-8'))
        except:
            NetworkHandler.log('Failed to get game leaders')
        finally:
            return leaders
        
    @staticmethod
    def submit_score(score):
        current_user = getuser()
        try:
            payload = {
                'apiKey' : API_KEY,
                'name' : current_user,
                'score' : int(score)
            }
            conn = http.client.HTTPSConnection("www.ljnath.com")
            conn.request("PUT", "/api/pybluesky", dumps(payload), headers={ 'Content-Type': 'application/json' })
            response = conn.getresponse()
            if response.code != 201:
                raise Exception()
            NetworkHandler.log('Successfully sumbitted score {} for user {}'.format(score, current_user))
        except:
            NetworkHandler.log('Failed to sumbitted score {} for user {}'.format(score, current_user))

    