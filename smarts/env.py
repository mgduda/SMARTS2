""" SMARTs Environment Reader and Environment Class """

import os
import yaml
import sys
import subprocess

class Environment:
    """ Class Environment - Class for reading and then loading the modsets
    within an Environment.yaml file """

    def __init__(self, envFile, *args, **kwargs):
        """ Initalize an Environment class with a envFile - Does no checking or
        parsing. """
        self.envFile = envFile
        self.env = None
        return

    def parse_file(self, *args, **kwargs):
        """ Load an environment.yaml file. After loaded via yaml.safe_load, the
        loaded enviornment will be parsed to ensure basic parts of the environment.yaml
        file.

        On error, this method will return -1 and will return 0 on success """
        if not os.path.isfile(self.envFile):
            print("ERROR: '", self.envFile, "' does not exist!")
            print("ERROR: Please specify a valid yaml file!")
            return -1

        try:
            self.env = yaml.safe_load(open(self.envFile))
        except yaml.scanner.ScannerError as error:
            print("ERROR: Could not read", self.envFile, "!")
            print(error)
            print("\n")
            return -1

        # Do some interal error checking here ... are all the main parts there?
        if 'Description' not in self.env: # Description section check
            print("ERROR: The environment.yaml file contained no 'Description' section")
            print("ERROR: Please add a 'Description' section to: '", self.envFile,"'", sep="")
            return -1
        else: # Check for individual Description Components
            description = self.env['Description']
            if 'Name' not in description:
                print("ERROR: The environment.yaml 'Description' section contained no 'Name' attribute.")
                print("ERROR: Please add a 'Name:' attribute to the 'Description' section in the")
                print("ERROR: environment file: ", self.envFile)
                return -1

            if 'Max Cores' not in description:
                print("ERROR: The environment.yaml 'Description' section contained no 'Max Cores' attribute")
                print("ERROR: to specify the max number of cores to use on this machine.")
                print("ERROR: Please add a 'Max Cores:' attribute to the 'Description' section in'")
                print("ERROR: environment file: ", self.envFile)
                return -1
            else:
                if description['Max Cores'] == 0:
                    print("ERROR:'Max Cores' in the 'Description' section of the env.yaml file")
                    print("ERROR: was set to zero. Please set to a value >= 1")
                    return -1

            if 'Modules' in description:
                if description['Modules'] == True and 'LMOD_CMD' not in description:
                    print("ERROR: In the 'Description' section of the env.yaml file, the 'Modules:' attribute")
                    print("ERROR: was set to True, but a 'LMOD_CMD' attribute was not given. Please add")
                    print("ERROR: a 'LMOD_CMD' attribute to the description section of: '", self.envFile, "'", sep="")
                    return -1

        # LMOD Checks - Turn LMOD support on or off
        if 'Modules' in self.env['Description']:
            if self.env['Description']['Modules'] == True:
                self.lmod_cmd = self.env['Description']['LMOD_CMD']
                self.lmod_supported = True
            else: # Modules == False
                self.lmod_supported = False
        elif 'LMOD_CMD' in self.env['Description'] and 'Modules' not in self.env['Description']:
            print("WARNING: No 'Modules' attribute in the 'Description' section of the env.yaml file was ")
            print("WARNING: found, but a LMOD_CMD was specified. SMARTS will not use LMOD")
            print("WARNING: for this SMARTS run.")
            self.lmod_supported = False
        else: # No Modules attribute in env.yaml file - Turn off lmod support
            self.lmod_supported = False

        if 'Modsets' not in self.env: # Modset section checks
            print("ERROR: The environment.yaml file contained no 'Modests' section")
            print("ERROR: Please add a 'Modsets' section to: '", self.envFile,"'", sep="")
            return -1
        elif self.env['Modsets'] == None:
            print("ERROR: No Modsets were given!")
            print("ERROR: Please specify at least one modset under the 'Modsets' section")
            return -1
        else: # Check each modset for basic errors:
            for modsets in list(self.env['Modsets'].keys()):
                modset = self.env['Modsets'][modsets]

                # Compiler section check
                if 'Compiler' in modset:
                    compiler = modset['Compiler']
                    if 'Name' not in compiler:
                        print("ERROR: 'Name' was not found in the 'Compiler' section for Modset")
                        print("ERROR: '", modsets, "'", sep='')
                        return -1
                    if 'Version' not in compiler:
                        print("ERROR: 'Version' was not found in the 'Compiler' section for Modset")
                        print("ERROR: '", modsets, "'", sep='')
                        return -1
                    if 'Path' not in compiler and 'Module' not in compiler:
                        print("ERROR: No method for specifying the compiler for modset: '", modsets, "'", sep="")
                        print("ERROR: In the env.yaml file: ", self.envFile)
                        print("ERROR: Please either use 'Path:' or 'Module' to specify a compiler")
                        return -1
                    if 'Module' in compiler and self.lmod_supported == False:
                        print("ERROR: The 'Compiler' for the modset '", modsets, "' was specified with", sep="")
                        print("ERROR: 'Module', but 'Modules' in the 'Description' section of '", self.envFile, "'", sep="")
                        print("ERROR: is set to False.")
                        return -1
                    if 'Executables' not in compiler:
                        print("ERROR: 'Executables' not found in compiler for modset: '", modsets, "'", sep="")
                        return -1
                else:
                    print("ERROR: No 'Compiler' section found for the modset: '", modsets, "'", sep="")
                    print("ERROR: Please add one to continue")
                    return -1

                # MPI section check
                if 'MPI' in modset:
                    mpi = modset['MPI']
                    if 'Path' not in mpi and 'Module' not in mpi:
                        print("ERROR: In the MPI specification, no 'path' or 'module' was given")
                        print("ERROR: Please add either a 'path' or a 'module' attribute to specify")
                        print("ERROR: an MPI installation in the modset:", modsets)
                        return -1
                    if 'Module' in mpi and self.lmod_supported == False:
                        print("ERROR: The mpi specification for the modset'", modsets, "' was specified with", sep="")
                        print("ERROR: 'module', but 'Modules' in the 'Description' section of '", self.envFile, "'", sep="")
                        print("ERROR: is set to False or LMOD support for this enviornment is not supported")
                        print("ERROR: because of an error. Please speicfy the compiler location as a")
                        print("ERROR: 'path' or fix the above warnings")
                        return -1
                    if 'Executables' not in mpi:
                        print("ERROR: 'Executables' was not found in the MPI section for the modset:")
                        print("ERROR: '", modsets, "'", sep='')
                        return -1
                # Library section check
                if 'Libs' in modset:
                    libs = modset['Libs']
                    for lib in libs:
                        libName = list(lib.keys())[0]
                        if ('Name' in lib and 'Value' not in lib):
                            print("ERROR: The attribute 'Name' was given, but no 'Value' was")
                            print("ERROR: given to assign it a value for the library: '", libName, "'.", sep="")
                            print("ERROR: Please specify a Value to associate with Name:")
                            print("ERROR: ```")
                            print("ERROR: Name:")
                            print("ERROR: Value:")
                            print("ERROR: ```")
                            return -1
                        if ('Name' not in lib and 'Value' in lib):
                            print("ERROR: The attribute 'Value' was given, but 'Name' was not given ")
                            print("ERROR: for the library: '", libName, "'. Please specify Name to assign", sep="")
                            print("ERROR: a Value to it.")
                            print("ERROR: ```")
                            print("ERROR: Name: ENV_NAME")
                            print("ERROR: Value: value")
                            print("ERROR: ```")
                            return -1
                        if 'Name' not in lib and 'Value' not in lib and 'Module' not in lib:
                            print("ERROR: No method for specifying the library: '", libName, "'", sep="")
                            print("ERROR: Please specify a way to load the library with either a")
                            print("ERROR: 'Name', 'Value' pair or with 'Module' and 'Version'")
                            return -1
                        if 'Module' in lib and self.lmod_supported == False:
                            print("ERROR: The library specification for the modset'", modsets, "' was specified with", sep="")
                            print("ERROR: 'Module', but 'Modules' in the 'Description' section of '", self.envFile, "'", sep="")
                            print("ERROR: is set to False or LMOD support for this enviornment is not supported.")
                            return -1
                else:
                    print("ERROR: 'Libs' section was not found in the modset: '", modsets,"'", sep='')
                    return -1

        if self.env['Description']['HPC'] != None:
            self.hpc = self.env['Description']['HPC']
        else:
            self.hpc = None

        self.name = self.env['Description']['Name']
        self.ncpus = self.env['Description']['Max Cores']


        return 0;

    def list_modsets(self, name=None, *args, **kwargs):
        """ Return a list of modsets found in the parsed environment.yaml file,
        if name is specified then modset names that contain that name will be returned.

        Keyword arguments:
        name -- Name to specify specific modset(s) name (String)
        """
        modsets = self.env['Modsets']

        modsetNames = []
        for modset in list(modsets.keys()):
            if name:
                if name in modset:
                    modsetNames.append(modset)
            else:
                modsetNames.append(modset)

        return modsetNames

    def list_modset(self, modset, *args, **kwargs):
        """ Return a dictionary of the modset, modset, from the environment.yaml
        file.

        modset - Name of modset to retrieve (String)
        """
        pass

    def list_libraries(self, modset, *args, **kwargs):
        """ Return a list of libraries in the modset, modset from the environment.yaml
        file.

        modset - Name of modset to retrieve its libraries (string)
        """
        pass

    def _lmod_load(self, module, version=None):
        """ Internal function to interface with LMOD to load the module, module via
        `module load`. If version is specified, that version will try to be loaded.

        module - Name of module to be loaded with `module load` (string)
        version (optional) - Version number of module to be loaded (string)
        """

        if version == None:
            version = ""

        lmod_load_cmd = str(self.lmod_cmd) + ' python load '
        module_str = str(module) + '/' + str(version)
        lmod_load_cmd += module_str

        print("DEBUG: Going to run the following lmod command: ", lmod_load_cmd)
        module_load = subprocess.Popen(lmod_load_cmd,
                                       shell=True, # TODO: Exploration around shell=True
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)

        module_load_stdout = module_load.stdout.read().decode()
        module_load_stderr = module_load.stderr.read().decode()

        module_load.wait()
        if module_load.returncode != 0:
            print("ERROR: Problems calling `lmod load ", module_str, "' see lmod error below:",
                sep='')
            print(module_load_stdout)
            print(module_load_stderr)
            return False

        # TODO: Information on what exec does
        exec (module_load_stdout)

        # TODO: Explore what happens when errors in this function 
        return True


    def _load_compiler(self, compiler, *args, **kwargs):
        """ Load a compiler by altering this process PATH environment. This module
        checks to see if the compiler was loaded successful by running `--version` and
        checking the version number of the compiler

        compiler - Env.yaml description of a compiler (dict)
        """

        name    = compiler['Name']
        version = compiler['Version']
        cmds    = compiler['Executables']

        if 'Module' in compiler.keys():
            compiler_module = compiler['Module']
            if self.lmod_supported:
                # Load the compiler using LMOD
                if not self._lmod_load(compiler_module, version):
                    # TODO: Percolate these back up to the API
                    print("ERROR: Could not load the compiler: ", name, version)
                    print("ERROR: using lmod. Is it specified correctly?")
                    return False
            else:
                # TODO: Percolate these back up to the API
                # TODO: We should also check for this type of inconsistency when we first load the
                # lmod file, to catch errors as soon as possible. So this ugly if statement should
                # go away! (YAY!)
                print("ERROR: Lmod is not supported on this system, no lmod_cmd was given or")
                print("ERROR: modules=true was not set to true. ")
                print("ERROR: Please see the environment.yaml specification for using lmod")
                return False
        elif 'Path' in compiler.keys(): # Load the compiler via its PATH specification
            os.environ['PATH'] = compiler['Path']+'/bin/'+':'+os.environ['PATH']
        else: 
            print("ERROR: We don't know the method used to load this compiler!")
            sys.exit(-1)

        # Test the compiler to see if we have the right version loaded
        for cmd in cmds:
            check = subprocess.Popen(cmd+' --version', shell=True,
                                                       stdout=subprocess.PIPE,
                                                       stderr=subprocess.PIPE)
            stdout = str(check.stdout.read(), encoding='utf-8')
            stderr = str(check.stderr.read(), encoding='utf-8')

            if str(version) not in stdout:
                print(version, " was not succesfully loaded for the command ", cmd)
                print("Instead got: ")
                print(stdout)
                print(stderr)
                return False

        # print("DEBUG: Succesfully Loaded compiler: ", name, "/", version, " succesfully!", sep='')

        return True

    def _load_mpi(self, modset, *args, **kwargs):
        """ Load an MPI implementation by prepending it to PATH - This function is similar to
        Environment._load_compiler """
        mpi = modset['MPI']
        cmds = modset['MPI']['Executables'] # TODO: This should be checked - In yaml load ??

        # Load the MPI implementation depending on if its a module or a path specification
        if 'Module' in mpi.keys():
            mpi_module = mpi['Module']
    
            # Version not necessary with LMOD commands
            if 'Version' in mpi: 
                mpi_version = mpi['Version']
            else:
                mpi_version = None

            if not self._lmod_load(mpi_module, mpi_version):
                # TODO: Percolate these back up to the API
                print("ERROR: Could not load the mpi implementation: ", mpi_name, mpi_version)
                print("ERROR: using lmod. Is it specified correctly?")
                return False
        elif 'Path' in mpi.keys():
            os.environ['PATH'] = mpi['Path']+'/bin/'+':'+os.environ['PATH']

        # See if the MPI_PATH/bin exists
        #  - Then try and run the mpi executables
        #  - Possible see if mpicc --version prints out the correct associated compiler ???

        for cmd in cmds:
            # Some MPI exeuctables print out the version for the copmiler they are linked with, so
            # just make sure that they are able to run (for now)
            # TODO: This will also fail if the fork can't find the executable
            check = subprocess.Popen(cmd,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            stdout = str(check.stdout.read(), encoding='utf-8')
            stderr = str(check.stderr.read(), encoding='utf-8')

            CMD_NOT_FND = 127

            if check.returncode == CMD_NOT_FND:
                print("ERROR: Could not load this MPI Implementation!")
                print("ERROR: error was:", stdout)
                print("ERROR: ", stderr)
                return False

        return True
        

    def _load_library(self, library, *args, **kwargs):
        """ Internal function to load a library of a modset - This function with either load the
        library by running `lmod load` (_lmod_load) or will create an environment variable and
        assign it a value if that is how the library is specified.
        """

        # The library is specified as a lmod module
        if 'Module' in library.keys():
            module = library['Module']

            if 'Version' in library.keys():
                version = library['Version']
            else:
                version = ""

            if not self._lmod_load(module, version):
                print("ERROR: Could not load the library: ", library['Module'], version)
                print("ERROR: Is it specified correctly?")
                return False
        # The library is specified as a environment variable
        elif 'Name' in library.keys():
            if 'Value' in library.keys():
                env_name = library['Name']
                value = library['Value']

                print("SMARTS: Setting the env variable:", env_name, "to value:", value)
                os.environ[env_name] = value
                print("SMARTS: Environment variable is: ", os.environ[env_name])
            else:
                print("ERROR: For the library", library['Name'], "does not have a maching value name")
                return False

        return True

    def load_modset(self, modsetName, *args, **kawrgs):
        """ Completely load the modset, modsetName to be used by a single test. This function
        completely loads a modset (compiler, mpi implementation, and all libraries).

        To load a compiler, this function will alter the PATH environment variable for the current
        process (single test) and prepend the compiler path to it. If the compiler is specified as
        a module, it will be loaded via the lmod Python interface (`module python load ...`)

        MPI implementation will be loaded in a similar manner to compilers.

        Both MPI and Compilers will be checked to ensure that the correct version is installed by
        running the compiler executables specified in the executables section of the compiler or
        MPI env.yaml sections with `--version` and checking the versions in the env.yaml file match
        correctly.

        Libraries will be loaded by creating ENV_NAME as an environment variable and assigning to
        it the value specified in value.

        modsetName -- Name of the modset to be loaded (String)
        """

        # Load a modset
        modset = self.env['Modsets'][modsetName]
        compiler = modset['Compiler']

        # print("DEBUG: Requested modset is: ", modset)
        # print("DEBUG: Compiler is: ", compiler)
        # print("DEBUG: Compiler name: ", compiler['name'])

        if not self._load_compiler(compiler):
            return False

        if "MPI" in modset.keys():
            if not self._load_mpi(modset):
                return False

        for library in modset['Libs']:
            if not self._load_library(library):
                return False

        print("SMARTS: Loaded modset: '", modsetName, "' succsfully!", sep='')

        return True
