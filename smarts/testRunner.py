""" SMARTs Test Runner - With Test Manager and Test Scheduler """
import os
import string
import sys
from multiprocessing import Process
from importlib import import_module
import datetime

NOT_IMPLEMENTED_ERROR = "IS NOT YET IMPLEMENTED"

# from smarts import HPC
# import environment

class TestSubProcess(Process):
    """ Wrapper around tests which will enable them to be launched as subprocsses """
    def __init__(self, test_launch_name, test,
                                         env,
                                         srcDir,
                                         testDir,
                                         hpc,
                                         *args, **kwargs):
        Process.__init__(self)
        self.test = test
        self.test_launch_name = test_launch_name
        self.srcDir = os.path.abspath(srcDir)
        self.testDir = os.path.abspath(testDir)
        self.env = env
        self.hpc = hpc
        self.args = args
        self.kwargs = kwargs
        self.status = "Initialized"
    
    def run(self):
        print("DEBUG: Creating directory for:", self.test_launch_name)
        os.mkdir(self.test_launch_name)

        if not os.path.isdir(self.test_launch_name):
            print("ERROR: Can not find directory: ", self.test_launch_name)
            sys.exit(-1)

        os.chdir(self.test_launch_name)
        self.status = "Running"
        self.test.run(self.env, self.srcDir, self.testDir, hpc=self.hpc, *self.args, **self.kwargs)
        self.status = "Finished"
        return

class TestRunner:
    def __init__(self, env, testDir, srcDir, *args, **kwargs):
        # The test directory is the directory that holds each test's implementation , not where
        # they are ran.
        self.env = env
        self.testDir= testDir
        self.srcDir = srcDir
        _debug_ = 0

        # Based on if the env we have is an HPC or not, initalize the HPC
        if env.hpc == True:
            # Initalize HPC
            raise NotImplementedError("HPC COMPATABLITY IS NOT YET IMPLEMENTED")
            pass
        else:
            self.hpc = None

        # At a Python's program startup, sys.path is set to PYTHONPATH (and not 
        # the normal PATH variable). Similar to the PATH environment, it is the locations
        # Python will search for importing Python modules.
        # To find the user created tests, append it to the front.
        if _debug_ > 0:
            print("TestRunner: Test directory is: ", self.testDir)

        sys.path.insert(0, self.testDir)

        self.manager = TestManager(self.testDir)
        self.scheduler = TestScheduler(self, self.testDir, self.srcDir, *args, **kwargs)

    def list_tests(self, *args, **kwargs):
        # List all tests
        return self.manager.list_tests()

    def list_test(self, tests, *args, **kwargs):
        # List a single test
        print("List test!")
        return self.manager.list_test(tests)

    def run_tests(self, tests, env, *args, **kwargs):
        # For each test:
        #  Use the test manager to check the given test
        #  If the test exists then run it using the Test Scheduler

        # Check To see if all tests requested on this system 
        # Check to see if the requested tests are avaliable on this sytem.
        # If they are, also check to see if the maximum CPU's are not over
        # the environments ammount
#        for test in tests:
#            # TODO: Might be worthwhile to try to find as many tests as possible and then return
#            # the all the test names that were not found
#            if self.manager.list_test(test) == None:
#                print("The test", test, "could not be found!")
#                return "The test "+test+" could not be found!"
#
        
        # Create the subdirectory of this regression test run and then move the cwd
        # into that test directory`

        # Run the tests
        self.scheduler.run_tests(tests)


class TestManager:
    def __init__(self, test_directory, *args, **kwargs):
        self.test_directory = test_directory

    def list_tests(self, *args, **kwargs):
        # Return a list all the valid and invalid tests
        verbose = kwargs.get('verbose', 0)

        if verbose > 0:
            print("TestManager: list_tests() - Listing tests found in:", self.test_directory)

        valid_tests = []
        invalid_tests = []
        for tests in os.listdir(self.test_directory):
            if os.path.isdir(os.path.join(self.test_directory, tests)):

                testFile = os.path.join(tests, tests).replace('/', '.')
                runName = testFile

                # Translate the directory path into what Python wants for its import_module command
                if '.' in runName:
                    runName = testFile.split('.')[0]

                try:
                    mod = import_module(testFile)
                    try:
                        test = getattr(mod, tests)
                        valid_tests.append([runName, test.test_name])
                    except:
                        invalid_tests.append([runName, "Could not load this test's attributes"])
                except Exception as e:
                    invalid_tests.append([testFile, e])

        return valid_tests, invalid_tests

    def list_test_suites(self, **kwargs):
        # List all of the available test-suites
        raise NotImplementedError("TestManager.list_test_suites "+NOT_IMPLEMENTED_ERROR)

    def list_test(self, tests, **kwargs):
        # Return the information about a single test or test-suite as a (dictionary or object?)
        raise NotImplementedError("TestManager.list_test "+NOT_IMPLEMENTED_ERROR)

    def check_test(self, test, **kwargs):
        # Check to see if the test suite and test name are on the system
        raise NotImplementedError("TestManager.check_test"+NOT_IMPLEMENTED_ERROR)

