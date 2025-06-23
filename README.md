# Simple MPAS Atmosphere Regression Testing System (SMARTS)

The Simple MPAS Atmosphere Regression Testing System or SMARTS, is a general
regression testing system. Developed to test changes for MPAS Atmosphere and
its tool set, it allows for generalized testing of software on different
machines in an efficient manner.

SMARTS is written in Python, and its tests are also written in Python, thus,
anything that can be coded in Python can be made into a test. For instance,
creating a file in Python, calling a subprocess to compile MPAS code, or
launching a simulation.

Tests are launched as subprocesses, and can be launched concurrently to
maximize efficiency. Machine resources (number of cpus, compilers, libraries,
MPI implementations) are described in env.yaml files and thus enable SMARTS to
be used with on a verity of machines with a verity of compilers and libraries.

SMARTS also has the ability to submit jobs supercomputers (such as the Cheyenne
super computer) using PBS.

This README only serves as a quickstart guide to using SMARTS. For a more
in-depth README see the LaTeX documentation in the `doc/` directory.

# Quickstart Guide

0. Install [https://pyyaml.org/wiki/PyYAML](PyYAML) - `pip3 install pyYAML
   --user`. If you're running on Cheyenne, this module is available by running
   `ncar_pylib`.
```
ml load python
ml load ncarenv
ncar_pyblib
```

1. Clone SMARTS onto your Machine and create an env.yaml file for your machine.
The envs/ directory contains already created env.ymal files. Use these, and
the Environment section of the design document to create one for your
machine.

2. List and run tests - Next, see if you can run the `smarts.py` command line
program by running `python3 smarts.py -h`:

``` 
usage: smarts [-h] [-e env.yaml] [-s dir] [-t dir] [-v level] {list,run} ...

A regression testing system for MPAS

optional arguments:
  -h, --help            show this help message and exit

Required arguments:
  -e env.yaml, --env-file env.yaml
                        The location of the env.yaml file
  -s dir, --src-dir dir
                        The directory that holds the code to test changes
                        (MPAS-Model)
  -t dir, --test-dir dir
                        The location of the test directory

Optional arguments:
  -v level, --verbose level
                        Output debug level

subcommands:
  command description

  {list,run}            Sub-command help message
    list                List SMART's tests, test suites and compilers
    run                 Run a test or a test-suite by name
```

The smarts.py program works in a similar manner as the git command line
program. It has subcommands. For instance, git has `git remote`, `git remote
list` and `git add`, `git commit`, etc. smarts.py works in a similar manner.
Subcommands for smarts are: `smarts.py list` and `smarts.py run`. Each subcommand
contains its own help message, which can be retrieved by typing `smarts.py
subcommand --help`. To bring up the help message above, type `smarts.py -h`.

The smarts.py program needs three required arguments to run:
* An environment file (`-e/--env`),
* A directory that contains tests (`-t/--test-dir`)
* A source directory that contains the source code you want to test
  (`-s/--src-dir`).

While using all of the above required arguments running `python3 smarts.py list
tests` will display the tests available in the directory passed by `-t`.

3. Create a new test

Tests are implemented in Python as a class and are imported by the SMARTS
TestRunner.  Individual tests will need to reside in a directory of their own
inside the main test directory. The name of this directory will need to be the
same name of the file of the test and will need to be the same name of the
class of the tests.

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

Tests will need the follow attributes in their class for the test to be ran:
1. `test_name` - Optional - The long name of the test
2. `test_description` - Optional - The description of the test 
3. `ncpus` - Required - The number of CPUs this test will use
4. `test_depencies` - Optional - A list of test launch names (i.e. classnames)
   that this test is dependent on. For instance: `['gnu_check', 'intel_check']`

The test will then also need to have a run function as the one above with the
same arguments and in the same position:
``` Python
def run(self, env, result, src_dir, test_dir, hpc=None, *args, **kwargs):
```
You can use these arguments to help write your tests.

1. `env` - The Env Class Instance - A copy of the environment class loaded with
   the env.yaml file specified for the machine. You can use the environment
   class to find and load specific modsets.
2. `result` - Result Object - A result object. This object will communicate the
   result of your test with the TestScheduler. Set the attribute result
   (`result.result`) to either "PASSED" or "FAILED" respectively. If your test
   does not set `result.result` your test will fail. `result.msg` can be set to
   notify the user of the reason of failure (or success).
3. `src_dir` - String - The directory that contains the source files to be
   tested. Use this path to copy files from the code you wish to test. This is
   the directory that was passed in via the `-s/--src-dir`.
4. `test_dir` - String - The directory that contains the test informations.
   Use this path to retrieve default input files (i.e. namelist.atmosphere for
   an idealized MPAS simulation). This is the directory that was passed in via
   the `-t/--test-dir`.
5. `hpc`- HPC Class Instance or None - An HPC class that will be an interface
   to the HPC scheduler. If HPC == None, then this
   machine is not an HPC.

# Planned Features

## Beta Release - v0.5
* ~~Dependencies~~
* ~~Schedules Test Concurrently~~
* ~~Load Modules Completely~~
   * ~~Loads compilers, mpi implementations and libraries~~
   * ~~Needs a little more testing~~
* ~~Runs tests and reports their status via stdout (but does not call a reporter)~~
* ~~Requirements Document mostly finished~~
* ~~Basic env.yaml error checking - Check for missing parts of the passed in env.yaml file~~

## v1.0 Release
* ~~HPC Runner - HPC class to run jobs on compute nodes~~
* Basic Text Reporter - A basic reporter that creates a report and outputs it via
                        stdout.
* List Modset - Print detailed information of a single modset
* List Libraries - Return a list of the libraries for a single modset
* ~/.smarts.conf - Config file to reduce the number of command line options
  (e.g. -e and -t)
* Standard Library - If desired/wanted?
