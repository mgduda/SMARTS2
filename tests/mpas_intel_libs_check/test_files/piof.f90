program test
   use mpi
   use pio

   integer :: ierr
   type (iosystem_desc_t) :: io_system

   call MPI_Init(ierr)

   call PIO_Init(0, MPI_COMM_WORLD, 1, 0, 1, PIO_rearr_box, io_system)

   call MPI_Finalize(ierr)
   stop

end program test
