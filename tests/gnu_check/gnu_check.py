import os

class gnu_check:
    test_name = "GNU Compiler Check"
    test_description = "Check to see if there is a GNU compiler is on the machine and able to be" \
                       " found by SMARTs"
    nCPUs = 1
    status = None

    def run(self, env, src_dir, test_dir, hpc=None, *args, **kwargs):
        # Load GNU Compilers
        gnu_compilers = env.list_modsets(name="GNU")
        for versions in gnu_compilers:
            version = versions['compiler']['version']
            # For each compiler, test to see if we can make, and compile simple
            # C and Fortran programs
            if not env.load_modset(versions):
                print("Failed to load", versions)
                self.status = "FAILED"
                return self.status

            print("GNU_CHECK: Checking to see if gnu", versions['compiler']['version'],
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
            if os.system('gcc -o c_prog simple_c_prog.c') != 0:
                print("Failed to compile simple_c_prog.c with gcc")
                self.status = "FAILED"
                self.err_msg = "Failed to copmile simple_c_prog.c with gcc/"+version
                return self.status
            else:
                print("GNU", versions['compiler']['version'], "can compile C programs ...")
            
            # Compile Fortran program and check to see if it compiles correctly
            if os.system('gfortran -o f_prog simple_fortran_prog.f90') != 0:
                print("Failed to compile simple_c_prog.c with gcc")
                self.status = "FAILED"
                self.err_msg = "Failed to copmile simple_c_prog.c with gcc/"+version
                return self.status
            else:
                print("GNU", versions['compiler']['version'], "can compile Fortran programs ...")

        print("gnu_check - COMPLETE!")
        self.status = "TRUE"
        return self.status
