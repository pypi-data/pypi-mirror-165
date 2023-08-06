'''Generic observer/notifier super-class.'''

import asyncio
import logging
import os
import sys

VERBOSE_DEBUG = False


class Observer:
    '''Super class for an Observer class.

    The observer must use notifer.subscribe() and
    notifier.unsubscribe() messages to ensure that
    notify() messages will be received.'''

    def __init__(self):
        '''Initialise an Observer with a local queue.'''

        self.__notifier_queue: asyncio.Queue = asyncio.Queue()

        super().__init__()

    async def notify(self, notifier):
        '''Receive a notification of a new message from
        notifier instance.  Pull the data off the notifier's 
        queue and store in the local queue.'''

        message = await notifier.get()
        await self.__notifier_queue.put(message)


class Notifier:
    '''Super class for a Notifier class.

    The notifier receives subscribe() and unsubscribe()
    messages to register interested observers.

    The notifier sends a notify() to observers when 
    data exists and then receives a get() to pop the
    data from queue.'''

    def __init__(self):
        '''Initialise a Notifier with a local queue.'''

        self.__logger = logging.getLogger('ac-ws.notifier')

        self.__observers = []
        self.__observer_queue: asyncio.Queue = asyncio.Queue()

        super().__init__()

    async def get(self):
        '''Fetch an item from the queue.  Returns None if the queue is empty.'''

        try:
            response = self.__observer_queue.get_nowait()
        except asyncio.QueueEmpty:
            response = None

        if VERBOSE_DEBUG:
            self.__logger.debug(f'get(self) -> {response})')

        return response

    async def put(self, item):
        '''Put an item on the local queu and notify all observers.'''

        if VERBOSE_DEBUG:
            self.__logger.debug(f'put(self, {item})')

        await self.__observer_queue.put(item)
        for obs in self.__observers:
            await obs.notify(self)

    def subscribe(self, observer):
        '''Subscribe an observer object for state changes.
        Observer object must include an async notify(self, observable, *args, **kwargs) method.'''
        self.__observers.append(observer)

    def unsubscribe(self, observer):
        '''Unsubscribe an observer object.'''
        try:
            self.__observers.remove(observer)
        except ValueError:
            pass


class ObserverNotifier(Observer, Notifier):
    '''Super class that is both an Observer and Notifier.'''

    def __init__(self):
        super().__init__()
