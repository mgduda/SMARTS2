program f_mpi

   use mpi

   integer :: ierr

   call MPI_Init(ierr)
   call MPI_Finalize(ierr)
   stop
end program f_mpi
