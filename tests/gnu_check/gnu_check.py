import os

class gnu_check:
    test_name = "GNU Compiler Check"
    test_description = "Check to see if there is a GNU compiler is on the machine and able to be" \
                       " found by SMARTs"

    nCPUs = 1
    status = None

    def run(self, env, hpc, *args, **kwargs):

        # Load GNU Compilers

        # gnu_compilers = env.list_modsets(name="GNU")


#        for versions in gnu_compilers:
#            env.load_modset(versions)
       
        
        simple_c_prog = "int main(void) { return 0; }"
        simple_fortran_prog = "end"

        c_prog_file = open('./simple_c_prog.c', 'w')
        c_prog_file.write(simple_c_prog)
        c_prog_file.close()

        # Check to see if the c program source file was written

        fortran_prog_file = open('./simple_fortran_prog.f90', 'w')
        fortran_prog_file.write(simple_fortran_prog)
        fortran_prog_file.close()

        # Check to see if the fortran source file was written


        # Compiler c program and check to see if it compiles correctly


        # Compile Fortran program and check to see if it compiles correctly

