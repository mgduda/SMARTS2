import sys
from multiprocessing import shared_memory

class HPC:
    def __init__(self, type, *args, **kwargs):
        self.type = type
        return 

    def launch_job(self, command, PBS_OPTIONS=None, SLURM_OPTIONS=None, *args, **kwargs):
        # Launch a job onto the self.type HPC with the command
        # Kwargs: timeout = length?, blocking

        # Grab the ID of the job, and report its initial qstat reference to the user (if running in
        # nonblocking). 

        # TODO: Don't allow jobs to submit to a interactive job

        if self.type == "PBS": 
            pass
        elif self.type == "SLURM":
            pass
        else:
            print("That Batch scheduler is not a valid batch scheduler!", self.type)
            sys.exit(-1)

    def cancel_job(self, job):
        # Cancel the HPC job, job
        pass

    def wait(self, job, timeout):
        # Wait on a job to finish - Easiest way to wait on a job might be to look for the file that
        # is created at the end, rather then just running `qstat -fu $USER`, which bogs down the system
        # or `qstat -u $USER` which updates every 1 minute

        # At the end of the timeout, call `qstat -fu $USER` and report status to the user
        if self.type == "PBS": 
            pass
        elif self.type == "SLURM":
            pass
        else:
            print("That Batch scheduler is not a valid batch scheduler!", self.type)
            sys.exit(-1)
        pass