class TestScheduler:

    def __init__(self, testRunner, testDir, srcDir, *args, **kwargs):
        self.testManager = testRunner.manager
        self.env = testRunner.env
        print("Environment is: ", self.env)
        self.ncpus = testRunner.env.ncpus
        self.testDir = testDir
        self.srcDir = srcDir

    def _setup_tests(): # Possible function to set up test to take stuff out of run tests
        pass
       
    def _create_run_directory(self):
        # If all tests are able to be ran, then create the test directory
        # smarts.year-mm-dd_hh.mm.ss
        run_directory = 'run-smarts-'
        now = datetime.datetime.now()
        run_directory += now.strftime('%Y-%m-%d-%H.%M.%S')
        # print("DEBUG: Creating directory: ", run_directory)
        os.mkdir(run_directory)
        if not os.path.isdir(run_directory):
            print("ERROR: Could not create run_directory: ", run_directory)
            return False

        return run_directory
        
    def _check_dependencies(self, test, loaded_tests):
        print(test.test.test_name)
        if hasattr(test.test, 'dependencies'):
            if test.test.dependencies == None:
                return True
            else: # If this test has dependencies
                for dependency in test.test.dependencies:
                    # Check to see if the dependency is running or not
                    for tests in loaded_tests:
                        test_name = tests.test.__class__.__name__
                        if test_name == dependency:
                            print(tests.status)
                            if tests.status != "Joined":
                                return False
                            else:
                                return True
        else:
            return True

        return True

    

    def run_tests(self, tests, *args, **kwargs):
        # Pass in the test names? Or test objects?
        num_tests = len(tests)
        finished = 0
        avaliable_cpus = self.ncpus
        self.hpc = None
        

        # Import and then initalize each test as a Python Subprocess
        loaded_tests = []
        for test_launch_name in tests:
            """ Import each test as a module. """
            module = import_module(test_launch_name+'.'+test_launch_name)
            test = getattr(module, test_launch_name) # get the test from the module
            test = test() # Initialize the test
            print(test.test_name, "is scheduled to run!")
            """ Wrap our test class inside our extended multiprocessing.Process object. When we
            initalize this wrapper we will need to pass in any arguments that will need to have
            passed to the test, because we cannot overload the Process.start() function. """
            testProcess = TestSubProcess(test_launch_name, test,
                                         self.env,
                                         self.srcDir,
                                         self.testDir,
                                         self.hpc)
            loaded_tests.append(testProcess)

        # Create the run directory that will hold each test. Each test will be ran within their own
        # directories within this directory.
        self.run_directory = self._create_run_directory()

        if not self.run_directory:
            print("ERROR: There was a problem creating the run directory!")
            sys.exit(-1)

        os.chdir(self.run_directory)


        ################
        # Test Scheduler - TODO: Maybe have this in a new function TestScheduler.scheduler(..) ?
        ################
        while ( finished != num_tests):
           # print("Number of finished tests:", finished)
           # print("Number of total tests:", num_tests)

            if avaliable_cpus > 0:
                for test in loaded_tests:
    
                    # Start tge test if we gave enough CPUS and if test is either not alive
                    # or has not been ran
                    if ( test.test.nCPUs <= avaliable_cpus and not test.is_alive()
                                                           and test.exitcode is None):


            
                        # Check to see if this test has a dependency
                        # If true, all the dependencies are finished so laucnh the test
                        # if not, then don't
                        #print("Checking dependencies!")
                        if not self._check_dependencies(test, loaded_tests):
                            #print(test.test.test_name, "not gonna start")
                            continue;

                        avaliable_cpus -= test.test.nCPUs
                        test.start()
                        print(test.test.test_name, "has started!\n")

            # Join tests
            for test in loaded_tests:
                #print("Joing test: ", test.exitcode, test.is_alive(), test.status)
                if (test.exitcode is not None and not test.is_alive() 
                                              and test.status != "Joined"):
                    test.join(.2) # Wait for .2 seconds for the test to join
                    test.status = "Joined"
                    print("Joined with ", test.test.test_name, "this test: ", 
                                          test.test.status, "\texit: ", test.exitcode)
                    avaliable_cpus += test.test.nCPUs
                    finished += 1

        return
