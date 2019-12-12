import sys
import os

class intel_check:
    test_name = "Intel Compiler Check"
    test_description = "Check to see if there is a Intel compiler is on the machine and able to be" \
                       " found by SMARTs"
    nCPUs = 1

    def run(self, env, result, src_dir, test_dir, hpc, *args, **kwargs):
        # Load INTEL Compilers
        intel_compilers = env.list_modsets(name="INTEL")
        for versions in intel_compilers:
            modset = env.load_modset(versions)

            # For each compiler, test to see if we can make, and compile simple
            # C and Fortran programs
            if not modset:
                result.result = "FAILED"
                result.msg = "Failed to load "+versions
                return -1

            simple_c_prog = "int main(void) { return 0; }"
            simple_fortran_prog = "end"

            c_prog_file = open('./simple_c_prog.c', 'w')
            c_prog_file.write(simple_c_prog)
            c_prog_file.close()

            # Check to see if the c program source file was written
            if not os.path.isfile('./simple_c_prog.c'):
                result.result = "FAILED"
                result.msg = "Unable to create ./simple_c_prog.c"
                return -1

            fortran_prog_file = open('./simple_fortran_prog.f90', 'w')
            fortran_prog_file.write(simple_fortran_prog)
            fortran_prog_file.close()

            # Check to see if the fortran source file was written
            if not os.path.isfile('./simple_fortran_prog.f90'):
                result.result = "FAILED"
                result.msg = "Unable to create ./simple_fortran_prog.f90"
                return -1

            # Compiler c program and check to see if it compiles correctly 
            if os.system('icc -o c_prog simple_c_prog.c') != 0:
                result.result = "FAILED"
                result.msg = "Failed to copmile simple_c_prog.c with intel/"+version
                return -1
            
            # Compile Fortran program and check to see if it compiles correctly
            if os.system('ifort -o f_prog simple_fortran_prog.f90') != 0:
                result.result = "FAILED"
                result.msg = "Failed to copmile simple_fortran_prog.f90 with intel/"+version
                return -1

        result.result = "PASSED"
        result.msg = "Intel Check COMPLETED!"
        return 0
