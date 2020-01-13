import os
import shutil

class mpas_atm_intel_compile:
    test_name = "MPAS Atmosphere Intel Compile"
    test_description = "Compile MPAS Atmosphere with Intel (If possible)"
    dependencies = ['intel_check', 'mpas_intel_libs_check']
    nCPUs = 4

    def run(self, env, result, src_dir, test_dir, hpc=None, *args, **kwargs):
        
        intel_modset_name = env.list_modsets(name="INTEL")
        if not intel_modset_name:
            result.result = "FAILED"
            result.msg = "This env file had no modsets with the name: 'INTEL'"
            return result.result

        if not env.load_modset(intel_modset_name[0]):
            result.result = "FAILED"
            result.msg = "Could not load the INTEL modset"
            return result.result

        # Check to see if we are in an MPAS src directory
        if not os.path.isdir(os.path.join(src_dir, 'src', 'core_atmosphere')):
            result.result = "FAILED"
            result.msg = src_dir+" does not appear to be a MPAS source directory"
            return result.result

        # Copy the MPAS source into its own directory in the current run directory
        mpas_src_copy = os.path.join('./', 'MPAS-Model')
        shutil.copytree(src_dir, mpas_src_copy)
        if not os.path.isdir(mpas_src_copy):
            result.result = "FAILED"
            result.msg = "MPAS source directory was not copied succesfully!"

        # Change directory to MPAS-Model
        os.chdir(mpas_src_copy)

        # Clean MPAS for MPAS-A
        ierr = os.system('make clean CORE=atmosphere &> ../atmosphere-clean.log')
        if ierr != 0:
            result.result = "FAILED"
            result.msg = "Could not clean MPAS atmosphere core"
            return

        print("MPAS_INTEL_COMPILE: Compiling MPAS Atmosphere CORE ....")
        ierr = os.system('make -j4 ifort CORE=atmosphere &> ../atmosphere-compile.log')
        if ierr != 0:
            result.result = "FAILED"
            result.msg = "Could not compile MPAS Atmosphere core"
            return

        if not os.path.isfile('./atmosphere_model'):
            result.result = "FAILED"
            result.msg = "Make command returned 0, but could not find 'atmosphere_model'"
            return result.result

        result.result = "PASSED"
        result.msg = "MPAS Atmosphere Core compiled succesfully"
