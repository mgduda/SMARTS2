""" SMARTs Test Runner - With Test Manager and Test Scheduler """

class TestRunner:
    def __init__(self, *args, **kwargs):
        self.testManger = TestManager()
        self.testScheduler = TestScheduler()

    def list_all_tests(self, **kwargs):
        # List all tests
        pass

    def list_test(self, tests, **kwargs):
        # List a single test
        pass

    def run_tests(self, tests, **kwargs):
        # For each test:
        #  Use the test manager to check the given test
        #  If the test exists then run it using the Test Scheduler
        pass


class TestManager:
    def __init__(self, *args, **kwargs):
        pass

    def list_tests(self, *args, **kwargs):
        # List all the available tests
        pass

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
    def __init__(self, args, **kwargs):
        pass

    def run_tests(self, tests, **kwargs):
        # Run all the test or suite-tests in tests
        pass
