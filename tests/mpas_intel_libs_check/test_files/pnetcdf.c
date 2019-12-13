#include <pnetcdf.h>
#include <stddef.h>
#include "mpi.h"

int main(void) {

	int ncid, ierr;

    MPI_Init(NULL, NULL);
	ierr = ncmpi_create(MPI_COMM_WORLD, "blah.nc", 
										 NC_64BIT_OFFSET, 
										 MPI_INFO_NULL, 
										 &ncid);
	
	ierr = ncmpi_close(ncid);
	MPI_Finalize();

	return 0;
}
