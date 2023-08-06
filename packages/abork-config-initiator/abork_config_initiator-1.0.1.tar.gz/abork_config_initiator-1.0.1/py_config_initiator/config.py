import os.path as p
from typing import List


class ParametersError(Exception):
    pass


class EmptyConfigsError(Exception):
    pass


class ConfigInitor:

    def __init__(self, path:str, filename:str='config.ini'):

        self.filename = filename
        self.path = path

    def set_template(self, string:str=None, list:List[str]=None):

        if not string and not list:
            raise ParametersError('Supply a template either as string or as list')

        if string and list:
            raise ParametersError('Supply only one template')

        if ( string and not isinstance(string, str) ) or ( list and not isinstance(list, List) ):
            raise ParametersError('Wrong type for parameter used.')
    
        self.value_check = []
        
        if list:
            string = ''
            for row in list:
                string += row + '\n'

        self.template = string
        return self

    def check(self):

        if not self.path or not p.exists(self.path):
            raise ValueError('Supplied path does not exist.')

        fullpath = p.join(self.path, self.filename)

        if not p.exists(fullpath):
            self.__create_file(fullpath)

        self.__check_file(fullpath)

    def __create_file(self, fullpath:str):

        with open(fullpath, mode='w') as file:
            file.write(self.template)

    def __check_file(self, fullpath:str):
        
        with open(fullpath, mode='r') as file:
            lines = file.readlines()
        
        empty_configs = []

        for line in lines:
            if line.find('=') > 0 and line.split('=')[1].isspace():
                empty_configs.append(line.split('=')[0])

        if empty_configs:
            raise EmptyConfigsError('Empty configs: ' + str(empty_configs))