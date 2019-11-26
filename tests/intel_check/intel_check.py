import sys
import os

class intel_check:
    test_name = "Intel Compiler Check"
    test_description = "Check to see if there is a Intel compiler is on the machine and able to be" \
                       " found by SMARTs"
    nCPUs = 1
    status = None

    def run(self, env, hpc, *args, **kwargs):
        # Load INTEL Compilers
        intel_compilers = env.list_modsets(name="INTEL")
        for versions in intel_compilers:
            version = versions['compiler']['version']

            # For each compiler, test to see if we can make, and compile simple
            # C and Fortran programs
            if not env.load_modset(versions):
                print("Failed to load", versions)
                self.status = "FAILED"
                return self.status

            print("INTEL_CHECK: Checking to see if intel", versions['compiler']['version'],
                  "can compile C and Fortran programs...")

            simple_c_prog = "int main(void) { return 0; }"
            simple_fortran_prog = "end"

            c_prog_file = open('./simple_c_prog.c', 'w')
            c_prog_file.write(simple_c_prog)
            c_prog_file.close()

            # Check to see if the c program source file was written
            if not os.path.isfile('./simple_c_prog.c'):
                print("FAILED: Was unable to create ./simple_c_prog.c")
                self.status = "FAILED"
                self.err_msg = "Unable to create ./simple_c_prog.c"
                return -1

            fortran_prog_file = open('./simple_fortran_prog.f90', 'w')
            fortran_prog_file.write(simple_fortran_prog)
            fortran_prog_file.close()

            # Check to see if the fortran source file was written
            if not os.path.isfile('./simple_fortran_prog.f90'):
                print("FAILED: Was unable to create ./simple_fortran_prog.f90")
                self.status = "FAILED"
                self.err_msg = "Unable to create ./simple_fortran_prog.f90"
                return -1

            # Compiler c program and check to see if it compiles correctly 
            if os.system('icc -o c_prog simple_c_prog.c') != 0:
                print("Failed to compile simple_c_prog.c with icc")
                self.status = "FAILED"
                self.err_msg = "Failed to copmile simple_c_prog.c with intel/"+version
                return self.status
            else:
                print("Intel", versions['compiler']['version'], "can compile C programs ...")
            
            # Compile Fortran program and check to see if it compiles correctly
            if os.system('ifort -o f_prog simple_fortran_prog.f90') != 0:
                print("Failed to compile simple_fortran_prog.f90 with ifort")
                self.status = "FAILED"
                self.err_msg = "Failed to copmile simple_fortran_prog.f90 with intel/"+version
                return self.status
            else:
                print("Intel", versions['compiler']['version'], "can compile Fortran programs ...")

        print("intel_check - COMPLETE!")
        self.status = "TRUE"
        return self.status

        return 
