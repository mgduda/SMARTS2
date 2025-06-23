""" SMARTs Command Line Runner """

from __future__ import absolute_import, division, print_function
import os
import sys
import argparse
from smarts.config import CommandLineConfig, SmartsCFConfig, SmartsConfig, SmartscfType
from smarts.env import Environment
from smarts.testManager import TestManager

def print_tests(test_directory, valid_tests, invalid_tests):
    """ Command line routine to retrive valid and invalid tests and print
    them out to the terminal """

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
    """ Retrive and print the modsets in the environment file specified with -e/--env """
    # SMARTS Command Line API print modset function - Print the list of modsets
    # found in the enviornment.yaml file
    print("Avaliable Modsets on:", envName)
    for mods in modsets:
        print('-', mods['name'], '\t', mods['compiler']['version'])


def print_test_info(tests):
    """ Retrive and print the infromation of a specifiec test, including its name,
    description, number of cpus and other information """

    tests = sorted(tests, key=lambda t: t['runName'])

    for test in tests:
        if 'error' in test.keys():
            print("ERROR LOADING:", test['runName'])
            print(test['error'])
        else:
            print("    Run name:", test['runName'])
            print("   Long name:", test['longName'])
            print(" Description:", test['description'])
            print("       ncpus:", test['ncpus'])
            print('Dependencies:', test['dependencies'])

        if len(tests) != 1:
            print('------------------------------------------------------')

    return 0


def setup_smarts(envFile=None, testDir=None, srcDir=None):
    """ Helper function to intialize the smarts Environment class and
    smarts TestManager - Will fail if any of the above files or directories
    do not exist """

    print(testDir)
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
    if srcDir:
        if not os.path.isdir(srcDir):
            print("ERROR: The source directory does not exist!")
            print("ERROR: Was it specified correctly?")
            print("ERROR: ", srcDir)
            sys.exit(-1)

    env = Environment(envFile)
    if env.parse_file() == -1:
        sys.exit(-1)

    test_handler = TestManager(env, testDir, srcDir)

    return env, test_handler


def list_cmd(args):
    """ SMARTS Command Line API for handling the list command passed in to
    the argparser. """

    testDir = args.config.test_dir
    envFile = args.config.env_file

    env, test_handler = setup_smarts(envFile, testDir)

    if len(args.items) == 1:
        if args.items[0] == 'tests':
            valid_tests, invalid_tests = test_handler.list_tests()
            print_tests(testDir, valid_tests, invalid_tests)
            return 0
        elif args.items[0] == 'test-suites':
            test_handler.list_testSuites()
            return 0
        elif args.items[0] == 'modsets':
            # List out all the avaliable modsets
            modsets = env.list_modsets()
            print_modsets(modsets, env.name)
            return 0
        else:
            print("ERROR: Unkown subcommand: ", args.items[0])
            args.listParser.print_help()
            sys.exit(-1)
    if len(args.items) > 1:
        # Print infromation of a specific item, either tests or modsets
        if args.items[0] == 'test' or args.items[0] == 'tests':
            tests = test_handler.list_test(args.items)
            print_test_info(tests)
            return 0
        elif args.items[0] == 'modset':
            # Print out the infromation for a single modset
            pass

    return 0


def run_cmd(args):
    """ SMARTS Command Line API for handling the run command passed in to
    the argparser. """
    testDir = args.config.test_dir
    srcDir = args.config.test_dir
    envFile = args.config.env_file
    tests = list(set(args.items))

    env, test_handler = setup_smarts(envFile=envFile, testDir=testDir, srcDir=srcDir)
    test_handler.run_tests(tests, env)

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="SMARTS",
                                     description="A regression testing system for MPAS",
                                     epilog=None)


    config = SmartsConfig(parser)

    subparsers = parser.add_subparsers(dest='command',
                            description='command description',
                            help='Sub-command help message')

    # List subcommand
    listParser = subparsers.add_parser('list',
                                    help="List SMART's tests, test suites and compilers",
                                    description='Description for list sub-command',
                                    epilog='Epilog for list sub-command')
    listParser.add_argument('items',
                            help='List items help message',
                            nargs='+')
    listParser.set_defaults(func=list_cmd)

    # Run subcommand
    runParser = subparsers.add_parser('run',
                                    help="Run a test or a test-suite by name",
                                    description='Description for run sub-command',
                                    epilog='Epilog for run sub-command')
    runParser.add_argument('items',
                        help='Run items help message',
                        nargs='+')
    runParser.set_defaults(func=run_cmd)

    args = parser.parse_args()
    args.parser = parser
    args.listParser = listParser
    args.runParser = runParser
    args.config = config

    if args.command is None:
        parser.print_help()
        sys.exit(-1)

    try:
        args.config.test_dir
    except ValueError as ve:
        parser.print_help()
        sys.exit(-1)
    
    try:
        args.config.src_dir
    except ValueError as ve:
        parser.print_help()
        sys.exit(-1)

    try:
        args.config.env_file
    except ValueError as ve:
        parser.print_help()
        sys.exit(-1)


    args.func(args)