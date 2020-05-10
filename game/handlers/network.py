import http.client
import mimetypes
import platform
import os
import pickle
from datetime import datetime
from time import time
from json import loads, dumps
from game.handlers import Handlers
from game.handlers.serialize import SerializeHandler

class NetworkHandler(Handlers):
    def __init__(self, api_key):
        Handlers().__init__()
        self.__api_key = api_key
        self.__api_host = 'app.ljnath.com'
        self.__endpoint = '/pybluesky/'
        self.__sync_file = 'data/offline.dat'
        self.__headers = { 'Content-Type': 'application/json' }
        self.__https_connection = http.client.HTTPSConnection(self.__api_host)
        self.__serialize_handler = SerializeHandler(self.__sync_file)

    def check_game_update(self, game_env):
        try:
            self.__https_connection.request("GET", "{}?action=getUpdate&apiKey={}".format(self.__endpoint, self.__api_key), headers=self.__headers )
            response = self.__https_connection.getresponse()
            if response.code != 200:
                raise Exception()
            json_reponse = loads(response.read().decode('utf-8'))
            if json_reponse['version'] != game_env.static.version:
                game_env.dynamic.update_available = True
                game_env.dynamic.update_url = json_reponse['url']
                self.log('New game version {} detected'.format(json_reponse['version']))
        except:
            self.log('Failed to check for game update')
            
        self.submit_result(game_env, sync_only=True)

    def get_leaders(self):
        leaders = {}
        try:
            self.__https_connection.request("GET", "{}?action=getTopScores&apiKey={}".format(self.__endpoint, self.__api_key), headers=self.__headers)
            response = self.__https_connection.getresponse()
            if response.code != 200:
                raise Exception()
            leaders = loads(response.read().decode('utf-8'))
        except Exception as e:
            print(e)
            self.log('Failed to get game leaders')
        finally:
            return leaders
        
    def submit_result(self, game_env, sync_only = False):
        payloads = []
        deserialized_object = self.__serialize_handler.deserialize()
        if deserialized_object:
            payloads = list(deserialized_object)

        if not sync_only:
            payload = {
                'apiKey' : self.__api_key,
                'name' : game_env.dynamic.player_name,
                'score' : game_env.dynamic.game_score,
                'level' : game_env.dynamic.game_level,
                'accuracy' : game_env.dynamic.accuracy,
                'platform' : '{} {}'.format(platform.system(), platform.release()),
                "epoch": int(time())
            }
            payloads.append(payload)

        unprocessed_payloads = []
        for payload in payloads:
            if self.__post_results(payload):
                self.log('Successfully submitted result: score={}, name={}, level={}'.format(payload.get('score'), payload.get('name'), payload.get('level')))
            else:
                payload.update({'apiKey':''})
                unprocessed_payloads.append(payload)
                self.log('Falied to submit result: score={}, name={}, level={}'.format(payload.get('score'), payload.get('name'), payload.get('level')))
        self.__serialize_handler.serialize(unprocessed_payloads)

    def __post_results(self, payload):
        result = True
        try:
            payload['apiKey'] = self.__api_key
            self.__https_connection = http.client.HTTPSConnection(self.__api_host)
            self.__https_connection.request("PUT", self.__endpoint, dumps(payload), headers=self.__headers)
            response = self.__https_connection.getresponse()
            if response.code != 201:
                raise Exception()
        except:
            result = False
        finally:
            return result