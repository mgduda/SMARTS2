""" SMARTs Commandline Runner """

import argparse

def list_cmd(args):
    
    if len(args.items) == 1:
        if args.items[0] == 'tests':
            print("Listing all of the tests")
            # test_handler.list_tests()
            return 0
        elif args.items[0] == 'test-suites':
            print("Listing all of the test-suites")
            # test_handler.list_testSuites()
            return 0
        elif args.items[0] == 'modsets':
            print("Listing all of the test-suites")
            # env.list_modests()
            return 0

    for item in args.items:
        print("Printing test/test-suite information for: ", item)
        # test_handler.list_test(item)
    
    return 0

def run_cmd(args):

    print("Running tests: ", args.items)
    # test_runner.add_test(args.items)
    return 0



if __name__ == "__main__":
    """ """
    parser = argparse.ArgumentParser(prog="smarts",
                                      description="A regression testing system for MPAS",
                                      epilog="Don't Panic (This is the Epilog Area)"
                                    )

    subparsers = parser.add_subparsers(dest='command',
                                       #required=True,
                                       description='command description',
                                       help='Sub-command help message')

    # List subcommand
    parserList = subparsers.add_parser('list',
                                       help="List SMART's tests, test suites and compilers",
                                       description='Description for list sub-command',
                                       epilog='Epilog for list sub-command')
    parserList.add_argument('items', nargs='+')
    parserList.set_defaults(func=list_cmd)

    # Run subcommand
    parserRun = subparsers.add_parser('run',
                                     help="Run a test or a test-suite by name",
                                     description='Description for run sub-command',
                                     epilog='Epilog for run sub-command')
    parserRun.add_argument('items', nargs='+')
    parserRun.set_defaults(func=run_cmd)
    
    args = parser.parse_args()
    args.func(args)
