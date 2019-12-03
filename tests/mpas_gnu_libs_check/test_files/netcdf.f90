program netcdf_test

   use mpi
   use netcdf

   integer :: ierr, ncid

   ierr = nf90_create('blah.nc', NF90_CLOBBER, ncid)
   ierr = nf90_close(ncid)

   stop 

end program netcdf_test
