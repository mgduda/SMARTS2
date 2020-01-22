import os

class example_test:
        test_name = "Example Test"
        test_description = "Create a Hello World C and Fortran program and try to compile it"
        nCPUs = 1
        test_dependencies = None

        """ This test will load a GNU-9 modset, create a Hello World C and Fortram program and
        compile it with the GNU compile we loaded """

        def run(self, env, result, srcDir, testDir, hpc=None):

                        
                c_prog = '#include <stdio.h>\nint main(void){ printf("Hello World!\\n"); return 0;}'
                f_prog = 'program HelloWorld\nimplicit none\nwrite(6,*)"Hello World!"\nend program'

                gnu9 = env.list_modsets(name="GNU-9")
                if len(gnu9) == 0:
                        result.result = "FAILED"
                        result.msg = "Could not load a GNU-9 Modset"
                        return -1

                c_file = open('HelloWorld.c', mode='w')

                if not os.path.isfile('HelloWorld.c'):
                        result.result = "FAILED"
                        result.msg = "'HelloWorld.c' was not created!"
                        return -1

                c_file.write(c_prog)
                c_file.close()
                
                if os.system('gcc -o helloworld_c HelloWorld.c'):
                        result.result = "FAILED"
                        result.msg = "Failed to compiled HelloWorld.c with gcc"
                        return -1

                f_file = open('HelloWorld.f90', mode='w')

                if not os.path.isfile('HelloWorld.f90'):
                        result.result = "FAILED"
                        result.msg = "'HelloWorld.f90' was not created!"
                        return -1

                f_file.write(f_prog)
                f_file.close()

                if os.system('gfortran -o helloworld_f HelloWorld.f90'):
                        result.result = "FAILED"
                        result.msg = "Failed to compiled HelloWorld.F90 with gfortran"
                        return -1

                result.result = "PASSED"
                result.msg = "Succesfully compiled C and Fortran Programs"
                return 0
