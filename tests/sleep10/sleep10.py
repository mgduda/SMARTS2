import os
import time

class sleep10:
    test_name = "Sleep 10"
    test_description = "Sleep for 10 seconds"
    nCPUs = 1
    status = None
    dependencies = None

    def run(self, env, src_dir, test_dir, hpc=None, *args, **kwargs):
        time.sleep(10) 
        self.status = "PASSED"
        return self.status
        
