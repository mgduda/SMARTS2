""" SMARTs Command Line Runner """

from __future__ import absolute_import, division, print_function
import os
import sys
import argparse
from smarts.env import Environment
from smarts.testRunner import TestRunner



def print_tests(test_directory, valid_tests, invalid_tests):
    # Print the list of valid and invalid lists to the tests
    print("Tests found in: ", test_directory, ":", sep='')

    if len(valid_tests) > 0:
        print("Valid tests:")
        for tests in valid_tests:
            print("  -", tests[0], "--", tests[1])

    print()
    
    if len(invalid_tests) > 0:
        print("Invalid tests: (These tests were not able to be loaded)")
        for tests in invalid_tests:
            print("  x", tests[0], "--", tests[1])
        print()
    elif len(valid_tests) == 0 and len(invalid_tests) == 0:
        print("ERROR: No tests found in this directory!")
        print("ERROR: Was the right test directory given or were the")
        print("ERROR: tests created correctly?")
        return -1

    return 0

def print_modsets(modsets, envName):
    print("Avaliable Modsets on:", envName)
    for mods in modsets:
        print('-', mods['name'], '\t', mods['compiler']['version'])


def print_test_info(tests):
    pass


def setup_smarts(envFile, testDir, srcDir):
    if not os.path.isfile(envFile):
        print("ERROR: The environment.yaml file does not exist!")
        print("ERROR: Was it specified correctly?")
        print("ERROR: ", envFile)
        sys.exit(-1)
    if not os.path.isdir(testDir):
        print("ERROR: The test directory does not exist!")
        print("ERROR: Was it specified correctly?")
        print("ERROR: ", testDir)
        sys.exit(-1)
    if not os.path.isdir(srcDir):
        print("ERROR: The source directory does not exist!")
        print("ERROR: Was it specified correctly?")
        print("ERROR: ", srcDir)
        sys.exit(-1)

    env = Environment(envFile)
    env.parse_file()  # TODO: Handle/report env.yaml file parsing errors here
    test_handler = TestRunner(testDir, env, srcDir)

    return env, test_handler


def list_cmd(args):
    """ Parse the list command """
    testDir = args.dir[0] 
    testDir = os.path.abspath(testDir)
    srcDir = args.src[0]
    srcDir = os.path.abspath(srcDir)
    envFile = args.env[0]
    envFile = os.path.abspath(envFile)
    
    #print("TEST DIR: ", testDir)
    #print("ENV FILE: ", envFile)

    env, test_handler = setup_smarts(envFile, testDir, srcDir)
    
    if args.items[0] == 'tests':
        valid_tests, invalid_tests = test_handler.list_tests()
        print_tests(testDir, valid_tests, invalid_tests)
        return 0

    elif args.items[0] == 'test':
        print("Calling test_handler.list_test")
        test = test_handler.list_test(args.items)
        print_test_info(tests)
        return 0

    elif args.items[0] == 'test-suites':
        test_handler.list_testSuites()
        return 0

    elif args.items[0] == 'modsets':
        # List out all the avaliable modsets
        modsets = env.list_modests()
        print_modsets(modsets, env.name)
        return 0

    elif args.items[0] == 'modset':
        # Print out the infromation for a single modset
        pass
    
    return 0


def run_cmd(args):
    """ Parse the run command """
    testDir = args.dir[0] # The directory that contains each test
    srcDir = args.src[0]  # The directory that contains the code to be tested
    envFile = args.env[0] # The environment.yaml file

    env, test_handler = setup_smarts(envFile, testDir, srcDir)

    print("Running tests: ", args.items)
    test_handler.run_tests(args.items, env)

    return 0


if __name__ == "__main__":
    """ SMARTs Command Line Argument Parsing """


    parser = argparse.ArgumentParser(prog="smarts",
                                      description="A regression testing system for MPAS",
                                      epilog="Don't Panic (This is the Epilog Area)"
                                    )

    parser.add_argument('-e', '--env',
                        dest='env',
                        help='The location of the env.yaml file',
                        metavar='env.yaml',
                        required=True,
                        default=None,
                        nargs=1)
    parser.add_argument('-s', '--src',
                        dest='src',
                        help='The directory that holds the code to test changes (MPAS-Model)',
                        metavar='dir',
                        required=True,
                        default=None,
                        nargs=1)
    parser.add_argument('-d', '--dir',
                        dest='dir',
                        help='The location of the test directory',
                        metavar='dir',
                        required=True,
                        default=None,
                        nargs=1)
    parser.add_argument('-v', '--verbose',
                        dest='verbose',
                        help="Output debug level",
                        type=int,
                        metavar='level',
                        default=0,
                        nargs=1)


    subparsers = parser.add_subparsers(dest='command',
                                       required=True,
                                       description='command description',
                                       help='Sub-command help message')

    # List subcommand
    parserList = subparsers.add_parser('list',
                                       help="List SMART's tests, test suites and compilers",
                                       description='Description for list sub-command',
                                       epilog='Epilog for list sub-command')
    parserList.add_argument('items', 
                             help='List items help message',
                             nargs='+')
    parserList.set_defaults(func=list_cmd)

    # Run subcommand
    parserRun = subparsers.add_parser('run',
                                     help="Run a test or a test-suite by name",
                                     description='Description for run sub-command',
                                     epilog='Epilog for run sub-command')
    parserRun.add_argument('items',
                            help='Run items help message',
                            nargs='+')
    parserRun.set_defaults(func=run_cmd)

    args = parser.parse_args()

    # Check to see if the environment file exists
    args.func(args)
