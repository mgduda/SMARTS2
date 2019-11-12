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
        print("TestManager: list_tests() - Listing tests found in:", self.test_directory)

        errors = []

        import textwrap

        print("")
        print("{0:>13} {1:>19}".format(' Launch Name', '| Long Name'))
        print("-" * 50)
        for tests in os.listdir(self.test_directory):

            if os.path.isdir(os.path.join(self.test_directory, tests)):
                testFile = os.path.join(tests, tests).replace('/', '.')
                runName = testFile

                if '.' in runName:
                    runName = testFile.split('.')[0]

                colLen = 15

                if (len(runName) > colLen):
                    runName = runName[0:15]
                    runName += '...'
                else:
                    # Pad the string with spaces
                    runName += " " * (colLen - len(runName) + 3)

                try:
                    mod = import_module(testFile)
                    try:
                        test = getattr(mod, tests)
                        print("- {0}\t{1}".format(runName, test.test_name))
                    except:
                        print("- {0}\t{1}".format(runName, "Could not load this test's attributes"))


                except Exception as e:
                    # TODO: Instead of printing this in line, make a list of the tests that could
                    # not be loaded and then print them out at the end.
                    # Make sure the list is a list of tests AND a list of the REASONS they weren't
                    # able to be loaded!
                    errors.append([testFile, e])

        print("\n")
        print("WARNING: The following tests could not be loaded:\n")
        print("{0:<1} {1:>39}".format("Test Name", "Reason"))
        for err in errors:
            print("WARNING: {0:<1} {1:>60}".format(str(err[0]), str(err[1])))

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
