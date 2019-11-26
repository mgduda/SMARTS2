""" SMARTs Environment Reader and Environment Class """

import os
import yaml

class Environment:
    def __init__(self, envFile, *args, **kwargs):
        self.envFile = envFile
        self.env = None
        return

    """
    TODO: Do checking of the env.yaml file:
        
    Check for both: 
        - Description - Produces error
        - Modests - Produce Warnings

    Description Checks:
        - Check for max_cores
        - If modules = True then LMOD_CMD must be set
        - If HPC = PBS then check there isn't slurm_options and visa versa
        - If HPC = False and HPC_OPTIONS is present produce warning
        - 
    Modests:
        - If a module command is listed, then check to see if the LMOD_CMD
          is present in the description
        - Libraries (if present) - Check to see if they are either modules (w/ optional version) or
          either a ENV_NAME AND value pair.
    """

    def parse_file(self, *args, **kwargs):
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

        # Do some interal error checking here ... are all the main parts there?

        if self.env['Description']['HPC'] != None:
            self.hpc = self.env['Description']['HPC']
        else:
            self.hpc = None

        self.name = self.env['Description']['Name']
        self.ncpus = self.env['Description']['Max Cores']

        print("\nEnvironment file read successfully!\n")
        return 0;

    def list_modests(self, name=None, *args, **kwargs):
        # If name is None, list out all modests found in the environment.yaml file,
        # else, list out the modests that contain name.
        # Returns a list
        return self.env['Modsets']

    def list_modset(self, modset, *args, **kwargs):
        # List the information of a single modest
        # This should probably return the yaml dictiony of said modset
        pass

    def list_libraries(self, modset, *args, **kwargs):
        # List the libraries of a specifiec modset
        # Returns a list
        pass

    def _load_compiler(self, compiler, executables, *args, **kwargs):
        # Internal function to load a compiler on a modset
        pass

    def _load_library(self, library, *args, **kwargs):
        # Internal function to load a library based on the modset lib
        pass

    def load_modest(self, modset, *args, **kawrgs):
        # Load a modset
        pass

