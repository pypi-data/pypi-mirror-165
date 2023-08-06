'''Assetto Corsa WebSockets Server Messages'''

from dataclasses import dataclass, is_dataclass, asdict
from enum import Enum
import json
from typing import Union


class EnhancedJSONEncoder(json.JSONEncoder):
    '''
    Enhanced JSON encoder.

    Use as per:
    json.dumps(foo, cls=EnhancedJSONEncoder)

    https://stackoverflow.com/questions/51286748/make-the-python-json-encoder-support-pythons-new-dataclasses
    https://stackoverflow.com/questions/24481852/serialising-an-enum-member-to-json
    '''

    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        if isinstance(o, Enum):
            return o.value
        return super().default(o)


@dataclass
class DriverInfo:
    '''Represents a driver.'''
    name: str = ''
    host: str = ''
    port: int = 0
    car: str = ''
    guid: str = ''
    ballast: int = 0
    msg: str = ''


@dataclass
class ServerInfo:
    '''Represents version information for a server.'''

    version: str = ''
    timestamp: str = ''
    track: str = ''
    cars: str = ''
    msg: str = ''


@dataclass
class SessionInfo:
    '''Represents an individual session in the AC game server'''

    type: str = ''
    laps: int = 0
    time: int = 0
    msg: str = ''


class MessageType(Enum):
    '''Allowable message types'''

    DRIVER_INFO = 'DriverInfo'
    SERVER_INFO = 'ServerInfo'
    SESSION_INFO = 'SessionInfo'


MessageBody = Union[DriverInfo, ServerInfo, SessionInfo]


@dataclass
class Message:
    '''Basic message structure'''
    type: MessageType
    body: MessageBody
