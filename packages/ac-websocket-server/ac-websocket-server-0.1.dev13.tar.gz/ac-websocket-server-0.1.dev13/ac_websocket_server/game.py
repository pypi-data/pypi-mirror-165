'''Assetto Corsa Game Server Class'''

import asyncio
import configparser
from dataclasses import dataclass, field
from datetime import datetime
import glob
import hashlib
import json
import logging
import os
import sys
from typing import Dict
from ac_websocket_server.entries import EntryList

from ac_websocket_server.error import WebsocketsServerError
from ac_websocket_server.objects import DriverInfo, EntryInfo, ServerInfo, SessionInfo
from ac_websocket_server.watcher import Watcher


@dataclass
class GameServer:
    '''Represents an Assetto Corsa Server.'''
    # pylint: disable=logging-fstring-interpolation, invalid-name

    server_directory: str

    version: str = field(init=False)
    timestamp: str = field(init=False)
    name: str = field(init=False)
    track: str = field(init=False)
    cars: str = field(init=False)
    http_port: int = field(init=False)
    tcp_port: int = field(init=False)
    udp_port: int = field(init=False)
    drivers: Dict[str, DriverInfo] = field(init=False)
    entries: Dict[int, EntryInfo] = field(init=False)
    sessions: Dict[str, SessionInfo] = field(init=False)

    def __post_init__(self):

        self.__logger = logging.getLogger('ac-ws.game')

        self.drivers = {}
        self.entries = {}
        self.sessions = {}

        self.__queue: asyncio.Queue = asyncio.Queue()

        if os.path.exists(f'{self.server_directory}/acServer.py'):
            self.__cwd = None
            self.__exe = f'{self.server_directory}/acServer.py'
            self.__hash = None
        else:
            self.__cwd = self.server_directory
            if sys.platform == 'linux':
                self.__exe = f'{self.server_directory}/acServer'
                self.__hash = 'f781ddfe02e68adfa170b28d0eccbbdc'
            else:
                self.__exe = f'{self.server_directory}/acServer.exe'
                self.__hash = '357e1f1fd8451eac2d567e154f5ee537'

        server_cfg_file_name = f'{self.server_directory}/cfg/server_cfg.ini'

        if os.path.exists(server_cfg_file_name):

            cfg = configparser.ConfigParser()
            try:
                cfg.read(
                    f'{self.server_directory}/cfg/server_cfg.ini')

                self.name = cfg['SERVER']['NAME']
                self.http_port = cfg['SERVER']['HTTP_PORT']
                self.tcp_port = cfg['SERVER']['TCP_PORT']
                self.udp_port = cfg['SERVER']['UDP_PORT']

                for session in ['PRACTICE', 'QUALIFY', 'RACE']:
                    if cfg.has_section(session):
                        name = cfg[session].get('NAME')
                        time = cfg[session].get('TIME', 0)
                        laps = cfg[session].get('LAPS', 0)
                        self.sessions[name] = SessionInfo(
                            name, laps=laps, time=time)

            except configparser.Error as e:
                raise WebsocketsServerError(e) from e

        else:
            self.__logger.error(
                f'Missing server_cfg.ini file in {self.server_directory}')

        entry_list_file_name = f'{self.server_directory}/cfg/entry_list.ini'

        if os.path.exists(entry_list_file_name):

            self.entry_list = EntryList(entry_list_file_name)

            self.entries = self.entry_list.entries

        else:
            self.__logger.error(
                f'Missing entry_list.ini file in {self.server_directory}')

        self.__logfile_stdout: str
        self.__logfile_stderr: str

        self.__watcher_stdout: Watcher

        self.__observers = []

        self.__process: asyncio.subprocess.Process

    async def get(self):
        '''Fetch an item from the queue.  Returns None if the queue is empty.'''

        try:
            response = self.__queue.get_nowait()
        except asyncio.QueueEmpty:
            response = None

        return response

    async def notify(self, notifier):
        '''Receive a notification of a new message from log watcher.'''

        message = await notifier.get()

        try:
            item = json.loads(message)

            if item['type'] == 'ServerInfo':
                self.version = item['body']['version']
                self.timestamp = item['body']['timestamp']
                self.track = item['body']['track']
                self.cars = item['body']['cars']

            if item['type'] == 'DriverInfo' and item['body']['msg'] == 'joining':

                body = item['body']
                name = body['name']

                driver_info = DriverInfo()

                driver_info.name = name
                driver_info.host = body['host']
                driver_info.port = body['port']
                driver_info.car = body['car']
                driver_info.guid = body['guid']
                driver_info.ballast = body['ballast']
                driver_info.msg = body['msg']

                self.drivers[driver_info.name] = driver_info

                self.__logger.debug(f'Driver {name} joining')

            if item['type'] == 'DriverInfo' and item['body']['msg'] == 'leaving':
                body = item['body']
                name = body['name']
                del self.drivers[name]
                self.__logger.debug(f'Driver {name} leaving')

            if item['type'] == 'SessionInfo':

                body = item['body']
                session_type = body['type']

                session_info = SessionInfo()

                session_info.type = session_type
                session_info.laps = body['laps']
                session_info.time = body['time']

                self.sessions[session_type] = session_info

        except json.JSONDecodeError:
            pass

        await self.put(message)

    async def put(self, item):
        '''Put an item on the queu and notify all observers.'''

        await self.__queue.put(item)
        for obs in self.__observers:
            await obs.notify(self)

    async def start(self):
        '''Start the game server.'''

        if self.__hash:
            try:
                with open(self.__exe, 'rb') as file_to_check:
                    data = file_to_check.read()
                    if self.__hash != hashlib.md5(data).hexdigest():
                        raise WebsocketsServerError(
                            f'{self.__exe} checksum mismatch')
            except FileNotFoundError as e:
                raise WebsocketsServerError(
                    f'{self.__exe} missing') from e

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.__logger.info('Starting game server')

        os.makedirs(f'{self.server_directory}/logs/session', exist_ok=True)
        os.makedirs(f'{self.server_directory}/logs/error', exist_ok=True)

        self.__logfile_stdout = f'{self.server_directory}/logs/session/output{timestamp}.log'
        self.__logfile_stderr = f'{self.server_directory}/logs/error/error{timestamp}.log'

        session_file = open(self.__logfile_stdout, 'w', encoding='utf-8')
        error_file = open(self.__logfile_stderr, 'w', encoding='utf-8')

        try:
            self.__process = await asyncio.create_subprocess_exec(
                self.__exe, cwd=self.__cwd, stdout=session_file, stderr=error_file)

            self.__logger.info(f'Process pid is: {self.__process.pid}')
            await self.put('Assetto Corsa server started')
            # await self.put(str(self))
            self.__watcher_stdout = Watcher(self.__logfile_stdout)
            self.__watcher_stdout.subscribe(self)
            await self.__watcher_stdout.start()
        except PermissionError as e:
            self.__logger.error(f'Process did not start: {e}')
            await self.put('Assetto Corsa server did not start')
            raise WebsocketsServerError(e) from e

    async def stop(self):
        '''Stop the game server'''

        self.__logger.info('Stopping game server')
        await self.put('Assetto Corsa server is stopping')

        self.__process.terminate()

        status_code = await asyncio.wait_for(self.__process.wait(), None)
        self.__logger.info(f'Game server exited with {status_code}')

        await self.__watcher_stdout.stop()
        self.__watcher_stdout.unsubscribe(self)

    def subscribe(self, observer):
        '''Subscribe an observer object for state changes.
        Observer object must include an async notify(self, observable, *args, **kwargs) method.'''
        self.__observers.append(observer)

    def unsubscribe(self, observer):
        '''Unsubscribe an observer object.'''
        try:
            self.__observers.remove(observer)
        except ValueError as error:
            self.__logger.debug(
                "Unsubscribe failed with value error: %s for %s", error, observer)

    async def update_grid(self, reverse: bool = False):

        try:
            result_files = glob.glob(
                os.path.join(f'{self.server_directory}/results', "*RACE.json"))
            result_file = max(result_files, key=os.path.getctime)

            await self.put(f'Updating entries using {result_file}')

            self.entry_list.parse_result_file(result_file)

            if reverse:
                self.entry_list.set_reversed_order()
            else:
                self.entry_list.set_standard_order()

            await self.put('Grid updated to ' + str(self.entry_list.show_grid()))

            self.entry_list.write(
                f'{self.server_directory}/cfg/entry_list.ini')

            await self.put('Assetto Corsa server entry_list.ini updated')
        except WebsocketsServerError as error:
            await self.put(f'Error parsing results file: {error}')
