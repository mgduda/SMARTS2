
import os
import sys
from pathlib import Path
from enum import Enum
from dataclasses import dataclass

import argparse

from smarts.env import Environment
import configparser as ConfigParser

SMARTS_CONFIG_FNAME = '.smartscf'

@dataclass
class ConfigData:
    environment_file : str
    environment : Environment
    test_directory : str
    source_directory : str
    verbose : int

class Config:
    def __init__(self, configData=None):
        if configData is not None:
            self._data = configData
        else:
            self._data = ConfigData(environment_file=None,
                                    environment=None,
                                    test_directory=None,
                                    source_directory=None,
                                    verbose=0)

    @property
    def env(self) -> Environment:
        return self._data.environment

    @env.setter
    def env(self, value : Environment):
        print("Setting enviornment file")
        self._data.environment = value

    @property
    def env_file(self) -> str:
        return self._data.environment_file

    @env_file.setter
    def env_file(self, value : str):
        self._data.environment_file = value

    @property
    def test_dir(self) -> str:
        return self._data.test_directory

    @test_dir.setter
    def test_dir(self, value : str):
        self._data.test_directory = value

    @property
    def source_dir(self) -> str:
        return self._data.source_directory

    @source_dir.setter
    def source_dir(self, value : str):
        self._data.source_directory = value

    @property
    def verbose(self) -> int:
        return self._data.verbose

    @verbose.setter
    def verbose(self, value : int):
        self._data.verbose = value

class CommandLineConfig(Config):
    def __init__(self, parser):
        super().__init__()
        self.parser = parser
        self.setup_argparse()

    def setup_argparse(self):
        print("Setting up optional argparse")
        optional = self.parser.add_argument_group('Optional arguments')

        optional.add_argument('-e', '--env-file',
                            dest='env',
                            help='The location of the env.yaml file',
                            metavar='env.yaml',
                            default=None)
        optional.add_argument('-s', '--src-dir',
                            dest='src',
                            help='The directory that holds the code to test changes (MPAS-Model)',
                            metavar='dir',
                            default=None)
        optional.add_argument('-t', '--test-dir',
                            dest='dir',
                            help='The location of the test directory',
                            metavar='dir',
                            default=None)

        optional.add_argument('-v', '--verbose',
                            dest='verbose',
                            help="Output debug level",
                            type=int,
                            metavar='level',
                            default=0)
                        
    def parse_config_arguments(self, args):
        self.env_file = args.env
        self.test_dir = args.dir
        self.source_dir = args.src

class SmartscfType(Enum):
    USER = Path.home()
    CWD = Path(os.getcwd())

class SmartsCFConfig(Config):
    def __init__(self, config_type : SmartscfType):
        super().__init__()
        self.smartsCfType=config_type
        self.configParser = ConfigParser.ConfigParser()
        if self.is_config_present():
            self.parse_config()
        else:
            print("Config is not present")

    @property
    def config_location(self) -> str:
        return os.path.join(self.smartsCfType.value, SMARTS_CONFIG_FNAME)

    def is_config_present(self) -> bool:
        return os.path.isfile(self.config_location)

    def parse_config(self):
        self.configParser.read(self.config_location)

        if 'smarts' not in self.configParser.sections():
            raise(ValueError(f"'[smarts]' section was not found in the config file {self.config_location}. "\
                              "See the README for '.smartscf' exmaple"))

        smarts_section = self.configParser['smarts']

        if 'environment' in smarts_section:
            self.env_file = os.path.expanduser(smarts_section['environment'])

        if 'tests_dir' in smarts_section:
            self.test_dir = os.path.expanduser(smarts_section['tests_dir'])

        if 'source_dir' in smarts_section:
            self.source_dir = os.path.expanduser(smarts_section['source_dir'])
        
        if 'verbose' in smarts_section:
            self.verbose = os.path.expanduser(smarts_section['verbose'])


class SmartsConfig:
    def __init__(self, parser):
        self.cl_config = CommandLineConfig(parser)
        self.user_config = SmartsCFConfig(SmartscfType.USER)
        self.cwd_config = SmartsCFConfig(SmartscfType.CWD)

    @property
    def test_dir(self):
        if self.cl_config.test_dir is not None:
            return self.cl_config.test_dir

        if self.cwd_config.test_dir is not None:
            return self.cwd_config.test_dir

        if self.user_config.test_dir is not None:
            return self.user_config.test_dir

        raise ValueError(f'No test directory file was found in any configuration')

    @property
    def src_dir(self):
        if self.cl_config.source_dir is not None:
            return self.cl_config.source_dir

        if self.cwd_config.source_dir is not None:
            return self.cwd_config.source_dir

        if self.user_config.source_dir is not None:
            return self.user_config.source_dir

        raise ValueError(f'No source directory file was found in any configuration')


    @property
    def env_file(self):
        if self.cl_config.source_dir is not None:
            return self.cl_config.env_file

        if self.cwd_config.source_dir is not None:
            return self.cwd_config.env_file

        if self.user_config.source_dir is not None:
            return self.user_config.env_file

        raise ValueError(f'No enviornment file was found in any configuration')
    
