#include <stdio.h>
#include <netcdf.h>

int main(void) { 
	int ierr;
	int ncid;

	if ((ierr = nc_create("blarh.nc", NC_CLOBBER, &ncid))) {
		fprintf(stderr, "Error: %s\n", nc_strerror(ierr));
		return -1;
	}

	if ((ierr = nc_close(ncid))) {
		fprintf(stderr, "Error: %s\n", nc_strerror(ierr));
		return -1;
	}

	return 0;
}
