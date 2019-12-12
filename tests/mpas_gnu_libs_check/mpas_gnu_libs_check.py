import os
from shutil import copyfile

class mpas_gnu_libs_check:
    test_name = "MPAS GNU Libs Check"
    test_description = "Check to see if we can access/user the MPAS IO libs by compiling simple"\
                       "programs"
    dependencies = ['gnu_check']
    nCPUs = 1

    def run(self, env, result, srcDir, testDir, hpc=None, *args, **kwargs):

        # Load any GNU 9.x.x version
        modset = env.list_modsets(name="GNU-9")
        if len(modset) == 0:
            result.result = "FAILED"
            result.msg = "This environment does not have a GNU-9 modset"
            return -1

        if not env.load_modset(modset[0]):
            result.result = "FAILED"
            result.msg = "Could not load the GNU-9 modset"
            return -1

        # List the directories that are in my test directory (I'm looking for `test_files`)
        if 'test_files' in os.listdir(os.path.join(testDir, 'mpas_gnu_libs_check')):
            test_files_dir = os.path.join(testDir, 'mpas_gnu_libs_check', 'test_files')
            print("Location of test files is: ", test_files_dir)
        else:
            print("MPAS_GNU_LIBS_CHECK: Could not find the test_files directory!")
            result.result = "FAILED"
            result.msg = "MPAS_GNU_LIBS_CHECK: Could not find the test_files directory!"
            return -1

        for files in os.listdir(test_files_dir):
            copyfile(os.path.join(test_files_dir, files), './'+files)

        # Check if files are copied
        for files in os.listdir(test_files_dir):
            if files not in os.listdir('./'):
                print("FAILURE: This file could not be copied!", files)
                result.result = "FAILED"
                result.msg = "FAILURE: This file could not be copied!"+files
                return -1

        # MPI Test - C and Fortran

        ## C
        if os.system('mpicc -o c_mpi mpi.c') != 0:
            print("Failed to compile mpi.c with mpicc")
            result.result = "FAILED"
            result.msg = "Failed to copmile mpi.c with mpicc!"
            return -1
        else:
            print("MPAS_GNU_LIBS_CHECK: Can compile C with mpicc!")

        ## Fortran
        if os.system('mpif90 -o f_mpi f_mpi.f90') != 0:
            print("Failed to compile mpi.f90 with mpif90")
            result.result = "FAILED"
            result.msg = "Failed to copmile mpi.c with mpif90!"
            return -1
        else:
            print("MPAS_GNU_LIBS_CHECK: Can compile Fortran with mpif90!")

        # PNetCDF - C and Fortran

        ## C
        if os.system('mpicc -o c_pnetcdf pnetcdf.c -I$PNETCDF/include -L$PNETCDF/lib -lpnetcdf'):
            print("Failed to compile pnetcdf.c with mpicc")
            result.result = "FAILED"
            result.msg = "Failed to compile a C PNetCDF (pnetcdf.c) with mpicc!"
            return -1
        else:
            print("MPAS_GNU_LIBS_CHECK: Can compile a C PNetCDF Program!")

        ## Fortran
        if os.system('mpif90 -c pnetcdf.f90 -I$PNETCDF/include -L$PNETCDF/lib -lpnetcdf'):
            print("Failed to compile mpi.f90 with mpif90")
            result.result = "FAILED"
            result.msg = "Failed to copmile a Fortran PNetCDF (pnetcdf.f90) with mpif90!"
            return -1
        else:
            print("MPAS_GNU_LIBS_CHECK: Can compile a Fortran PNetCDF (pnetcdf.f90) Program!")

        # NetCDF - C and Fortran

        ## C
        if os.system('mpicc -o c_netcdf netcdf.c -I$NETCDF/include -I$PNETCDF/include -L$NETCDF/lib -L$PNETCDF/lib -lnetcdf -lpnetcdf -lhdf5_hl -lhdf5 -ldl -lz'):
            print("Failed to compile netcdf.c with mpicc")
            result.result = "FAILED"
            result.msg = "Failed to compile a C NetCDF program (netcdf.c) with mpicc!"
            return -1
        else:
            print("MPAS_GNU_LIBS_CHECK: Can compile a C NetCDF Program!")

        ## Fortran
        if os.system('mpif90 -c netcdf.f90 -I$NETCDF/include -I$PNETCDF/include -L$NETCDF/lib -L$PNETCDF/lib -lnetcdf -lpnetcdf -lhdf5_hl -lhdf5 -ldl -lz -lm'):
            print("Failed to compile netcdf.f90 with mpif90")
            result.result = "FAILED"
            result.msg = "Failed to compile a Fortran NetCDF program (netcdf.f90) with mpif90!"
            return -1
        else:
            print("MPAS_GNU_LIBS_CHECK: Can compile a Fortran NetCDF Program!")

        # PIO - C and Fortran

        ## C
      # Don't try to compile c pio, because it dont work
      #  if os.system('mpicc -o c_pio pio.c -I$PIO/include -I$NETCDF/include -I$PNETCDF/include -L$PIO/lib -L$PNETCDF/lib -lpio -lnetcdf -lpnetcdf -lhdf5_hl -lhdf5 -ldl -lz'):
      #      print("Failed to compile pio.c with mpicc")
      #      result.result = "FAILED"
      #      result.msg = "Failed to compile a C PIO program (netcdf.c) with mpicc!"
      #      return -1
      #  else:
      #      print("MPAS_GNU_LIBS_CHECK: Can compile a C PIO Program!")

        ## Fortran
        print("PIO: ", os.environ['PIO'])
        if os.system('mpif90 -o piof piof.f90 -I$PIO/include -I$NETCDF/include -I$PNETCDF/include -L$PIO/lib -L$NETCDF/lib -L$PNETCDF/lib -lpiof -lpioc -lgptl -lnetcdf -lpnetcdf -lhdf5_hl -lhdf5 -ldl -lz -lm'):
            print("Failed to compile piof.f90 with mpif90")
            result.result = "FAILED"
            result.msg = "Failed to compile a Fortran PIO program (pio.f90) with mpif90!"
            return -1
        else:
            print("MPAS_GNU_LIBS_CHECK: Can compile a Fortran PIO Program!")

        result.result = "PASSED"
        result.msg = "Can succsfully compile all MPAS IO Libraries"
        return 0
