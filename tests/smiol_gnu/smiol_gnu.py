import os
import shutil
import subprocess

class smiol_gnu:
    test_name = "SMIOL GNU Test"
    test_description = "See if SMIOL runs successfully with GNU"
    nCPUs = 1

    def run(self, env, result, src_dir, test_dir, hpc=None, *args, **kwargs):

        gnu_compilers = env.list_modsets(name="GNU")
        if len(gnu_compilers) == 0:
            result.result = "FAILED"
            result.msg = "Could not load any GNU Modsets!"
            return -1

        for versions in gnu_compilers:
            modset = env.load_modset(versions)
            if not modset:
                result.result = "FAILED"
                result.msg = "Failed to load "+versions
                return -1

            print("VERSIONS: ", versions)

            # For each GNU Version, create a directory and copy in the entire SMIOL directory
            smiol_test_dir = './smiol-'+str(versions)
            shutil.copytree(src_dir, smiol_test_dir)

            if not os.path.isdir(smiol_test_dir):
                result.result = "ERROR"
                result.msg = "Could not create directory: "+smiol_test_dir
                return

            os.chdir(smiol_test_dir)

            ierr = os.system('make gnu')
            if ierr != 0:
                result.result = "FAILED"
                result.msg = "Make gnu returned a non-zero error code: "+str(ierr)
                return

            if not os.path.isfile('libsmiol.a'):
                result.result = "FAILED"
                result.msg = "Could not find 'libsmiol.a' when using Modset: "+versions
                return
                
            if not os.path.isfile('smiol_runner_c'):
                result.result = "FAILED"
                result.msg = "Could not find 'smiol_runner_c' when using Modset: "+versions
                return

            if not os.path.isfile('libsmiolf.a'):
                result.result = "FAILED"
                result.msg = "Could not find 'libsmiolf.a' when using Modset: "+versions
                return

            if not os.path.isfile('smiol_runner_f'):
                result.result = "FAILED"
                result.msg = "Could not find 'smiol_runner_f' when using Modset: "+versions
                return

            c_run = subprocess.Popen('./smiol_runner_c', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            c_run_output = c_run.stderr.read()
            c_run.wait()

            if c_run.returncode != 0:
                result.result = "FAILED"
                result.msg = "Recived non-zero return code from './smiol_runner_c' run: ", str(c_run.returncode)
                return

            f_run = subprocess.Popen('./smiol_runner_f', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            f_run_output = f_run.stderr.read()
            f_run.wait()

            if f_run.returncode != 0:
                result.result = "FAILED"
                result.msg = "Recived non-zero return code from './smiol_runner_f' run: ", str(f_run.returncode)
                return

            # Go back to the main test run directory
            os.chdir('..')

        result.result = "PASSED"
        result.msg = "All SMIOL Checks Passed"



