""" SMARTs Environment Reader and Environment Class """

import os
import yaml
import sys
import subprocess

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

        # See if the lmod command is supported
        if self.env['Description']['Modules']:
            self.lmod_supported = True
            self.lmod_cmd = self.env['Description']['LMOD_CMD']
        else:
            self.lmod_supported = False

        print("\nEnvironment file read successfully!\n")
        return 0;

    def list_modsets(self, name=None, *args, **kwargs):
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

    def _load_compiler(self, compiler, *args, **kwargs):
        # Internal function to load a compiler on a modset
        print("DEBUG: In Environment._load_compiler(...)")

        name    = compiler['name']
        version = compiler['version']
        cmds    = compiler['executables']

        # If LMOD Support enabled:
            # lmod_cmd = self.lmod_cmd

        print("DEBUG: Loading compiler: ", name, version)

        if 'module' in compiler.keys():
            print("This is a module!")
            compiler_module = compiler['module']
            if self.lmod_supported:
                # Infromation about how the `lmod python` command is translated into python
                load_compiler_lmod_cmd = str(self.lmod_cmd)+' python load '+compiler_module+'/'+version
                print("DEBUG: Load compiler command:\n > ", load_compiler_lmod_cmd)
                module_load = subprocess.Popen(load_compiler_lmod_cmd,
                                               shell=True, # TODO: Exploration around shell=True
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)
                # Information on what exec does
                exec (module_load.stdout.read())
            else:
                print("Lmod is not supported on this system, no lmod_cmd was given or modules=true"
                      " was not")
                return False

        elif 'path' in compiler.keys():
            print("This is a path!")
            os.environ['PATH'] = compiler['path']+'/bin/'+':'+os.environ['PATH']
        else:
            print("We don't know the method used to load this compiler!")
            sys.exit(-1)


        # Test the compiler to see if we have the right version loaded
        for cmd in cmds:
            check = subprocess.Popen(cmd+' --version', shell=True,
                                                       stdout=subprocess.PIPE,
                                                       stderr=subprocess.PIPE)
            stdout = str(check.stdout.read(), encoding='utf-8')
            stderr = str(check.stderr.read(), encoding='utf-8')

            if version not in stdout:
                print(version, " was not succesfully loaded for the command ", cmd)
                print("Instead got: ")
                print(stdout)
                print(stderr)
                return False

        print("Loaded compiler: ", name, "/", version, " succesfully!", sep='')

        return True

    def _load_library(self, library, *args, **kwargs):
        # Internal function to load a library based on the modset lib
        pass

    def load_modset(self, modset, *args, **kawrgs):
        print("DEBUG: In Environment.load_modset(...)")
    
        # Load a modset
        compiler = modset['compiler']


        print("DEBUG: Requested modset is: ", modset)
        print("DEBUG: Compiler is: ", compiler)
        print("DEBUG: Compiler name: ", compiler['name'])

        if not self._load_compiler(compiler):
            print("ERROR: There was an error loading the modset! ", modset)
            sys.exit(-1)

        # for library in modset['libraries']:
        #   if not _load_library(library):
        #       print("ERROR: There was an error loading this library! ", library)
        #       sys.exit(-1)


        return True
