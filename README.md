# Simple MPAS Atmosphere Regression Testing System (SMARTS)

The Simple MPAS Atmosphere Regression Testing System or SMARTS, is a general regression
testing system. Developed to test changes for MPAS Atmosphere and its tool set, it allows
for generalized testing of potentially any software system.

SMARTS is written in Python, and its tests are also written in Python, thus, anything
that can be coded in Python can be made into a test. For instance, creating a file in
Python, calling a subprocess to compile MPAS code, or launching a simulation.

Tests are launched as subprocesses, and can be launched concurrently to
maximize efficiency. Machine resources (number of cpus, compilers, libraries,
MPI implementations) are described in env.yaml files and thus enable SMARTS to
be used with on a verity of machines with a verity of compilers and libraries.

In future release, SMARTS will have APIs to be used with a number of different services,
for instance a Github API, or across multiple machines. For now, SMARTS can only be ran
on the command line.

For more information on SMARTS please see its design document: 
https://docs.google.com/document/d/1ryoUOnww6uHigySUX7z7PBN-mb25YdyRO5eTPettfqw/edit?usp=sharing

# Quickstart Guide

0. Install [https://pyyaml.org/wiki/PyYAML](PyYAML) - `pip3 install pyYAML --user`. If you're running
on Cheyenne, this module is available by running `ncar_pylib`.
```
ml load python
ml load ncarenv
ncar_pyblib
```

1. Clone SMARTS onto your Machine and create an env.yaml file for your machine. The envs/
directory contains already created env.ymal files. Use these, and the Environment section of
the design document to create one for your machine.

2. List and run tests - Next, see if you can run the `smarts.py` commandline program.

``` 
usage: smarts [-h] [-e env.yaml] [-s dir] [-t dir] [-v level] {list,run} ...

A regression testing system for MPAS

optional arguments:
  -h, --help            show this help message and exit
  -e env.yaml, --env-file env.yaml
                        The location of the env.yaml file
  -s dir, --src-dir dir
                        The directory that holds the code to test changes
                        (MPAS-Model)
  -t dir, --test-dir dir
                        The location of the test directory
  -v level, --verbose level
                        Output debug level

subcommands:
  command description

  {list,run}            Sub-command help message
    list                List SMART's tests, test suites and compilers
    run                 Run a test or a test-suite by name
```

The smarts.py program works in a similar manner as the git command line program. It
has subcommands. For instance, git has `git remote`, `git remote list` and
`git add`, `git commit`, etc. smarts.py works in a similar manner, but has subcommands
`smarts.py list` and `smarts.py run`. Each subcommand contains its own help message, which
can be retrieved by typing `smarts.py subcommand --help`. To bring up the help message 
above, type `smarts.py -h`.

The smarts.py program needs three 'optional' arguments to run: An environment file 
(`-e/--env`), a directory that contains tests (`-t/--test-dir`) and a source directory 
that contains the source code you want to test (`-s/--src-dir`).

Running `python3 smarts.py list tests` will display the tests available in the directory
passed by `-t`.

3. Create a test of your own

Tests are also implemented in Python as a class and are imported by the TestRunner. 
Individual tests will need to reside in a directory of their own. The name of this 
directory will need to be the same name of the file of the test and will need to be 
the same name of the class of the tests.

Below is an example tests that contains the bare minimum needed to run:

``` Python
import os # User imported libraries

class test_example:
    test_name = "Test Example"
    test_description = "Create a directory and see if it was created" \       
                       "successfully"
    ncpus = 1
    test_dependencies = None

    def run(self, env, result, src_dir, test_dir, hpc=None, *args,   
                                                            **kwargs):
        if True:
          result.result = "PASSED"
          result.msg = "It appears True is True!"
        else:
          result.result = "FAILED"
          result.msg = "It appears True is in fact, not True!"
```

Test will need th follow attributes in their class to be able to be ran:
1. `test_name` - Required - The long name of the test
2. `test_description` - Optional - The description of the test 
3. `ncpus` - Required - The number of CPUs this test will use
4. `test_depencies` - Optional - A list of test launch names (i.e. classnames) that this 
    test is depedent on. For instance: `['gnu_check', 'intel_check']`

The test will then also need to have a run function as the one above with the
same arguments (in the same position):
``` Python
def run(self, env, result, src_dir, test_dir, hpc=None, *args, **kwargs):
```
You can use these arguments to help write your tests. 

1. `env` - Env Class Instance - A copy of the environment class loaded with the env.yaml file specified
          for the machine. You can use the environment class to find and load specific
          modsets.
2. `result` - Result Object - A result object. This object will communicate the result of your test
            with the TestScheduler. Set the attribute result (`result.result`) to either
            "PASSED" or "FAILED" respectivly. If your test does not set `result.result`
            your test will fail.
3. `src_dir` - String - The directory that contain the source files to be tested. Use this
             path to copy files from the code you wish to test.
4. `test_dir` - String - The directory that contains the test implementation. Use this
              path to retrive default input files (i.e. namelist.atmosphere for an idealized
              MPAS simulation)
5. `hpc`- HPC Class Instance or None - An HPC class that will be an interface to the HPC
              scheduler (not yet implemented). If HPC == None, then this machine is not an
              HPC.

# Things that work well

* Writing and launching tests
* Loading compilers, mpi implementations and libraries
* Making tests dependent upon other tests
* Seeing the results of tests
* Launching tests in parallel.

# Things that don't work well

* Loading some libraries on some machines (i.e. reddwarf has some issues)
* Handling errors when it can't load a library successfully with LMOD

# Planned Features

## Beta Release - v0.5
* ~~Dependencies~~
* ~~Schedules Test Concurrently~~
* Load Modules Completely
   * Loads compilers, mpi implementations and libraries
   * Needs a little more testing
* ~~Runs tests and reports their status via stdout (but does not call a reporter)~~
* Requirements Document mostly finished
* Basic env.yaml error checking - Check for missing parts of the passed in env.yaml file

## v1.0 Release
* Test Suites - Ability to group tests into suites via a suites.yaml file or by grouping
                test directories into a suite directory.
* HPC Runner - HPC class to run jobs on compute nodes
* Basic Text Reporter - A basic reporter that creates a report and outputs it via
                        stdout.
* List Test - Print detailed information of a single test
* List Modset - Print detailed information of a single modset
* List Libraries - Return a list of the libraries for a single modset
* ~/.smarts.conf - Config file to reduce the number of command line options (e.g. -e and -t)
