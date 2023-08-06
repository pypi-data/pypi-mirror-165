'''Assetto Corsa Websocket Server Class'''

import asyncio
import json
import logging
import os
import websockets

from .debug import monitor_tasks
from .constants import HOST, PORT
from .error import WebsocketsServerError
from .game import GameServer
from .handlers import handler
from .objects import EnhancedJSONEncoder

EXTRA_DEBUG = False


class WebsocketsServer:
    '''Represents an Assetto Corsa WebSocket Server.

    Allows control of an Assetto Corsa server with a websockets interface.'''

    def __init__(self,
                 server_directory: str = None,
                 host: str = HOST,
                 port: int = PORT
                 ) -> None:

        self.__logger = logging.getLogger('ac-ws.ws-server')

        if EXTRA_DEBUG:
            asyncio.get_event_loop().create_task(monitor_tasks())

        self.connected = set()

        self.host = host
        self.port = port

        if not server_directory:
            self.server_directory = os.getcwd()
        else:
            self.server_directory = server_directory

        self.game: GameServer = None

        self.send_queue = asyncio.Queue()

        self.stop_server: asyncio.Future = None

    async def consumer(self, message):
        # pylint: disable=logging-fstring-interpolation

        self.__logger.debug(f'Received message: {message}')

        if 'drivers list' in str(message):
            self.__logger.info('Received request to list game server drivers')
            if self.game:
                await self.send_queue.put(json.dumps(self.game.drivers, cls=EnhancedJSONEncoder))
            else:
                await self.send_queue.put('Game server not started - driver list not available')
            return
        if 'server info' in str(message):
            self.__logger.info('Received request to show game server info')
            if self.game:
                await self.send_queue.put(json.dumps(self.game, cls=EnhancedJSONEncoder))
            else:
                await self.send_queue.put('Game server not started - info not available')
            return
        if 'server restart' in str(message):
            self.__logger.info('Received request to restart game server')
            await self._stop_game()
            await self._start_game()
            return
        if 'server start' in str(message):
            self.__logger.info('Received request to start game server')
            await self._start_game()
            return
        if 'server stop' in str(message):
            self.__logger.info('Received request to stop game server')
            await self._stop_game()
            return
        if 'sessions list' in str(message):
            self.__logger.info('Received request to list game server sessions')
            if self.game:
                await self.send_queue.put(json.dumps(self.game.sessions, cls=EnhancedJSONEncoder))
            else:
                await self.send_queue.put('Game server not started - session list not available')
            return

        response_message = f'Received unrecognised message: {message}'
        await self.send_queue.put(response_message)

    async def handler(self, websocket):

        self.connected.add(websocket)

        await websocket.send(
            f'Welcome to the Assetto Corsa WebSocker server running at {self.host}:{self.port}')

        await handler(websocket, self.consumer, self.producer)

    async def notify(self, notifier):
        '''Receive a notification of a new message from notifier.
        Pull the data off the notifier queue and process.'''

        message = await notifier.get()
        await self.send_queue.put(message)

    async def producer(self):
        data = await self.send_queue.get()
        self.__logger.debug(f'Sending message: {data}')
        return data

    async def start(self):
        '''Start the websocket server'''

        try:

            self.__logger.info(f'Starting websocket server')

            self.stop_server = asyncio.Future()

            async with websockets.serve(self.handler, self.host, self.port):
                await self.stop_server

            self.__logger.info(f'Stopping websocket server')

        except KeyboardInterrupt:
            self.__logger.info(f'Interupting the server')

    async def _start_game(self):
        # pylint: disable=invalid-name

        if not self.game:
            try:
                self.game = GameServer(server_directory=self.server_directory)
                self.game.subscribe(self)
                await self.game.start()
                self.__logger.info('Game server started')
            except WebsocketsServerError as e:
                await self.send_queue.put(str(e))
        else:
            await self.send_queue.put('Command ignored - game server already started')

    async def stop(self):
        '''Stop the websocket server'''

        self.stop_server.set_result()

    async def _stop_game(self):
        # pylint: disable=invalid-name

        if self.game:
            try:
                await self.game.stop()
                self.game.unsubscribe(self)
                self.__logger.info('Game server stopped')
            except WebsocketsServerError as e:
                await self.send_queue.put(str(e))
        else:
            await self.send_queue.put('Command ignored - game server not already started')
