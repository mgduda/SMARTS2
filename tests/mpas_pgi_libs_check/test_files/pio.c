#include <stddef.h>
#include "pio.h"
#include "mpi.h"


int main(void) {
	
	int iosysid;

	MPI_Init(NULL, NULL);
	PIOc_Init_Intracomm(MPI_COMM_WORLD, 1, 1, 1, PIO_REARR_BOX, &iosysid);
	PIOc_free_iosystem(iosysid);
	MPI_Finalize();

	return 0;
}
