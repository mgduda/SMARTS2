""" SMARTs Test Runner - With Test Manager and Test Scheduler """
import os
import string
import sys
import datetime
from importlib import import_module

from multiprocessing import Process
from multiprocessing.managers import BaseManager, NamespaceProxy

from smarts.reporters.reporter import Result

from importlib import import_module
from multiprocessing import Process
from multiprocessing.managers import BaseManager, NamespaceProxy

NOT_IMPLEMENTED_ERROR = "IS NOT YET IMPLEMENTED"

INITIALIZED = "INITIALIZED"
SCHEDULED = "SCHEDULED"
UNSCHEDULED = "UNSCHEDULED"
RUNNING = "RUNNING"
FINISHED = "FINISHED"
JOINED = "JOINED"
ERROR = "ERROR" 

PASSED = "PASSED"
FAILED = "FAILED"
INCOMPLETE = "INCOMPLETE"


class TestRunner:
    """ class TestRunner - Class responsible for managing and running tests """
    def __init__(self, env, testDir, srcDir, *args, **kwargs):
        """ Initalize the TestRunner. After initalization the TestRunner will have two
        nested-classes, a TestManager (self.manager) and a TestScheduler (self.scheduler),
        as well as an HPC class (if avaliable)

        Arguments:
        env     -- An initalized and parsed Environment class - (Class Environment)
        testDir -- The directory that holds SMARTS test - (String or Pathlike object)
        srcDir  -- The directory that to be tested - (String or Pathlike object)
        """
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
        """ Return a list of valid and a list of invalid tests found in the testDir. In the valid
        test list, each element will contain the launch name and test name. In the invalid tests
        list, each element will contain the launch name and then the reason it is an invalid tests.
        """
        return self.manager.list_tests()

    def list_test(self, tests, *args, **kwargs):
        """ Return the information of a specific test, including its name, description etc - See
        TestManager.list_test(...) for more information on this function. """
        print("List test!")
        return self.manager.list_test(tests)

    def run_tests(self, tests, env, *args, **kwargs):
        """ Run all the tests specified in tests - See TestScheduler.run_tests(...) for more
        information on this function.

        tests -- List of strings specifying tests to run (List of strings)
        """
        self.scheduler.run_tests(tests)


class TestManager:
    """ Class TestManager - Class for discovering tests in the test directory """
    def __init__(self, test_directory, *args, **kwargs):
        self.test_directory = test_directory

    def list_tests(self, *args, **kwargs):
        """ Return a list of valid and a list of invalid tests found in the testDir. In the valid
        test list, each element will contain the launch name and test name. In the invalid tests
        list, each element will contain the launch name and then the reason it is an invalid 
        tests. """
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
        """ List all of the available test-suites """
        raise NotImplementedError("TestManager.list_test_suites "+NOT_IMPLEMENTED_ERROR)

    def list_test(self, tests, **kwargs):
        """ Return the information about a single test or test-suite as a
        (dictionary or object?) """
        raise NotImplementedError("TestManager.list_test "+NOT_IMPLEMENTED_ERROR)

    def check_test(self, test, **kwargs):
        """ Check to see if the test suite and test name are on the system """
        raise NotImplementedError("TestManager.check_test"+NOT_IMPLEMENTED_ERROR)


