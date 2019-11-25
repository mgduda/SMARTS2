""" SMARTs Test Runner - With Test Manager and Test Scheduler """
import os
import string
import sys
from importlib import import_module

# from smarts import HPC
# import environment

class TestRunner:
    def __init__(self, test_directory, env, src, *args, **kwargs):
        # The test directory is the directory that holds each test's implementation , not where
        # they are ran.
        self.directory = test_directory
        self.env = env
        self.src = src
        _debug_ = 0

        # Based on if the env we have is an HPC or not, initalize the HPC
        if env.hpc == True:
           # Initalize HPC
            pass
        else:
           # HPC = None
            pass

        # At a Python's program startup, sys.path is set to PYTHONPATH (and not 
        # the normal PATH variable). Similar to the PATH environment, it is the locations
        # Python will search for importing Python modules.
        # To find the user created tests, append it to the front.
        if _debug_ > 0:
            print("TestRunner: Test directory is: ", self.directory)

        sys.path.insert(0, self.directory)

        self.manager = TestManager(self.directory)
        self.scheduler = TestScheduler()

    def list_tests(self, *args, **kwargs):
        # List all tests
        return self.manager.list_tests()

    def list_test(self, tests, *args, **kwargs):
        # List a single test
        pass

    def run_tests(self, tests, env, *args, **kwargs):
        # For each test:
        #  Use the test manager to check the given test
        #  If the test exists then run it using the Test Scheduler

        # Check To see if all tests requested on this system 
        # Check to see if the requested tests are avaliable on this sytem.
        # If they are, also check to see if the maximum CPU's are not over
        # the environments ammount
        for test in tests:
            # TODO: Might be worthwhile to try to find as many tests as possible and then return
            # the all the test names that were not found
            if self.manager.list_test(test) == None:
                print("The test", test, "could not be found!")
                return "The test "+test+" could not be found!"

        
        # Create the subdirectory of this regression test run and then move the cwd
        # into that test directory`
        pass


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
        pass

    def list_test(self, name, **kwargs):
        # Return the information about a single test or test-suite as a (dictionary or object?)


        pass

    def check_test(self, name, **kwargs):
        # Check to see if the test suite and test name are on the system
        pass


class TestScheduler:
    def __init__(self, *args, **kwargs):
        pass

    def run_tests(self, tests, **kwargs):
        # Run all the test or suite-tests in tests
        pass
