program pnetcdf_test

   use mpi
   use pnetcdf

   integer :: ierr, ncid

   call MPI_Init(ierr)

   ierr = nf90mpi_create(MPI_COMM_WORLD, 'pnetcdfBlah.nc', NF90_CLOBBER, MPI_INFO_NULL, ncid)
   ierr = nf90mpi_close(ncid)

   call MPI_Finalize(ierr)

   stop 

end program pnetcdf_test