""" Class TestSubProcess - Wrapper for individual test to enable management of multiprocessing """
class TestSubProcess(Process):
    def __init__(self, test_launch_name, test,
                                         result,
                                         env,
                                         srcDir,
                                         testDir,
                                         hpc=None,
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
        self.status = INITIALIZED
        self.DEBUG = kwargs.get('DEBUG', 0)

        # Initalize the Result Class - I.E. Start the Result Manager
        result = result()
        result.start()
        self.result = result.result()

    def run(self):
        if self.DEBUG > 1:
            print("DEBUG: Creating directory for:", self.test_launch_name)

        os.mkdir(self.test_launch_name)

        if not os.path.isdir(self.test_launch_name):
            print("ERROR: Can not find directory: ", self.test_launch_name)
            sys.exit(-1)

        os.chdir(self.test_launch_name)
        self.status = RUNNING
        self.test.run(self.env,
                      self.result,
                      self.srcDir,
                      self.testDir,
                      hpc=self.hpc,
                      *self.args,
                      **self.kwargs)
        self.status = FINISHED
        return

    def isRunning(self):
        if self.status == RUNNING:
            return True
        else:
            return False

    def isFinished(self):
        if self.exitcode != None:
            return True
        else:
            False

    def isScheduled(self):
        if self.status == SCHEDULED:
            return True
        else:
            return False



class TestScheduler:
    """ Class TestScheduler - Class responsible for managing resources and launching tests as
    subprocesses """

    def __init__(self, testRunner, testDir, srcDir, *args, **kwargs):
        """ Initalize a TestScheduler Class

        testRunner - A initialized TestRunner class
        testDir - The test directory (where tests are stored)
        srcDir - The source code to test
        """
        self.manager = testRunner.manager
        self.env = testRunner.env
        self.ncpus = testRunner.env.ncpus
        self.testDir = testDir
        self.srcDir = srcDir

    def _create_run_directory(self):
        """ Create a run directory with the structure: run-smarts.year-mm-dd_hh.mm.ss """
        run_directory = 'run-smarts-'
        now = datetime.datetime.now()
        run_directory += now.strftime('%Y-%m-%d-%H.%M.%S')
        os.mkdir(run_directory)
        if not os.path.isdir(run_directory):
            print("ERROR: Could not create run_directory: ", run_directory)
            return False

        return run_directory

    def _get_depends_status(self, test, loaded_tests):
        """ Return a list of booleans that correspond test's dependencies status (currently either
         joined or not) """
        dependency_status = []

        if hasattr(test.test, 'dependencies'):
            if test.test.dependencies == None:
                return [True]
            else: # If this test has dependencies
                for dependency in test.test.dependencies:
                    # Check to see if the dependency is running or not
                    for tests in loaded_tests:
                        test_name = tests.test.__class__.__name__
                        if test_name == dependency:
                            if tests.status != JOINED:
                                dependency_status.append(False)
                            else:
                                dependency_status.append(True)
        else:
            return [True]

        return dependency_status


    def _update_dependents(self, test, loaded_tests):
        """ Recursive function to update the decedents of test depending on its result
        (test.result.result). If a test does not complete, then update its dependencies to be
        UNSCHEDULED. Then recursively call this function on those tests to update any
        dependencies they might have. """
        testStatus = test.result.result
        test_name = test.test.test_name
        test_launch_name = test.test.__class__.__name__

        if (   testStatus == "FAILED"
            or testStatus == "INCOMPLETE"
            or testStatus == "ERROR"
            or testStatus == None):
            for t in loaded_tests:
                if not hasattr(t.test, 'dependencies'):
                    continue

                if t.test.dependencies is None:
                    continue

                if test_name in t.test.dependencies or test_launch_name in t.test.dependencies:
                    # If test has failed, mark its dependents as UNSCHEDULED and then update those
                    # the dependents of those tests.
                    print("SMARTS:", t.test_launch_name, " has been unscheduled because one of its dependency failed")
                    t.status = UNSCHEDULED
                    t.result.result = "INCOMPLETE"
                    self._update_dependents(t, loaded_tests)

    def run_tests(self, tests, *args, **kwargs):
        """ Attempt to run all the tests found in tests. Tests will be ran, if:

        1. They can be loaded successfully
        2. There is enough resources (CPUS) available for them to be ran
        3. If all of their decencies complete with the result == PASSED

        Unless one test is a dependency of another, tests will be ran concurrently based 
        on the number of MAX CORES specified in the environment.yaml file. If a test has
        dependency, it will only run once they have all completed with the result == PASSED.

        If a test with dependents fail, all of its dependencies will not be ran.

        tests - List of strings of tests run name (String)
        """

        self.DEBUG = 0

        num_tests = len(tests)
        finished = 0
        avaliable_cpus = self.ncpus
        self.hpc = None
        run = True
        requested_test_names = tests


        """ Check to see if all the tests are valid tests """
        avaliable_tests, invalid_tests = self.manager.list_tests()
        launch_names = [t[0] for t in avaliable_tests]
        test_names = [t[1] for t in avaliable_tests]

        for test in tests:
            if test not in launch_names and test not in test_names:
                # This test was invalid - I.E. syntax, wrong format etc
                for invalid in invalid_tests:
                    if test in invalid[0]:
                        print("ERROR: The test, '", test, "' could not be loaded!", sep="")
                        print("ERROR:", invalid[1])
                        sys.exit(-1)

                # Could not find test - Test name
                print("ERROR: '", test, "' is not a test that could be found within:", sep="")
                print("ERROR:", os.path.abspath(self.testDir))
                sys.exit(-1)

        """ Import and initialize each test - Exit if any Test requested is fails to be 
        initialized """
        loaded_tests = []
        for test_launch_name in tests:
            # TODO: Try except here
            module = import_module(test_launch_name+'.'+test_launch_name)
            test = getattr(module, test_launch_name) # get the test from the module
            test = test() # Initialize the test

            print("SMARTS: ", test.test_name, "is scheduled to run!")

            testProcess = TestSubProcess(test_launch_name, test,
                                         Result,
                                         self.env,
                                         self.srcDir,
                                         self.testDir,
                                         self.hpc)
            testProcess.status = INITIALIZED
            loaded_tests.append(testProcess)


        """ Check to see if this tests dependencies (if it has any) are scheduled to run """
        for test in loaded_tests:
            if hasattr(test.test, 'dependencies'):
                if not test.test.dependencies: # test.test.dependencies == None
                    continue

                for dep in test.test.dependencies:
                    if dep not in requested_test_names:
                        print("ERROR: The dependency '", dep, "' was not requested to run!", sep="")
                        print("ERROR: Please specify it to run!")
                        sys.exit(-1)
                    else:
                        continue
            else:
                continue


        """ Check to see if this test does not require more resources then whats available """
        for test in loaded_tests:
            if test.test.nCPUs > avaliable_cpus:
                print("ERROR: The test '", test.test.test_name, " requires more cpus the available!", sep='')
                print("ERROR: The machine: '", self.env.name, "' has ", avaliable_cpus, " cpus available", sep='')
                print("ERROR: And '", test.test.test_name, "' requested: ", test.test.nCPUs, sep='')
                sys.exit(-1)


        """ If tests pass all the checks above, then set its status to SCHEDULED """
        for test in loaded_tests:
            test.status = SCHEDULED

        
        """ Since all tests pass the above checks, create the run directory and change to that
        directory  """
        self.run_directory = self._create_run_directory()
        if not self.run_directory:
            print("ERROR: There was a problem creating the run directory!")
            sys.exit(-1)
        os.chdir(self.run_directory)

        """ Initalize reporter with reporter type """
        # reporter = initalize_reporter(reporterType)

        ################
        # Test Scheduler - TODO: Maybe have this in a new function TestScheduler.scheduler(..) ?
        ################
        while ( run ):
            """ Start tests 
            If we have enough CPUs, and the test is scheduled and its dependencies have all run,
            then start it """
            for test in loaded_tests:
                # If we have enought resources
                if (test.test.nCPUs <= avaliable_cpus and test.isScheduled()): 
                    # Check dependencies
                    if all(self._get_depends_status(test, loaded_tests)):
                        avaliable_cpus -= test.test.nCPUs
                        test.start() # TODO: Try Accept here ??
                        test.status = RUNNING
                        print("SMARTS: ", test.test.test_name, "has started!\n")


            """ Join tests """
            for test in loaded_tests:
                if test.isRunning():
                    if test.isFinished():
                        test.join(.01)
                        test.status = JOINED
                        avaliable_cpus += test.test.nCPUs
                        print("SMARTS: ", test.test.test_name, " finished - It: ", test.result.result)

                        if test.result.result is None:
                            test.result.result = ERROR

                        # See if this test fails or not. If it fails, then update any tests that have
                        # it as a dependency as UNSCHEDULED
                        self._update_dependents(test, loaded_tests)

            """ Determine if we are finished running tests or not.  We have finished running tests
            when there is no more tests marked as either RUNNING or as SCHEDULED. """
            running = [True for test in loaded_tests if test.status == RUNNING]
            scheduled = [True for test in loaded_tests if test.status == SCHEDULED]

            if any(running) or any(scheduled):
                continue
            else:
                print("DEBUG: All tests are completed - Exiting the scheduler!")
                run = False

        # Report Results here
        # Sort tests so they print out in the order they ran
        loaded_tests = sorted(loaded_tests, key=lambda t: int(t.name.split('-')[1]))

        # for test in loaded_tests:
        #   reporter.add_results(test.result)
        # 
        # reporter.generate_report()

        print("\n\nTEST RESULTS")
        print("===============================================")
        for test in loaded_tests:
            print(' - ', test.test_launch_name,
                  ' - ', test.result.result,
                  ' - "', test.result.msg, '"', sep='')
        return
