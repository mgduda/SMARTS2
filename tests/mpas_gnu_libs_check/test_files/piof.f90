program test
   use mpi
   use pio
   use piolib_mod

   integer :: ierr

   call MPI_Init(ierr)

   call Init_Intracom(0, MPI_COMM_WORLD, 1, 0, 1, PIO_rearr_box, io_system)

   call MPI_Finalize(ierr)
   stop

end program test
