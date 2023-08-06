'''Assetto Corsa entry_list.ini helper Class to re-order and re-write'''

import configparser
import json
from enum import Enum, auto
import random
import sys
from typing import Any, Dict, List


from ac_websocket_server.objects import EntryInfo
from ac_websocket_server.error import WebsocketsServerError


class EntryListIterationMethod(Enum):
    '''Iteration method to rewrite file in various manners.'''
    ORIGINAL = auto()
    FINISHING = auto()
    REVERSE = auto()
    RANDOM = auto()


class EntryList:
    '''A collection of individual Entry for the entry_list.ini file'''

    def __init__(self, file_name: str = None, entries: Dict[int, EntryInfo] = None) -> None:
        '''
        Create a new EntryList with optional input file and pre-populated entries.
        '''

        if entries:
            self.entries = entries
        else:
            self.entries = {}

        self.file_name = file_name

        if file_name and not entries:
            self.parse_entries_file()

        self.iteration_method = EntryListIterationMethod.FINISHING

        self._entries_sorting_key = {}

        self._entries_total_time = {}

        for entry in self.entries.keys():
            self._entries_sorting_key[entry] = sys.maxsize

        self.elements: List[Any]
        self.index: int

    def __iter__(self):
        '''
        Create an Iterator based on EntryListIterationMethod
        '''

        self.elements = list(self.entries)
        self.index = 0

        if self.iteration_method == EntryListIterationMethod.RANDOM:
            for entry in self.entries.keys():
                self._entries_sorting_key[entry] = random.randrange(100)

        if self.iteration_method == EntryListIterationMethod.ORIGINAL:
            self.elements.sort(key=lambda entry: entry)
        elif self.iteration_method == EntryListIterationMethod.REVERSE:
            self.elements.sort(
                key=lambda entry: self._entries_sorting_key[entry], reverse=True)
        else:
            self.elements.sort(
                key=lambda entry: self._entries_sorting_key[entry])

        return self

    def __next__(self):
        '''Return the next Entry'''

        if self.index < len(self.elements):
            self.index += 1
            return self.entries[self.elements[self.index - 1]]
        else:
            raise StopIteration

    def parse_entries_file(self):
        '''Parse the original entries file.'''

        if self.file_name:

            config = configparser.ConfigParser()
            config.read(self.file_name)

            for car_id in config.sections():

                car = config[car_id]

                self.entries[car_id] = \
                    EntryInfo(car_id=car_id,
                              model=car['MODEL'],
                              skin=car['SKIN'],
                              spectator_mode=car['SPECTATOR_MODE'],
                              drivername=car['DRIVERNAME'],
                              team=car['TEAM'],
                              guid=car['GUID'],
                              ballast=car['BALLAST'],
                              restrictor=car.get('RESTRICTOR', '')
                              )

    def parse_result_file(self, result_file):
        '''Parse AC race results file'''

        try:
            with open(result_file, 'r', encoding='UTF-8') as f:
                data = json.load(f)
        except OSError as error:
            print("Unable to read input file: " +
                  result_file + "(" + error + ")")
            raise OSError from error

        results = data["Result"]

        position = 1

        try:

            for result in results:

                car_id = 'CAR_' + str(result['CarId'])
                total_time = result['TotalTime']

                if total_time > 0:
                    self.entries[car_id].drivername = result['DriverName']
                    self.entries[car_id].guid = result['DriverGuid']
                    self._entries_sorting_key[car_id] = position
                    position += 1
                else:
                    self._entries_sorting_key[car_id] = sys.maxsize

        except KeyError as error:
            raise WebsocketsServerError(error) from error

    def __repr__(self):

        entries = ""

        position = 0
        for entry in iter(self):
            entry.position = position
            entries += str(entry)
            position += 1

        return entries

    def set_original_order(self):
        self.iteration_method = EntryListIterationMethod.ORIGINAL

    def set_standard_order(self):
        self.iteration_method = EntryListIterationMethod.FINISHING

    def set_random_order(self):
        self.iteration_method = EntryListIterationMethod.RANDOM

    def set_reversed_order(self):
        self.iteration_method = EntryListIterationMethod.REVERSE

    def show_cars(self) -> str:
        '''Returns a string representation of all cars'''

        original_iteration_method = self.iteration_method

        self.iteration_method = EntryListIterationMethod.ORIGINAL

        entries = ""

        car_number = 1
        for entry in iter(self):
            if car_number != 1:
                entries += ', '
            entries += 'CAR_' + str(car_number) + ": "
            entries += entry.model
            car_number += 1

        self.iteration_method = original_iteration_method

        return entries

    def show_grid(self) -> str:
        '''Returns a string representation of the grid'''

        entries = ""

        position = 1
        for entry in iter(self):
            if position != 1 and entry.drivername != '':
                entries += ', '
            if entry.drivername != '':
                entries += 'P' + str(position) + ": "
                entries += entry.drivername
                position += 1

        return entries

    def write(self, output_file):

        try:
            with open(output_file, 'w') as f:
                f.write(str(self))
                f.close()
        except OSError as err:
            print("Unable to write output file: " +
                  output_file + "(" + err + ")")
            raise OSError
