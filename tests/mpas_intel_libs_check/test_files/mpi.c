#include <stddef.h>
#include "mpi.h"


int main(void) {

    MPI_Init(NULL, NULL);
	MPI_Finalize();

	return 0;
}
