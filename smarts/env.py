""" SMARTs Environment Reader and Environment Class """

import os
import yaml

class Environment:
    def __init__(self, envFile, *args, **kwargs):
        self.envFile = envFile
        self.env = None
        return

    def parse_file(self):
        if not os.path.isfile(self.envFile):
            print("ERROR: '", self.envFile, "' does not exist!")
            print("ERROR: Please specify a valid yaml file!")
            return -1

        try:
            self.env = yaml.safe_load(open(self.envFile))
        except yaml.scanner.ScannerError as error:
            print("ERROR: Could not read", self.envFile, "!")
            print("ERROR: Most likely a syntax error:\n")
            print(error)
            print("\n")
            return -1

        print("Environment file read successfully!\n\n")
        return 0;

    def list_modests(self):
        # List all the modests that are in the env specification
        pass
