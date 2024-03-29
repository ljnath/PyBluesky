import asyncio
import os
import pickle
import platform
from datetime import datetime
from json import dumps, loads
from time import time

import aiohttp

from game.handlers import Handlers
from game.handlers.serialize import SerializeHandler


class NetworkHandler(Handlers):
    def __init__(self, api_key):
        Handlers().__init__()
        self.__api_key = api_key
        self.__api_endpoint = 'https://app.ljnath.com/pybluesky/'
        self.__sync_file = 'data/offline.dat'
        self.__serialize_handler = SerializeHandler(self.__sync_file)

    async def check_game_update(self, game_env):
        try:
            get_parameters = {'action': 'getUpdate', 'apiKey': self.__api_key}
            async with aiohttp.ClientSession() as session:
                async with session.get(self.__api_endpoint, params=get_parameters, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status != 200:
                        raise Exception()
                    json_response = loads(await response.text())
                    if json_response['version'] != game_env.static.version:
                        game_env.dynamic.update_available = True
                        game_env.dynamic.update_url = json_response['url']
                        self.log('New game version {} detected'.format(json_response['version']))
        except:
            self.log('Failed to check for game update')
        await self.submit_result(game_env, only_sync=True)

    async def get_leaders(self):
        leaders = {}
        try:
            get_parameters = {'action': 'getTopScores', 'apiKey': self.__api_key}
            async with aiohttp.ClientSession() as session:
                async with session.get(self.__api_endpoint, params=get_parameters, timeout=aiohttp.ClientTimeout(total=15)) as response:
                    if response.status != 200:
                        raise Exception()
                    leaders = loads(await response.text())
        except:
            self.log('Failed to get game leaders from remote server')
        finally:
            return leaders
        
    async def submit_result(self, game_env, only_sync = False):
        payloads = []
        deserialized_object = self.__serialize_handler.deserialize()
        if deserialized_object:
            payloads = list(deserialized_object)

        if not only_sync:
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
        async with aiohttp.ClientSession() as session:
            put_tasks = [asyncio.ensure_future(self.__post_results(session, payload)) for payload in payloads]
            await asyncio.gather(*put_tasks, return_exceptions=False)

            for task, payload in zip(put_tasks, payloads):
                if task._result:
                    self.log('Successfully submitted result: score={}, name={}, level={}'.format(payload.get('score'), payload.get('name'), payload.get('level')))
                else:
                    payload.update({'apiKey':''})
                    unprocessed_payloads.append(payload)
                    self.log('Falied to submit result: score={}, name={}, level={}'.format(payload.get('score'), payload.get('name'), payload.get('level')))

        self.__serialize_handler.serialize(unprocessed_payloads)    
    
    async def __post_results(self, session, payload):
        result = True
        try:
            payload['apiKey'] = self.__api_key
            async with session.put(self.__api_endpoint, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status != 201:
                    result = False
        except:
            result = False
        finally:
            return result
