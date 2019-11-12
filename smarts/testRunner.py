""" SMARTs Test Runner - With Test Manager and Test Scheduler """
import os
import string
import sys
from importlib import import_module

class TestRunner:
    def __init__(self, test_directory, *args, **kwargs):
        self.directory = test_directory

        print("TestRunner: Test directory is: ", self.directory)
        sys.path.insert(0, self.directory)

        self.manager = TestManager(self.directory)
        self.scheduler = TestScheduler()

    def list_tests(self, **kwargs):
        # List all tests
        self.manager.list_tests()
        return 0


    def list_test(self, tests, **kwargs):
        # List a single test
        pass

    def run_tests(self, tests, **kwargs):
        # For each test:
        #  Use the test manager to check the given test
        #  If the test exists then run it using the Test Scheduler
        pass


class TestManager:
    def __init__(self, test_directory, *args, **kwargs):
        self.test_directory = test_directory

    def list_tests(self, *args, **kwargs):
        # List all the available tests
        print("TestManager: list_tests() - Listing tests found in", self.test_directory)

        # TODO: Pretty print out the test_filenames and their descriptions using either a table or
        # the python str.format() list and
        # https://docs.python.org/3.8/library/string.html#formatspec

        print("    Test Name\t        Test Description")
        for tests in os.listdir(self.test_directory):
            if os.path.isdir(os.path.join(self.test_directory, tests)):
                testFile = os.path.join(tests, tests).replace('/', '.')
                #print("- Test:", tests, '    ', testFile)
                mod = import_module(testFile)
                try: 
                    test = getattr(mod, tests)
                    print("- ", testFile, '\t\t', test.test_description)
                except:
                    print("- ", tests, "\tCould not load test attributes")


        return 0

    def list_test_suites(self, **kwargs):
        # List all of the available test-suites
        pass

    def list_test(self, name, **kwargs):
        # Print the information about a single test or test-suite
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
